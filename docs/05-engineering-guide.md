# Yuki 工程指南

本文说明后端开发、接口接入、Git 协作、持续集成和跨设备操作。架构与目录职责见[项目概览](01-project-overview.md)，响应契约见[公共响应与错误码](04-api-design/00-error-codes.md)。

## 后端使用方式

本节命令以 `backend/` 为工作目录。Python 版本由 `.python-version` 指定为 3.12；依赖清单与工具配置位于 `pyproject.toml`，解析后的依赖版本由 `uv.lock` 锁定。

### 恢复依赖与准备配置

在新设备安装 uv 后，恢复锁文件中的依赖：

```bash
uv sync --locked
```

该命令同时安装当前 `yuki` 包，应用和迁移脚本均通过包名导入源码。

启动应用或使用迁移工具前，将 `.env.example` 复制为同目录下的 `.env`，填写配置；也可以通过环境变量提供配置，环境变量优先于 `.env`。

| 环境变量 | 必填 | 格式与用途 |
| --- | --- | --- |
| `DATABASE_URL` | 是 | PostgreSQL 连接地址，格式为 `postgresql+psycopg://用户:密码@地址:端口/数据库`；连接信息中的特殊字符须 URL 编码 |

`core/config.py` 的 `Settings` 使用 `PostgresDsn` 校验连接地址，`get_settings()` 缓存读取结果。应用在生命周期启动时读取配置，迁移工具在相应入口读取配置；缺失或无效值由 Pydantic 报错。静态检查可在仅恢复依赖后执行。

版本控制保留 `.env.example`、依赖清单与锁文件。真实 `.env`、虚拟环境和工具缓存由根目录 `.gitignore` 排除，在各设备本地维护。

### 应用入口

本地开发时使用：

```bash
uv run --locked uvicorn yuki.main:app --reload --no-access-log
```

`yuki.main` 是模块名，`app` 是其中导出的 FastAPI 实例，访问地址以启动输出为准。

`lifespan` 在启动时初始化日志、读取配置、创建异步引擎与会话工厂，将工厂保存到 `app.state.db_session_factory`，关闭时在 `finally` 中释放引擎。数据库连接由实际数据库操作触发，建表与结构变更通过 Alembic 管理。

`infra/database.py` 的请求依赖从应用状态取得工厂，每次创建独立异步会话并负责关闭。工厂使用 `expire_on_commit=False`，业务服务控制事务提交与回滚。

### 请求日志

`infra/logging.py` 使用标准库 `logging`，以 INFO 级别向终端输出时间、级别、模块、请求 ID 和消息。模块通过 `logging.getLogger(__name__)` 获取 logger；非请求上下文的请求 ID 为 `-`。

`core/middleware.py` 使用纯 ASGI 中间件，为 HTTP 请求生成 `uuid4().hex`，同时存入请求状态与 `ContextVar`。请求结束时恢复上下文，并记录一次 INFO 完成日志，采集范围为 `method`、`path`、`status_code`、`duration_ms`，其中路径取 URL 的 path 部分，耗时通过单调时钟计算。非 HTTP scope 原样传递。

未捕获异常由全局处理器记录 ERROR 和堆栈，从请求状态取得 ID 并显式补充到日志和响应头。日志过滤器优先保留显式 ID，其余日志使用当前上下文 ID。

启动命令中的 `--no-access-log` 关闭 Uvicorn 默认访问日志，请求完成日志由应用统一记录，Uvicorn 错误日志继续保留。

### 迁移工具

迁移环境由 `alembic.ini` 和 `migrations/env.py` 提供，脚本目录相对于 `alembic.ini` 定位。修改业务表结构时使用：

| 操作 | 命令 | 使用条件 |
| --- | --- | --- |
| 生成候选迁移 | `uv run --locked alembic revision --autogenerate -m "describe_change"` | 已编写 ORM 模型，且能够连接目标数据库；检查生成内容后再应用 |
| 应用迁移 | `uv run --locked alembic upgrade head` | 已确认迁移脚本，且能够连接目标数据库 |
| 输出迁移 SQL | `uv run --locked alembic upgrade head --sql` | 已有迁移脚本及数据库地址配置，离线生成 SQL |

自动生成通过比较数据库结构与 `Base.metadata` 得到候选脚本。新增 ORM 模型时，在 Alembic 读取元数据前导入相应模型模块，使表定义注册到元数据中。

迁移与应用共用配置入口。在线迁移独立创建同步 psycopg 引擎，使用 `NullPool`，结束后释放；离线迁移根据配置和脚本生成 SQL。

### 静态检查

```bash
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy src/yuki migrations
```

Ruff 检查基础错误、导入排序、语法升级和格式。mypy 通过严格模式及 Pydantic 插件检查应用与迁移 Python 代码。

