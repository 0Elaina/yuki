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

## GET /api/v1/conversations

按角色 ID 分页查询会话列表，较新更新的排在前面。

**请求参数**

| 字段 | 类型 | 位置(body/query/path/header) | 必填 | 说明（枚举须写全映射） |
| --- | --- | --- | --- | --- |
| characterId | string | query | ✅ | 目标角色 ID，正整数十进制字符串 |
| page | int | query | ❌ | 页码，默认 1，最小 1 |
| size | int | query | ❌ | 每页条数，默认 20，1 至 100 |

**响应示例**

```json
{
  "data": {
    "items": [
      {
        "id": "1",
        "characterId": "1",
        "title": "新会话",
        "createdAt": "2026-11-09T18:00:00Z",
        "updatedAt": "2026-11-09T18:00:00Z"
      }
    ],
    "total": 1,
    "page": 1,
    "size": 20,
    "pages": 1
  },
  "code": "SUCCESS",
  "message": "响应成功"
}
```

**错误码**

| 状态码 | 错误码 |
| --- | --- |
| 422 | PARAM_VALIDATION_FAILED |
| 500 | INTERNAL_SERVER_ERROR |

## GET /api/v1/conversations/{conversation_id}

根据会话 ID 查询单个会话的完整详情。

**请求参数**

| 字段 | 类型 | 位置(body/query/path/header) | 必填 | 说明（枚举须写全映射） |
| --- | --- | --- | --- | --- |
| conversation_id | int | path | ✅ | 会话 ID，范围 1 至 2^63 - 1 |

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
| 404 | CONVERSATION_NOT_FOUND |
| 422 | PARAM_VALIDATION_FAILED |
| 500 | INTERNAL_SERVER_ERROR |

## POST /api/v1/conversations/batch-delete

批量删除会话，允许包含不同角色的会话；任一指定会话不存在时整批回滚，不产生局部删除。

**请求参数**

| 字段 | 类型 | 位置(body/query/path/header) | 必填 | 说明（枚举须写全映射） |
| --- | --- | --- | --- | --- |
| ids | array<string> | body | ✅ | 待删除的会话 ID 数组，1～100 项，按解析后的整数判重不可重复，每项为十进制数字字符串 |

**响应示例**

```json
{
  "data": 2,
  "code": "SUCCESS",
  "message": "响应成功"
}
```

**错误码**

| 状态码 | 错误码 |
| --- | --- |
| 404 | CONVERSATION_NOT_FOUND |
| 422 | PARAM_VALIDATION_FAILED |
| 500 | INTERNAL_SERVER_ERROR |

## DELETE /api/v1/conversations/{conversation_id}

根据会话 ID 删除单个会话。

**请求参数**

| 字段 | 类型 | 位置(body/query/path/header) | 必填 | 说明（枚举须写全映射） |
| --- | --- | --- | --- | --- |
| conversation_id | int | path | ✅ | 会话 ID，大于 0 且不超过 2^63 - 1 |

**响应示例**

```json
{
  "data": null,
  "code": "SUCCESS",
  "message": "响应成功"
}
```

**错误码**

| 状态码 | 错误码 |
| --- | --- |
| 404 | CONVERSATION_NOT_FOUND |
| 422 | PARAM_VALIDATION_FAILED |
| 500 | INTERNAL_SERVER_ERROR |

