# AI 设计

## 模型接入

LLM、Embedding、语音识别和语音合成通过独立服务 API 接入，支持本地部署和云端服务。推理与 Web 后端进程分离，同一服务可以提供多种能力。

LangChain 复用模型、消息、Embedding 和检索集成；LangGraph 组织需要明确步骤与状态的对话流程。图节点调用业务服务，普通配置 CRUD 留在对应模块。参考[官方职责说明](https://www.langchain.com/oss-overview)。

## 对话协作

chat 模块负责一次对话的协调：

1. 取得当前角色的人设、会话上下文和服务配置。
2. 从 memory 召回该角色的相关长期记忆，从 knowledge 检索该角色关联的背景资料。
3. 组合上下文并调用 LLM，由 conversations 维护用户可见的输入与回复记录。
4. 需要语音输出时调用语音合成服务，由前端协调回复文字、音频与 Live2D 表现。

语音输入先由识别服务转换为文字，再进入对话流程。模型服务凭据由后端读取和使用，保存方式见[工程指南](05-engineering-guide.md)。

## 数据与执行状态

| 数据 | 用途 | 管理方式 |
| --- | --- | --- |
| 会话与消息记录 | 查看历史、继续对话和管理会话 | conversations 在 PostgreSQL 维护业务记录 |
| LangGraph 检查点 | 保存工作流步骤、执行状态与线程内连续性 | 使用框架支持的 PostgreSQL 持久化组件 |
| 长期记忆 | 跨会话保留角色互动信息 | memory 管理来源内容与业务元数据，Qdrant 提供语义索引 |
| 背景与世界观资料 | 提供独立于对话生成过程的设定依据 | knowledge 管理来源内容及角色引用，Qdrant 提供语义索引 |

图线程与业务会话建立明确关联，界面历史由业务会话记录提供，检查点服务于执行状态。复用框架持久化组件，避免另外实现检查点框架。参考 [LangGraph 记忆](https://docs.langchain.com/oss/python/concepts/memory)和[持久化说明](https://docs.langchain.com/oss/python/langgraph/persistence)。

## 记忆与背景检索

长期记忆默认按角色隔离；背景与世界观资料独立管理，允许多个角色引用。记忆保留互动来源，模型归纳出的内容不自动成为背景设定。

检索在当前角色允许的范围内执行：记忆限定角色，背景资料限定角色关联。范围约束进入检索查询，不依赖 Prompt 排除其他角色内容。Qdrant 的筛选能力参考[官方实践](https://qdrant.tech/documentation/search-patterns/vector-search-filtering/)。

PostgreSQL 管理来源与业务关联，Qdrant 保存向量和必要检索元数据；资源型原文可由 assets 保存到 RustFS。来源内容保留以支持重建索引，来源修改或删除时同步维护索引。

Embedding 服务负责文本向量化。索引使用与向量模型兼容的维度，模型变化时重建对应索引，避免混用不兼容的向量。

## Prompt 与角色表现

Prompt 由 chat 集中组装，区分应用指令、角色设定、会话内容、长期记忆和背景资料。

回复文字与表现控制信息分别解释。模型产生的表现意图经过校验后，由前端映射到当前 Live2D 模型支持的表情和动作。

## 语音与 Live2D

前端负责录音、音频播放与角色渲染，运行时以 [Live2D Cubism Web SDK](https://docs.live2d.com/en/cubism-sdk-manual/cubism-sdk-for-web/) 的模型兼容能力为基准。口型、表情和动作复用官方 SDK 或经过兼容性核实的成熟封装。

切换角色或会话时，停止旧音频与表现，旧执行结果不能进入新对话。离开界面时释放播放器和角色运行时资源。

文字生成、语音合成和资源加载分别反馈结果；语音失败时保留已生成文字，并明确反馈音频失败。同类集成经验参考 [Open-LLM-VTuber](https://github.com/Open-LLM-VTuber/Open-LLM-VTuber)。