## 接口接入

### 路由与 OpenAPI

`api/router.py` 定义聚合路由 `api_router`，由 `main.py` 注册到应用。业务模块定义各自的路由，再挂载到聚合入口。

聚合入口通过 FastAPI 的 `responses` 声明 422 的 `ApiResponse[ValidationErrorData]` 和 500 的 `ApiResponse[None]`。这些声明随实际挂载的接口进入 OpenAPI，业务接口需要声明各自的成功响应模型和业务错误响应。业务若复用某个 HTTP 状态表达不同错误详情，需在该接口声明匹配的响应类型。

`responses` 用于描述 OpenAPI 契约，成功响应由接口显式构造，异常响应由已注册的处理器转换。

### 响应构造与异常处理

公共模型定义在 `api/schemas.py`。接口使用 `ApiResponse[T].success(data)` 构造成功正文，并声明匹配的响应模型；异常处理器使用 `ApiResponse[T].error(api_code, data, message)` 构造错误正文，`message` 为空时采用错误定义中的提示。HTTP 状态由路由或处理器设置，序列化时始终保留 `data` 字段及其 `null` 值。

业务服务通过 `core/exceptions.py` 的 `BusinessException` 抛出业务错误，携带 `ApiCode` 和公开提示。`core/exception_handlers.py` 在 HTTP 边界分别处理业务异常、`RequestValidationError`、Starlette `HTTPException` 和未捕获异常。

字段结构、异常分流结果和响应头见[公共响应与错误码](04-api-design/00-error-codes.md)。

## Git 与 GitHub 协作

### 仓库

仓库为 GitHub 公开仓库 `0Elaina/yuki`，通过 SSH 地址 `git@github.com:0Elaina/yuki.git` 访问，默认主分支为 `main`。

### 分支与合并

| 改动 | 提交流程 |
| --- | --- |
| 小幅文档修订、排版、错字、不改变行为的注释 | 可以直接提交并推送 `main` |
| 功能、缺陷修复、结构调整、依赖、CI 配置、重要设计约定变更 | 从最新 `main` 建任务分支，通过 PR 合并 |

任务分支使用 `<type>/<英文短描述>`，例如 `ci/backend-checks`、`docs/git-workflow`。任务完成后通过 Merge commit 合并，保留分支中的各条提交。合并提交的标题使用 PR 标题，正文使用 PR 说明。

合并条件为检查通过并完成自查，由项目维护者自行合并。合并后删除对应远程任务分支，新任务从最新 `main` 创建。`main` 作为持续保留的主分支，已推送的历史通过追加提交修正。

### 提交与 PR 说明

提交和 PR 标题使用 Conventional Commits：

```text
<type>(<scope>): <中文说明>
```

scope 为可选项，使用英文模块或工程名称；省略时写作 `<type>: <中文说明>`。

| type | 用途 |
| --- | --- |
| `feat` | 新增功能 |
| `fix` | 修复缺陷 |
| `docs` | 文档变更 |
| `refactor` | 保持外部行为的结构调整 |
| `perf` | 性能改进 |
| `style` | 代码排版与格式调整 |
| `test` | 测试相关变更 |
| `build` | 构建或依赖变更 |
| `ci` | 持续集成配置 |
| `chore` | 其他工程维护 |
| `revert` | 撤销已有变更 |

例如：`feat(api): 增加统一异常处理`、`docs: 修正配置说明`、`ci(backend): 接入静态检查`。发生不兼容变更时按规范使用 `!` 或 `BREAKING CHANGE` 说明。

每条提交描述一个可理解的逻辑变更，正文按需解释原因。PR 说明写清改动目的、主要变化和验证方式。

