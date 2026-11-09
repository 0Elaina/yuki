# 会话模块 API 设计

## POST /api/v1/conversations

创建新会话并返回会话详情。

**请求参数**

| 字段 | 类型 | 位置(body/query/path/header) | 必填 | 说明（枚举须写全映射） |
| --- | --- | --- | --- | --- |
| characterId | string | body | ✅ | 目标角色 ID，正整数十进制字符串 |

**响应示例**

```json
{
  "data": {
    "id": "1",
    "characterId": "1",
    "title": "新会话",
    "createdAt": "2026-11-09T18:00:00Z",
    "updatedAt": "2026-11-09T18:00:00Z"
  },
  "code": "SUCCESS",
  "message": "响应成功"
}
```

**错误码**

| 状态码 | 错误码 |
| --- | --- |
| 404 | CHARACTER_NOT_FOUND |
| 422 | PARAM_VALIDATION_FAILED |
| 500 | INTERNAL_SERVER_ERROR |

