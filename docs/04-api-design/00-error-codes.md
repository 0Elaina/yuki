# 全局业务码

ApiCode 是不可变数据类，保存 HTTP 状态、字符串业务码与默认消息。CommonApiCode 保存以下公共常量；业务模块可以创建自己的 ApiCode。

| HTTP 状态 | 业务码 | 默认消息 |
| --- | --- | --- |
| 200 | SUCCESS | 响应成功 |
| 400 | BAD_REQUEST | 请求参数有误 |
| 404 | NOT_FOUND | 请求的资源不存在 |
| 405 | METHOD_NOT_ALLOWED | HTTP 请求方法不支持 |
| 409 | CONFLICT | 资源状态冲突 |
| 413 | UPLOAD_TOO_LARGE | 上传文件或请求过大 |
| 415 | UNSUPPORTED_MEDIA_TYPE | 请求内容类型不支持 |
| 422 | PARAM_VALIDATION_FAILED | 参数校验未通过 |
| 429 | TOO_MANY_REQUESTS | 请求过于频繁，请稍后重试 |
| 500 | INTERNAL_SERVER_ERROR | 系统内部异常，请稍后重试 |
| 503 | SERVICE_UNAVAILABLE | 服务暂不可用，请稍后重试 |

### 角色模块业务码

| HTTP 状态 | 业务码 | 默认消息 |
| --- | --- | --- |
| 404 | CHARACTER_NOT_FOUND | 角色不存在 |

参数校验失败使用固定默认消息。业务异常可提供公开的自定义消息；未知异常返回固定 INTERNAL_SERVER_ERROR，堆栈由 Uvicorn 记录。

业务码提供公共响应语义，具体接口使用的错误码见对应模块文档。响应结构见[公共 API 契约](00-common-api.md)。
