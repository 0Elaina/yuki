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

