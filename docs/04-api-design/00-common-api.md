# 公共 API 契约

## JSON 响应

普通 JSON 接口使用 ApiResponse 泛型返回类型标注，由 FastAPI 推导响应模型；需要覆盖推导结果时再显式设置 response_model。接口错误码在对应模块的 API 文档中维护，路由不逐项重复声明错误响应。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| data | 接口定义的数据或 null | 无数据成功和错误响应为 null |
| code | string | 稳定业务码，成功为 SUCCESS |
| message | string | 默认中文消息或可公开的业务提示 |

```json
{
  "data": null,
  "code": "SUCCESS",
  "message": "响应成功"
}
```

成功使用 ApiResponse.success(data)，错误由异常处理器使用 ApiResponse.error(api_code, message) 构造。未提供 message 时采用业务码的默认消息。

Python 字段使用 snake_case，接口中的多词字段使用 Pydantic 别名输出 camelCase。时间使用带时区的 ISO 8601 字符串，统一 UTC。流式和二进制响应采用各自协议。

## 校验与异常

BusinessException 携带 ApiCode 和可选的公开消息，处理器按业务码返回 HTTP 状态及统一响应。业务码定义见[全局业务码](00-error-codes.md)。

RequestValidationError 固定返回 HTTP 422：

```json
{
  "data": null,
  "code": "PARAM_VALIDATION_FAILED",
  "message": "参数校验未通过"
}
```

框架 HTTPException 按公共 HTTP 状态映射业务码，并保留 Allow 等响应头；未登记状态返回固定 500。响应模型校验错误及其他未知异常也返回固定 500、INTERNAL_SERVER_ERROR，异常堆栈由 Uvicorn 记录。

OpenAPI 的公共 422、500 响应声明使用相同的 ApiResponse 结构。实现采用 [FastAPI 异常处理器](https://fastapi.tiangolo.com/tutorial/handling-errors/)。

## 分页

直接使用 fastapi-pagination 的 Page、Params 和 SQLAlchemy 异步 apaginate。PageQuery 仅继承 Params 调整每页默认条数，不提供额外分页执行函数。

| 查询参数 | 类型 | 默认值 | 约束 |
| --- | --- | --- | --- |
| page | int | 1 | 最小 1 |
| size | int | 20 | 1 至 100 |

分页结果使用原生 Page[T]，作为 ApiResponse 的 data：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| items | array | 当前页数据 |
| total | int | 查询结果总数 |
| page | int | 请求页码 |
| size | int | 每页条数 |
| pages | int | 总页数 |

调用 apaginate 时传入已有 session、明确排序的 Select 和 PageQuery；嵌套在 ApiResponse 中时，通过库原生 Config(page_cls=Page[模型]) 显式指定结果类型。当数据访问层查询 ORM 时返回 Page[ORM]；业务层在事务内将其 items 转换为 Page[输出模型]，复用原始分页元数据返回。输出模型按需启用 Pydantic 的 from_attributes，业务模块负责具体的数据转换。

业务层在 session.begin() 内执行查询；分页不另建会话或管理事务。计数使用库原生能力，需要专用计数时传入 count_query。参考[官方 SQLAlchemy 集成](https://uriyyo-fastapi-pagination.netlify.app/integrations/sqlalchemy/paginate/)。

### 分页模式适用边界

- **页码分页（`Page[T]` + `PageQuery`）**：适用于需要展示总数及随机跳页的列表查询，用于角色列表（`GET /api/v1/characters`）与会话列表（`GET /api/v1/conversations`）。
- **单向 ID 游标分页（`beforeId` + `nextBeforeId`）**：适用于持续追加写入、按主键倒序单向向上翻页的场景，用于会话历史消息（`GET /api/v1/conversations/{conversation_id}/messages`），避免新消息写入导致传统页码偏移。
