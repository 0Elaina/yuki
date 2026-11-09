# 会话数据表设计

## conversations 表

保存系统中的对话会话基础信息及与角色的归属关联。

**字段**

| 字段名 | 类型 | 约束(PK/FK/UNIQUE/NOT NULL/DEFAULT) | 说明（枚举须写全映射） |
| --- | --- | --- | --- |
| id | BIGINT | PK, GENERATED ALWAYS AS IDENTITY | 会话主键标识 |
| character_id | BIGINT | FK, NOT NULL | 关联角色标识，引用 characters.id，级联删除 |
| title | VARCHAR(64) | NOT NULL | 会话标题 |
| created_at | TIMESTAMPTZ | NOT NULL | 创建时间（UTC） |
| updated_at | TIMESTAMPTZ | NOT NULL | 更新时间（UTC） |

**索引**

| 索引名 | 类型 | 字段 | 理由（必须说明具体查询场景） |
| --- | --- | --- | --- |
| pk_conversations | 主键索引 | id | 主键唯一约束与按 ID 唯一定位会话场景 |
| ix_conversations_character_id_updated_at_id | 普通索引 | character_id, updated_at, id | 按角色筛选会话列表，并支持按更新时间与 ID 倒序读取会话分页及级联删除定位 |

**关系**

| 关系 | 目标表 | 外键字段 | 说明 |
| --- | --- | --- | --- |
| N:1 | characters | character_id | 会话所属的角色 |

**建表 SQL**

```sql
CREATE TABLE conversations (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    character_id BIGINT NOT NULL,
    title VARCHAR(64) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL,
    CONSTRAINT pk_conversations PRIMARY KEY (id),
    CONSTRAINT fk_conversations_character_id_characters FOREIGN KEY (character_id) REFERENCES characters (id) ON DELETE CASCADE
);

CREATE INDEX ix_conversations_character_id_updated_at_id ON conversations (character_id, updated_at, id);
```

