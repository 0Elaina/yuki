# Yuki 前端

Yuki 的单一 Vue 3 Web 应用，提供聊天、角色与应用设置界面。技术栈为 TypeScript、Vue 3、Vite、Vue Router、Pinia、Naive UI。

## 环境要求

- Node.js `^22.18.0` 或 `>=24.12.0`
- pnpm，版本由 `package.json` 的 `packageManager` 字段固定

```sh
pnpm install
pnpm dev
```

## 常用命令

| 命令                | 用途                                |
| ------------------- | ----------------------------------- |
| `pnpm dev`          | 启动开发服务器                      |
| `pnpm build`        | 类型检查后构建到 `dist/`            |
| `pnpm type-check`   | `vue-tsc` 类型检查                  |
| `pnpm lint`         | oxlint 与 ESLint 只检查，不修改文件 |
| `pnpm lint:fix`     | oxlint 与 ESLint 检查并自动修复     |
| `pnpm format`       | Prettier 格式化并写入               |
| `pnpm format:check` | Prettier 只检查格式                 |
| `pnpm check`        | 类型检查、lint 与格式检查并行执行   |

`pnpm lint` 与 `pnpm format:check` 不修改文件，供 CI 复用；本地改代码用对应的 `:fix` 与 `format`。

## 目录约定

| 目录           | 职责                                                     |
| -------------- | -------------------------------------------------------- |
| `src/app`      | 应用初始化、路由、布局、主题与全局 Provider              |
| `src/pages`    | 页面入口与功能组合                                       |
| `src/features` | 按角色、聊天、资源、设置等功能组织组件、请求、状态与类型 |
| `src/shared`   | 公共 HTTP 能力、通用组件与稳定工具                       |

依赖方向为 `app → pages → features → shared`，下层不反向引用上层。
