# 公共响应与错误码

## 响应正文

业务接口使用 `ApiResponse[T]`，正文始终包含以下三个必填字段。HTTP 状态表达协议结果，客户端结合 HTTP 状态与 `code` 判断处理结果。

| 字段 | 类型 | 含义 |
| --- | --- | --- |
| `code` | `str` | 成功为 `SUCCESS`；错误使用全大写字母、下划线分隔的业务码 |
| `message` | `str` | 面向人的说明；公共提示使用中文，成功提示为“响应成功” |
| `data` | `T` | 成功时为业务数据，普通错误为 `null`，请求校验错误为字段错误详情 |

普通错误响应示例（HTTP 404）：

```json
{
  "code": "MISSING_RESOURCE",
  "message": "资源不存在",
  "data": null
}
```

## 请求校验错误

请求参数校验失败时返回 HTTP 422，正文示例：

```json
{
  "code": "INVALID_REQUEST",
  "message": "请求参数无效",
  "data": {
    "errors": [
      {
        "loc": ["body", "name"],
        "type": "missing",
        "message": "Field required"
      }
    ]
  }
}
```

`data` 对应 `ValidationErrorData`，`errors` 中每项对应 `ValidationErrorItem`，公开字段限定如下：

| 字段 | 类型 | 含义 |
| --- | --- | --- |
| `loc` | `list[str \| int]` | 保留请求位置、嵌套字段和数组索引，例如 `["body", "tracks", 0, "title"]` |
| `type` | `str` | Pydantic 提供的错误类型 |
| `message` | `str` | Pydantic 原始错误说明，可能为英文 |

## 全局错误码

| HTTP 状态 | 错误码 | 公共提示 | 触发条件 |
| --- | --- | --- | --- |
| 422 | `INVALID_REQUEST` | 请求参数无效 | FastAPI 请求参数校验失败，`data.errors` 返回字段错误列表 |
| 404 | `MISSING_RESOURCE` | 资源不存在 | 框架抛出 404 HTTP 异常，包括路径不存在 |
| 405 | `UNSUPPORTED_METHOD` | 请求方法不受支持 | 框架抛出 405 HTTP 异常 |
| 原 HTTP 状态 | `HTTP_ERROR` | 请求处理失败 | 除 404、405 外的框架 HTTP 异常 |
| 500 | `INTERNAL_ERROR` | 服务器内部错误 | 未捕获的程序异常，包括响应模型校验失败；堆栈记录到日志，正文使用通用提示 |

业务异常按其声明的 HTTP 状态、业务码和公开提示返回，`data` 为 `null`。业务码以动词或形容词加名词命名，随对应模块归档。

## 响应头与接口描述

每次 HTTP 请求由服务端生成请求 ID，通过 `X-Request-ID` 响应头返回，用于关联请求日志和异常日志。框架 HTTP 异常保留原有响应头，例如 `Allow`、`WWW-Authenticate`。

业务路由统一挂载到 `/api/v1`。聚合入口为业务接口声明公共 422、500 错误模型；各接口声明自己的成功响应模型和业务错误响应。Swagger 与 OpenAPI 使用 FastAPI 默认结构。

接口接入方式见[工程指南](../05-engineering-guide.md#接口接入)。