每条开发提交与 PR 标题分别遵循上述格式，中文写作约定在审查时核对。标题自动检查的范围见[持续集成](#持续集成)。

### 日常操作与同步

以下 Git 命令均在项目根目录执行。开始工作前使用 `git status` 核对工作区，切换任务或设备前提交并推送需要接续的改动，进行中的任务可使用 Draft PR。

从主分支开始新任务，以下使用示例分支 `ci/backend-checks`：

```bash
git fetch origin
git switch main
git pull --ff-only
git switch -c ci/backend-checks
```

开发过程中按实际修改路径暂存文件，检查 `git diff --cached` 后提交；首次推送任务分支时使用 `git push -u origin ci/backend-checks`，再到 GitHub 创建目标为 `main` 的 PR。

任务期间需要引入主分支的新提交时，在任务分支上执行：

```bash
git fetch origin
git merge origin/main -m "chore: 同步 main 最新变更"
```

任务分支通过 merge 同步主分支，保留已推送的提交历史。遇到冲突时，解决并检查后完成合并和推送；另一设备已有新提交时，先同步当前任务分支，再引入 `origin/main`。

切换到已有本地分支后，使用 `git pull --ff-only` 同步。首次取得远程任务分支时使用 `git fetch origin`，再执行 `git switch --track origin/ci/backend-checks`。快进同步失败时先检查双方差异，再处理分叉，保留两端需要的提交。

PR 合并后，切回 `main` 并执行 `git pull --ff-only`，使用 `git branch -d <分支名>` 清理本地已合并分支；提示未合并时先核对提交关系。

### 首次入库

此流程适用于本地尚未初始化 Git、远程仓库为空的首次入库。需要配置 Git 提交身份，以及当前设备对应 GitHub 账号的 SSH 认证。

1. 在 GitHub 创建公开空仓库 `0Elaina/yuki`，初始化文件选项保持未勾选。
2. 在 `backend/` 执行[静态检查](#静态检查)，通过后返回项目根目录。
3. 初始化并检查提交范围：

   ```bash
   git init -b main
   git check-ignore -v backend/.env backend/.venv/ backend/.ruff_cache/ backend/.mypy_cache/
   git add .
   git status --short
   git diff --cached --stat
   git diff --cached --check
   ```

   核对忽略规则及暂存文件，提交范围应包含 `backend/.env.example`、`backend/uv.lock`、工程源码、文档及 `.github/workflows/`。

4. 将当前工程状态作为一次初始化提交并推送：

   ```bash
   git commit -m "chore: 初始化 Yuki 工程基础"
   git remote add origin git@github.com:0Elaina/yuki.git
   git push -u origin main
   ```

5. 在 GitHub 设置默认分支为 `main`。Settings → General → Pull Requests 中仅启用 Allow merge commits，合并消息格式选择 Pull request title and description；Squash、Rebase 合并选项和强制分支保护保持关闭。
6. 在 Actions 中确认 `Backend CI` 的 `backend-static` 通过；失败时按日志定位配置、依赖恢复、代码检查或认证问题，修正后重新运行。

推送后可用下列只读命令核对远程、分支跟踪和最新提交；`git rev-parse HEAD` 与远程 `main` 的提交 SHA 应一致：

```bash
git remote -v
git status -sb
git rev-parse HEAD
git ls-remote origin refs/heads/main
```

## 持续集成

两个 workflow 均使用 `ubuntu-24.04`，各任务超时为 10 分钟。同一 workflow 的同一分支或 PR 出现新运行时，取消旧运行。

### 后端静态检查

`.github/workflows/backend-ci.yml` 定义 `Backend CI`，任务名称为 `backend-static`。触发范围为 `main` 的所有推送，以及目标为 `main` 的 PR 的 `opened`、`reopened`、`synchronize` 事件。

使用 uv `0.13.0`，在 `backend/` 根据 `.python-version` 安装 Python 3.12，执行 `uv sync --locked`，再运行[本地静态检查](#静态检查)中的三条命令。uv 缓存以 `backend/uv.lock` 为依据。

workflow 权限为 `contents: read`，运行条件为 Python 和锁文件依赖。

### PR 标题检查

`.github/workflows/pr-title.yml` 定义 `PR Title`，任务名称为 `pr-title`。通过 `pull_request_target` 监听目标为 `main` 的 PR 的 `opened`、`reopened`、`edited`、`synchronize` 事件，修改标题后会重新检查。

使用 `amannn/action-semantic-pull-request` 检查已约定的 Conventional Commits 格式、type 和非空说明，scope 可选，允许中文。权限为 `pull-requests: read`，使用内置 `GITHUB_TOKEN`，执行范围限定为 PR 元数据校验。

Draft PR 与普通 PR 使用相同的标题校验规则。

### Action 版本维护

所有 Action 固定到完整提交 SHA，并在 workflow 中注释对应版本。更新时核对官方发布记录及对应提交。版本依据为：

- [actions/checkout v7.0.1](https://github.com/actions/checkout/releases/tag/v7.0.1)。
- [astral-sh/setup-uv v9.0.0](https://github.com/astral-sh/setup-uv/releases/tag/v9.0.0)。
- [amannn/action-semantic-pull-request v6.1.1](https://github.com/amannn/action-semantic-pull-request/releases/tag/v6.1.1)。

## 开发环境同步

新设备按以下顺序准备开发环境：

1. 安装 Git、uv，并配置 Git 提交身份与 GitHub SSH 认证。
2. 在项目父目录执行 `git clone git@github.com:0Elaina/yuki.git`。
3. 进入项目，按[日常操作与同步](#日常操作与同步)切换到需要接续的任务分支。
4. 在 `backend/` 按[恢复依赖与准备配置](#恢复依赖与准备配置)恢复依赖，配置本机环境变量或 `.env`。
5. 按使用需要分别准备数据库数据和媒体文件，工程文件通过 Git 同步。
