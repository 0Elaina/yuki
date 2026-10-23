# Yuki 项目概览

Yuki 是一个由平台统一维护曲库、面向多用户的在线音乐网站，用于展示全栈 Web 工程能力。

## 项目定位

- 管理端负责内容维护，用户端提供音乐使用能力，具体功能见[功能需求](02-feature-requirements.md)。
- 优先建设管理端，为用户端提供可维护的数据来源。
- 工程由个人开发维护，优先成熟方案，兼顾模块边界和维护成本。
- 运行目标为本地开发环境。

## 后端技术栈

| 领域 | 技术 |
| --- | --- |
| Python 工程 | uv、Python 3.12、uv_build |
| Web 后端 | FastAPI、Uvicorn |
| 校验与配置 | Pydantic 2、pydantic-settings |
| 数据访问 | SQLAlchemy 2.x asyncio、psycopg 3 binary |
| 关系数据库 | PostgreSQL |
| 结构迁移 | Alembic |
| 静态检查 | Ruff、mypy |
| 持续集成 | GitHub Actions |

## 应用架构

| 方面 | 设计 |
| --- | --- |
| 应用边界 | 同仓库、独立管理端和用户端、按业务模块组织的单后端 |
| 管理端 | 从官方 create-vue 起步，使用 Vue 和 Naive UI |
| 认证 | JWT 加可撤销、可轮换的刷新凭证 |
| 后台任务 | Celery + Redis；API 异步访问数据库，worker 使用独立同步会话，共享模型与纯业务规则 |
| 接口客户端 | 从 OpenAPI 生成 TypeScript 类型及 Axios SDK，认证与错误处理通过手写配置接入 |
| 文件传输 | API 管理授权与业务状态并签发预签名地址，浏览器与对象存储直接传输文件；已签发的读取地址在过期前保持有效 |

## 后端工程

后端以可安装的 `yuki` 包组织，以下路径以项目根目录为基准：

| 位置 | 职责 |
| --- | --- |
| `backend/src/yuki/main.py` | 应用入口，组装生命周期、中间件、异常处理器与路由 |
| `backend/src/yuki/api/` | 公共响应模型与版本化路由聚合 |
| `backend/src/yuki/core/` | 配置、业务异常、HTTP 异常转换与请求中间件 |
| `backend/src/yuki/infra/` | 数据库会话、日志配置与请求 ID 上下文 |
| `backend/migrations/` | Alembic 迁移环境与迁移脚本 |

响应结构与错误码见[公共接口契约](04-api-design/00-error-codes.md)。配置、生命周期及开发命令见[工程指南](05-engineering-guide.md)。

## 参考资料

- [FastAPI 模块组织](https://fastapi.tiangolo.com/tutorial/bigger-applications/)：应用与路由组织。
- [Vue 工具链](https://vuejs.org/guide/scaling-up/tooling)：官方脚手架参考。
- [SQLAlchemy PostgreSQL 方言](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html)：数据库驱动选择参考。
- [Celery 任务](https://docs.celeryq.dev/en/stable/userguide/tasks.html)：任务执行与重试参考。
- [FastAPI JWT 示例](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)与[OWASP 会话管理](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)：认证与会话设计参考。
