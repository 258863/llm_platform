# 系统架构

## 整体架构

```mermaid
graph TB
    subgraph Frontend
        A[Web UI] --> D[API Gateway]
        B[GridIO UI] --> D
        C[Terminal CLI] --> D
    end

    subgraph Backend
        D --> E[FastAPI Service]
        E --> F[Model Manager]
        E --> G[Knowledge Base]
        E --> H[Task Queue]
    end

    subgraph Models
        F --> I[DeepSeek-R1]
        F --> J[ChatGLM3]
        F --> K[Qwen]
    end

    subgraph Knowledge
        G --> L[Vector DB]
        G --> M[Document Store]
    end

    subgraph Hardware
        N[V100 GPU 1]
        O[V100 GPU 2]
        P[V100 GPU 3]
        Q[V100 GPU 4]
    end

    F --> N
    F --> O
    F --> P
    F --> Q
```

## 数据流图

```mermaid
sequenceDiagram
    participant User
    participant UI
    participant API
    participant Model
    participant KB
    participant GPU

    User->>UI: 发送请求
    UI->>API: HTTP/WebSocket
    API->>Model: 模型调用
    Model->>GPU: 推理请求
    GPU-->>Model: 推理结果
    Model->>KB: 知识库查询(可选)
    KB-->>Model: 知识库结果
    Model-->>API: 生成结果
    API-->>UI: 返回结果
    UI-->>User: 显示结果
```

## 组件说明

### 1. 前端组件
- Web UI: 基于Vue.js的完整界面
- GridIO UI: 基于GridIO的简易界面
- Terminal CLI: 命令行交互工具

### 2. 后端服务
- FastAPI Service: RESTful API服务
- Model Manager: 模型管理和调度
- Knowledge Base: 知识库管理
- Task Queue: 任务队列管理

### 3. 模型支持
- DeepSeek-R1: 7B/13B/33B版本
- ChatGLM3: 6B/32B版本
- Qwen: 7B/14B/72B版本

### 4. 知识库组件
- Vector DB: 向量数据库
- Document Store: 文档存储

### 5. 硬件资源
- 4x V100 GPU: 用于模型推理 