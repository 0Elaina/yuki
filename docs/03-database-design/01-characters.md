# 角色数据表设计

## characters 表

保存系统的角色基础身份与人设信息。

**字段**

| 字段名 | 类型 | 约束(PK/FK/UNIQUE/NOT NULL/DEFAULT) | 说明（枚举须写全映射） |
| --- | --- | --- | --- |
| id | BIGINT | PK, GENERATED ALWAYS AS IDENTITY | 角色主键标识 |
| name | VARCHAR(128) | NOT NULL | 角色名称，支持同名 |
| persona | TEXT | NOT NULL | 角色人设描述，允许空文本 |
| created_at | TIMESTAMPTZ | NOT NULL | 创建时间（UTC） |
| updated_at | TIMESTAMPTZ | NOT NULL | 更新时间（UTC） |

**索引**

| 索引名 | 类型 | 字段 | 理由（必须说明具体查询场景） |
| --- | --- | --- | --- |
| pk_characters | 主键索引 | id | 主键唯一约束与按 ID 唯一定位角色场景 |

**关系**

| 关系 | 目标表 | 外键字段 | 说明 |
| --- | --- | --- | --- |
| 无 | 无 | 无 | 当前为单表独立实体，暂无外键关联 |

**建表 SQL**

```sql
CREATE TABLE characters (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(128) NOT NULL,
    persona TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL,
    CONSTRAINT pk_characters PRIMARY KEY (id)
);
```

