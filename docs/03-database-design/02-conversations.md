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
| 1:N | conversation_turns | conversation_turns.conversation_id | 会话包含的对话轮次集合 |

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

## conversation_turns 表

保存对话中的独立轮次记录，归属特定会话并为消息提供轮次分组与级联锚点。

**字段**

| 字段名 | 类型 | 约束(PK/FK/UNIQUE/NOT NULL/DEFAULT) | 说明（枚举须写全映射） |
| --- | --- | --- | --- |
| id | BIGINT | PK, GENERATED ALWAYS AS IDENTITY | 轮次主键标识 |
| conversation_id | BIGINT | FK, NOT NULL | 所属会话标识，引用 conversations.id，级联删除 |
| created_at | TIMESTAMPTZ | NOT NULL | 创建时间（UTC） |
| updated_at | TIMESTAMPTZ | NOT NULL | 更新时间（UTC） |

**索引**

| 索引名 | 类型 | 字段 | 理由（必须说明具体查询场景） |
| --- | --- | --- | --- |
| pk_conversation_turns | 主键索引 | id | 主键唯一约束与按 ID 定位轮次场景 |
| uq_conversation_turns_conversation_id_id | 唯一约束 | conversation_id, id | 为 messages 表复合外键提供唯一目标键，并支撑按会话定位轮次 |

**关系**

| 关系 | 目标表 | 外键字段 | 说明 |
| --- | --- | --- | --- |
| N:1 | conversations | conversation_id | 轮次所属的会话 |
| 1:N | messages | (conversation_id, turn_id) | 轮次下包含的问答消息记录 |

**建表 SQL**

```sql
CREATE TABLE conversation_turns (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    conversation_id BIGINT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL,
    CONSTRAINT pk_conversation_turns PRIMARY KEY (id),
    CONSTRAINT fk_conversation_turns_conversation_id_conversations FOREIGN KEY (conversation_id) REFERENCES conversations (id) ON DELETE CASCADE,
    CONSTRAINT uq_conversation_turns_conversation_id_id UNIQUE (conversation_id, id)
);
```

## messages 表

保存对话会话中的单条用户提问与助手回复消息记录。

**字段**

| 字段名 | 类型 | 约束(PK/FK/UNIQUE/NOT NULL/DEFAULT) | 说明（枚举须写全映射） |
| --- | --- | --- | --- |
| id | BIGINT | PK, GENERATED ALWAYS AS IDENTITY | 消息主键标识 |
| conversation_id | BIGINT | FK, NOT NULL | 所属会话标识，与 turn_id 共同引用 conversation_turns，级联删除 |
| turn_id | BIGINT | FK, NOT NULL | 所属轮次标识，与 conversation_id 共同引用 conversation_turns，级联删除 |
| role | VARCHAR(32) | NOT NULL | 发送者角色标识，约定为 user 或 assistant（由 DTO 强校验） |
| content | TEXT | NOT NULL | 消息原始文本内容 |
| created_at | TIMESTAMPTZ | NOT NULL | 创建时间（UTC） |
| updated_at | TIMESTAMPTZ | NOT NULL | 更新时间（UTC） |

**索引**

| 索引名 | 类型 | 字段 | 理由（必须说明具体查询场景） |
| --- | --- | --- | --- |
| pk_messages | 主键索引 | id | 主键唯一约束与按 ID 唯一定位消息场景 |
| uq_messages_conversation_id_turn_id_role | 唯一约束 | conversation_id, turn_id, role | 确保同轮次内每角色至多一条消息，同时支撑按会话与轮次读取定位 |
| ix_messages_conversation_id_id | 普通索引 | conversation_id, id | 单会话内按消息 ID 边界条件倒序向前翻页查询历史消息 |

**关系**

| 关系 | 目标表 | 外键字段 | 说明 |
| --- | --- | --- | --- |
| N:1 | conversation_turns | conversation_id, turn_id | 消息所属的对话轮次及归属会话一致性校验 |

**建表 SQL**

```sql
CREATE TABLE messages (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    conversation_id BIGINT NOT NULL,
    turn_id BIGINT NOT NULL,
    role VARCHAR(32) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL,
    CONSTRAINT pk_messages PRIMARY KEY (id),
    CONSTRAINT fk_messages_conversation_id_turn_id_conversation_turns FOREIGN KEY (conversation_id, turn_id) REFERENCES conversation_turns (conversation_id, id) ON DELETE CASCADE,
    CONSTRAINT uq_messages_conversation_id_turn_id_role UNIQUE (conversation_id, turn_id, role)
);

CREATE INDEX ix_messages_conversation_id_id ON messages (conversation_id, id);
```

