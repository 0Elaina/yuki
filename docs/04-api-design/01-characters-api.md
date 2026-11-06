# 角色模块 API 设计

## POST /api/v1/characters

创建新角色并返回角色详情。

**请求参数**

| 字段 | 类型 | 位置(body/query/path/header) | 必填 | 说明（枚举须写全映射） |
| --- | --- | --- | --- | --- |
| name | string | body | ✅ | 角色名称，去除首尾空白后 1～100 字符 |
| persona | string | body | ❌ | 角色人设，上限 20000 字符，默认空字符串 |

**响应示例**

```json
{
  "data": {
    "id": "1",
    "name": "雪",
    "persona": "",
    "createdAt": "2026-11-06T08:00:00Z",
    "updatedAt": "2026-11-06T08:00:00Z"
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

## GET /api/v1/characters

分页查询角色列表，支持按名称子串不区分大小写模糊匹配。

**请求参数**

| 字段 | 类型 | 位置(body/query/path/header) | 必填 | 说明（枚举须写全映射） |
| --- | --- | --- | --- | --- |
| page | int | query | ❌ | 页码，默认 1，最小 1 |
| size | int | query | ❌ | 每页条数，默认 20，1 至 100 |
| keyword | string | query | ❌ | 角色名称搜索关键词，去除首尾空白后上限 100 字符，默认空字符串 |

**响应示例**

```json
{
  "data": {
    "items": [
      {
        "id": "1",
        "name": "雪",
        "createdAt": "2026-11-06T08:00:00Z",
        "updatedAt": "2026-11-06T08:00:00Z"
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

## GET /api/v1/characters/{character_id}

根据角色 ID 查询单个角色的完整资料。

**请求参数**

| 字段 | 类型 | 位置(body/query/path/header) | 必填 | 说明（枚举须写全映射） |
| --- | --- | --- | --- | --- |
| character_id | int | path | ✅ | 角色 ID，大于 0 且不超过 2^63 - 1 |

**响应示例**

```json
{
  "data": {
    "id": "1",
    "name": "雪",
    "persona": "",
    "createdAt": "2026-11-06T08:00:00Z",
    "updatedAt": "2026-11-06T08:00:00Z"
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
