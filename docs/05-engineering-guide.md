# 工程指南

## 依赖与启动

| 对象 | 工程位置 | 管理方式 |
| --- | --- | --- |
| 后端 | backend | Python 3.12，uv 管理 pyproject.toml 与 uv.lock |
| 前端 | frontend | pnpm 管理 package.json 与 pnpm-lock.yaml |
| 数据库迁移 | backend/migrations | Alembic 管理业务结构版本 |

后端工作目录为 backend。依赖声明与锁文件共同维护，开发和部署使用锁定结果。参考 [uv 项目结构](https://docs.astral.sh/uv/concepts/projects/layout/)。

安装依赖使用 `uv sync`，启动使用 `uv run yuki-api`。命令入口为 yuki.main:main，通过 Uvicorn 应用工厂启动服务，默认地址为 http://127.0.0.1:8000，交互文档位于 /docs。

本地配置使用 backend/.env，以 .env.example 为字段模板，填写共享服务凭据。HTTP_RELOAD 控制开发重载，重载仅监听后端 src 目录。

| 操作 | 在 backend 执行的命令 |
| --- | --- |
| 静态检查 | uv run ruff check . |
| 检查格式 | uv run ruff format --check . |
| 格式化 | uv run ruff format . |

## Git 工作流

采用 main 与短期任务分支，参考 [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow)。Git 操作由开发者执行。

1. 开始任务前同步 main，再创建或切换任务分支；分支使用 type/简短英文主题，例如 feat/character-config、ci/backend-checks。
2. 按独立改动提交，使用 `type(scope): 中文说明`，scope 可省略；常用类型为 feat、fix、refactor、docs、chore、ci，参考 [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)。
3. 推送任务分支，创建以 main 为目标的 PR；确认改动和 CI 通过后，使用 Create a merge commit 合并，保留分支提交。
4. 合并后同步本地 main，删除已合并的本地及远程任务分支。

## CI

GitHub Actions 配置位于 [.github/workflows/ci.yml](../.github/workflows/ci.yml)，在提交到 main 及创建或更新面向 main 的 PR 时运行。

后端使用 Python 3.12、uv 0.13.0，通过 `uv sync --locked` 按锁文件安装依赖，然后在 backend 执行以下只读检查：

| 检查 | 命令 |
| --- | --- |
| Ruff 静态检查 | uv run --no-sync ruff check . |
| Ruff 格式检查 | uv run --no-sync ruff format --check . |

依赖声明与 uv.lock 一同提交；依赖变更后先在本地运行 uv sync 更新锁文件。CI 不读取本地 .env，不启动数据库或 Redis。接入方式参考 [uv 官方 GitHub Actions 指南](https://docs.astral.sh/uv/guides/integration/github/)。

## 本地共享基础设施

共享 Docker 基础设施位于 `/home/nepgear/001-Own/01-Dev/dev-infra`。

| 配置来源 | 内容 |
| --- | --- |
| dev-infra/docker-compose.yml | 镜像、容器名、端口映射、网络与数据卷 |
| dev-infra/.env | 服务端口、账号与凭据 |
| dev-infra/README.md | 共享服务维护说明 |

| 服务 | 共享镜像标签 | 宿主机应用访问 | 共享网络内访问 |
| --- | --- | --- | --- |
| PostgreSQL | postgres:17-alpine | 127.0.0.1:5432 | dev-postgres:5432 |
| Redis | redis:7-alpine | 127.0.0.1:6379 | dev-redis:6379 |
| RustFS S3 API | rustfs/rustfs:latest | http://127.0.0.1:9000 | http://dev-rustfs:9000 |
| RustFS 控制台 | 与 S3 API 同一容器 | http://127.0.0.1:9001 | http://dev-rustfs:9001 |

服务地址与镜像标签取自共享配置。后端在宿主机运行时使用映射端口，在容器内运行时接入 `dev_infra_network` 并使用容器名。

RustFS SDK 使用 S3 API 端点，浏览器使用其可访问的资源地址；latest 标签随镜像更新变化，使用能力以目标版本的 [S3 兼容范围](https://docs.rustfs.com/en/reference/s3-compatibility)为准。

## 本地资源约定

| 资源 | 名称 |
| --- | --- |
| PostgreSQL 账号 | 沿用共享 postgres 账号 |
| PostgreSQL 数据库 | yuki |
| Redis 键前缀 | yuki: |
| RustFS bucket | yuki-media |

项目连接与迁移目标为 yuki 数据库，资源操作限定在项目范围。Redis 键通过 infrastructure.redis.redis_key 按业务和对象标识拼接，参考 [Redis 键名约定](https://redis.io/docs/latest/develop/using-commands/keyspace/)。

## 环境配置

配置使用 Pydantic Settings，AppSettings、PostgresSettings、RedisSettings 分别校验各自字段。进程环境变量优先于 backend/.env，配置文件路径由后端源码位置确定，不随启动工作目录变化。字段名不区分大小写，参考 [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)。

配置通过 settings_cached() 加载并按进程复用，修改后重启服务生效；该原生方法要求 pydantic-settings 2.16 及以上版本，参考[官方发布说明](https://github.com/pydantic/pydantic-settings/releases/tag/v2.16.0)。

.env.example 保存公开示例，真实密码仅填写本地 .env 或进程环境。密码保持原值，不能为空。前端可访问的环境变量仅存公开配置，参考 [Vite 环境变量](https://vite.dev/guide/env-and-mode)。

### 应用

| 环境变量 | 类型 | 默认值 | 约束与用途 |
| --- | --- | --- | --- |
| LOG_LEVEL | string | INFO | DEBUG、INFO、WARNING、ERROR、CRITICAL |
| HTTP_HOST | string | 127.0.0.1 | 非空监听主机，容器部署可配置为 0.0.0.0 |
| HTTP_PORT | int | 8000 | 1 至 65535 |
| HTTP_RELOAD | bool | false | 是否启用源码重载，示例配置为 true |
| CORS_ALLOW_ORIGINS | JSON array of string | ["http://localhost:5173","http://127.0.0.1:5173"] | 允许的浏览器来源，.env 中使用 JSON 数组 |

CORS 使用原生中间件，关闭凭据跨域，允许方法与请求头。

### PostgreSQL

| 环境变量 | 类型 | 默认值 | 约束与用途 |
| --- | --- | --- | --- |
| POSTGRES_HOST | string | 127.0.0.1 | 非空主机 |
| POSTGRES_PORT | int | 5432 | 1 至 65535 |
| POSTGRES_USER | string | postgres | 非空账号 |
| POSTGRES_PASSWORD | string | 必填 | 非空密码 |
| POSTGRES_DB | string | yuki | 非空目标数据库 |
| POSTGRES_SSLMODE | string | disable | disable、allow、prefer、require、verify-ca、verify-full |
| POSTGRES_POOL_SIZE | int | 5 | 大于 0，连接池保留连接数 |
| POSTGRES_MAX_OVERFLOW | int | 5 | 大于等于 0，允许额外连接数 |
| POSTGRES_POOL_TIMEOUT_SECONDS | number | 30 | 大于 0，等待连接池的秒数 |
| POSTGRES_CONNECT_TIMEOUT_SECONDS | int | 5 | 大于 0，驱动连接超时秒数 |

使用 Psycopg 3 异步驱动，连接会话时区为 UTC，连接池启用 pre-ping，日志隐藏 SQL 参数。URL.create 处理用户名、密码中的特殊字符，完整连接串不输出到日志。

### Redis

| 环境变量 | 类型 | 默认值 | 约束与用途 |
| --- | --- | --- | --- |
| REDIS_HOST | string | 127.0.0.1 | 非空主机 |
| REDIS_PORT | int | 6379 | 1 至 65535 |
| REDIS_PASSWORD | string | 必填 | 非空密码 |
| REDIS_DB | int | 0 | 大于等于 0 |
| REDIS_CONNECT_TIMEOUT_SECONDS | number | 5 | 大于 0，连接超时秒数 |
| REDIS_COMMAND_TIMEOUT_SECONDS | number | 3 | 大于 0，命令超时秒数 |

RedisDep 提供原生异步客户端，开启字符串解码。会话与客户端依赖入口位于 app/dependencies.py，事务使用方式见[数据库约定](03-database-design/00-conventions.md)。

## 生命周期与日志

应用通过 FastAPI lifespan 和 AsyncExitStack 创建及释放数据库、Redis 客户端。配置校验或初始化失败时释放已创建资源，正常关闭时关闭 Redis 和数据库引擎；连接在实际操作时建立。实现参考 [FastAPI lifespan](https://fastapi.tiangolo.com/advanced/events/)。

访问日志和未知异常堆栈使用 Uvicorn 原生输出；应用日志使用标准库 logging，LOG_LEVEL 控制日志级别。

应用日志按需记录业务事件，避免主动输出请求正文、完整对话和服务凭据。SQLAlchemy 开启参数隐藏。

## 数据库迁移

在 backend 工作目录使用 `uv run alembic current` 查看数据库版本，使用 `uv run alembic upgrade head` 应用已有迁移。Alembic 使用 PostgresSettings，不依赖 HTTP 应用或 Redis。

业务模型在 migrations/env.py 显式导入后参与自动生成。生成迁移时使用 Alembic revision 的 --autogenerate 与 -m 参数，执行前审查目标数据库、变更内容和数据转换。版本结构与默认字段约定见[数据库约定](03-database-design/00-conventions.md)。

