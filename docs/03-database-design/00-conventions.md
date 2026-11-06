# 数据库与持久化约定

## 数据访问与事务

业务数据使用 SQLAlchemy 2.x 和 Psycopg 3 异步驱动。Database 持有 AsyncEngine 与 async_sessionmaker，使用 SQLAlchemy 连接池，连接会话时区设为 UTC。连接 URL 通过 URL.create 构造，日志隐藏 SQL 参数。

会话工厂使用 autobegin=False、expire_on_commit=False，保留原生 autoflush。SessionDep 创建并关闭独立 AsyncSession，不查询、不包事务、不提交；依赖使用 function scope，在路由函数结束后释放会话。AsyncSession 不在并发任务间共享，参考 [SQLAlchemy 异步说明](https://docs.sqlalchemy.org/en/21/orm/extensions/asyncio.html)。

查询与持久化归属业务模块的数据访问层。ORM 模型表达存储结构，API 使用独立的 Pydantic 输入输出模型，模块之间通过业务服务协作。

所有业务查询和写入在业务层的 async with session.begin() 内执行，正常退出提交，异常退出回滚。Repository 使用传入的 session，需要获取写入结果时调用 flush()，不自行提交、回滚或另开事务。参考 [SQLAlchemy 显式事务](https://docs.sqlalchemy.org/en/21/orm/session_basics.html#disabling-autobegin-to-prevent-implicit-transactions)。

需要共同提交的跨 Repository 操作由外层业务服务管理。DTO 转换在所需字段可读取时完成，避免响应序列化触发异步懒加载。LLM 推理、语音处理、对象上传和向量索引调用不占用持续打开的数据库事务。

LangGraph 检查点与业务数据分别管理，不默认共享会话或事务；业务 Repository 不直接修改框架内部表。

## 命名与时间

表名、列名和约束名使用 snake_case，Base.metadata 统一生成以下名称。

| 对象 | 命名规则 |
| --- | --- |
| 主键 | pk_表名 |
| 普通索引 | ix_表名_列名组合 |
| 唯一约束 | uq_表名_列名组合 |
| 外键约束 | fk_表名_列名组合_目标表名 |
| 检查约束 | ck_表名_显式约束名，定义 CheckConstraint 时提供 name |

业务模型自行声明所需的 created_at、updated_at，Python 类型为带时区的 datetime，PostgreSQL 类型为非空 timestamptz。字段使用 SQLAlchemy 的 default=utc_now 在写入时填充，updated_at 同时使用 onupdate=utc_now。公共时间函数位于 shared/util/time_utils.py，每次调用返回 datetime.now(UTC)，参考[原生默认值机制](https://docs.sqlalchemy.org/en/20/core/defaults.html)。

新对象在 flush 前不保证已有时间值。原始 SQL、UPSERT 等不执行相应 onupdate 的写法显式维护时间。公共基类不统一附带主键、软删除、版本号或操作人字段。

非空、唯一与关联规则优先落实为数据库约束。索引对应实际筛选、关联或排序场景；软删除、版本号和审计字段按业务需要引入。

## 结构迁移

业务结构通过 backend/migrations 中的 Alembic 迁移管理，由开发者显式执行，应用启动不自动创建或同步业务表。

Alembic 直接读取 PostgresSettings 和 Base.metadata，不创建 Web 应用或连接 Redis；在线迁移使用异步引擎与 NullPool，离线模式支持生成 SQL。业务模型需在 migrations/env.py 显式导入后参与自动生成。

自动生成的迁移需要人工核对目标数据库、结构变更及数据转换，参考 [Alembic 自动生成说明](https://alembic.sqlalchemy.org/en/latest/autogenerate.html)。LangGraph 等组件的内部结构按官方初始化和升级方式维护，不由业务迁移默认接管。

连接来源与项目资源见[工程指南](../05-engineering-guide.md)，会话、检查点和语义索引的数据职责见 [AI 设计](../06-ai-design.md)。
