# LLM Platform

基于V100 GPU集群的大语言模型服务平台，支持多种模型部署、知识库集成和可视化界面。

## 功能特性

- 🚀 多模型支持
  - 支持DeepSeek-R1、ChatGLM3等主流大模型
  - 支持模型动态切换
  - 支持模型并行推理

- 📚 知识库集成
  - 支持文档知识库构建
  - 支持向量数据库存储
  - 支持RAG检索增强生成

- 🖥️ 可视化界面
  - Web UI界面
  - GridIO简易界面
  - 终端交互模式

- 🔌 API服务
  - FastAPI RESTful接口
  - WebSocket实时对话
  - API文档自动生成

## 系统要求

### 硬件要求
- GPU: 4x V100 (16GB/32GB)
  - 最低配置: 2x V100 16GB
  - 推荐配置: 4x V100 32GB
  - 支持GPU并行推理
- RAM: 64GB+
  - 最低配置: 64GB
  - 推荐配置: 128GB
  - 用于模型加载和推理
- Storage: 100GB+
  - 最低配置: 100GB SSD
  - 推荐配置: 500GB NVMe SSD
  - 用于存储模型文件、知识库和日志
- Network: 千兆网络
  - 用于模型下载和API访问

### 软件要求
- OS: Linux/Windows
  - Linux: Ubuntu 20.04 LTS或更高版本
  - Windows: Windows 10/11 专业版
- CUDA: 11.8+
- Python: 3.8+
- Docker: 20.10+ (可选)

## 模型规格

### DeepSeek-R1
- 模型大小: 7B/13B/33B参数
- 显存占用:
  - 7B: 约14GB显存
  - 13B: 约26GB显存
  - 33B: 约66GB显存
- 量化版本:
  - 7B-Q4_K_M: 约4GB显存
  - 13B-Q4_K_M: 约8GB显存
  - 33B-Q4_K_M: 约20GB显存
- 下载大小:
  - 7B: 约14GB
  - 13B: 约26GB
  - 33B: 约66GB

### ChatGLM3
- 模型大小: 6B/32B参数
- 显存占用:
  - 6B: 约12GB显存
  - 32B: 约64GB显存
- 量化版本:
  - 6B-Q4_K_M: 约4GB显存
  - 32B-Q4_K_M: 约16GB显存
- 下载大小:
  - 6B: 约12GB
  - 32B: 约64GB

### Qwen
- 模型大小: 7B/14B/72B参数
- 显存占用:
  - 7B: 约14GB显存
  - 14B: 约28GB显存
  - 72B: 约144GB显存
- 量化版本:
  - 7B-Q4_K_M: 约4GB显存
  - 14B-Q4_K_M: 约8GB显存
  - 72B-Q4_K_M: 约32GB显存
- 下载大小:
  - 7B: 约14GB
  - 14B: 约28GB
  - 72B: 约144GB

## 快速开始

### WSL Ubuntu环境配置

1. 安装WSL和Ubuntu
```bash
# Windows PowerShell (管理员)
wsl --install -d Ubuntu

# 设置WSL版本为WSL2
wsl --set-default-version 2
```

2. 配置WSL环境
```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装必要的系统包
sudo apt install -y build-essential git curl wget python3-pip

# 安装CUDA支持
# 访问 https://developer.nvidia.com/cuda-downloads
# 选择 Linux -> x86_64 -> Ubuntu -> 22.04 -> deb (network)
# 按照提示安装CUDA
```

3. 项目设置
```bash
# 在WSL中创建项目目录
mkdir -p ~/projects
cd ~/projects

# 克隆项目到WSL本地目录
git clone https://github.com/yourusername/llm_platform.git

# 或者从Windows复制项目文件到WSL
# 在Windows PowerShell中执行：
wsl --distribution Ubuntu --user yourusername cp -r /mnt/c/Users/YourUsername/Projects/llm_platform/* ~/projects/llm_platform/
```

4. 配置Python环境
```bash
# 进入项目目录
cd ~/projects/llm_platform

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

5. 配置Ollama
```bash
# 安装Ollama
curl https://ollama.ai/install.sh | sh

# 创建模型目录
mkdir -p ~/projects/llm_platform/models/ollama

# 设置OLLAMA_MODELS环境变量
echo 'export OLLAMA_MODELS=~/projects/llm_platform/models/ollama' >> ~/.bashrc
source ~/.bashrc

# 下载模型
ollama pull deepseek-r1
ollama pull chatglm3
ollama pull qwen
```

6. 启动服务
```bash
# 确保在项目目录下
cd ~/projects/llm_platform

# 启动API服务
python api/main.py

# 新开一个终端，启动Web UI
python ui/main.py
```

7. 访问服务
- API文档: http://localhost:8000/docs
- Web UI: http://localhost:8080
- GridIO: http://localhost:8081

### 注意事项
1. WSL2性能优化
```bash
# 在Windows中创建或编辑 %UserProfile%\.wslconfig 文件
[wsl2]
memory=16GB
processors=8
localhostForwarding=true
```

2. 文件同步
- 建议在WSL中直接开发，而不是在Windows中开发
- 如果需要同步代码，可以使用git进行版本控制
- 或者使用VSCode的Remote-WSL扩展，直接在WSL中编辑代码

3. 端口转发
- WSL2默认支持端口转发，无需额外配置
- 如果无法访问，检查Windows防火墙设置

4. GPU支持
- 确保Windows已安装NVIDIA驱动
- 在WSL中安装CUDA工具包
- 验证GPU可用性：
```bash
nvidia-smi
```

5. 开发建议
- 使用VSCode + Remote-WSL扩展进行开发
- 在WSL中直接运行和测试代码
- 避免在Windows和WSL之间频繁切换
- 使用git进行代码版本控制

### 其他环境配置

1. 安装依赖
```bash
pip install -r requirements.txt
```

2. 配置环境
```bash
cp config/config.example.yaml config/config.yaml
# 编辑 config.yaml 配置文件
```

3. 启动服务
```bash
# 启动API服务
python api/main.py

# 启动Web UI
python ui/main.py

# 启动GridIO界面
python ui/gridio_app.py
```

4. 访问服务
- API文档: http://localhost:8000/docs
- Web UI: http://localhost:8080
- GridIO: http://localhost:8081

## 详细部署指南

### 1. 模型部署

#### 1.1 下载模型
```bash
# 方式1：使用Ollama（推荐）
# 1. 创建模型目录
mkdir -p models/ollama

# 2. 安装Ollama并指定模型目录
# Linux
curl https://ollama.ai/install.sh | sh
# 设置OLLAMA_MODELS环境变量
export OLLAMA_MODELS=models/ollama
# 添加到.bashrc或.zshrc
echo 'export OLLAMA_MODELS=models/ollama' >> ~/.bashrc

# Windows
# 下载安装包：https://ollama.ai/download
# 设置环境变量 OLLAMA_MODELS=C:\path\to\models\ollama

# 3. 下载模型到指定目录
ollama pull deepseek-r1
ollama pull chatglm3
ollama pull qwen

# 4. 验证模型位置
ls models/ollama
# 应该能看到类似这样的目录结构：
# models/ollama/
# ├── deepseek-r1/
# ├── chatglm3/
# └── qwen/

# 方式2：使用huggingface-cli
# 创建模型目录
mkdir -p models/deepseek-r1
mkdir -p models/chatglm3
mkdir -p models/qwen

# 下载DeepSeek-R1模型
huggingface-cli download deepseek-ai/deepseek-r1 --local-dir models/deepseek-r1

# 下载ChatGLM3模型
git clone https://huggingface.co/THUDM/chatglm3-6b models/chatglm3

# 下载Qwen模型
git clone https://huggingface.co/Qwen/Qwen-7B models/qwen
```

#### 1.2 模型配置
在 `config/config.yaml` 中配置模型路径：
```yaml
models:
  deepseek-r1:
    path: "models/ollama/deepseek-r1"  # 指定Ollama模型路径
    type: "deepseek"
    max_length: 2048
    temperature: 0.7
  chatglm3:
    path: "models/ollama/chatglm3"  # 指定Ollama模型路径
    type: "chatglm"
    max_length: 2048
    temperature: 0.7
  qwen:
    path: "models/ollama/qwen"  # 指定Ollama模型路径
    type: "qwen"
    max_length: 2048
    temperature: 0.7
```

### 2. 数据库配置

#### 2.1 向量数据库
```bash
# 创建向量数据库目录
mkdir -p data/vector_db

# 配置向量数据库路径
# 在 config/config.yaml 中设置：
vector_db:
  path: "data/vector_db"
  collection: "documents"
```

#### 2.2 文档存储
```bash
# 创建文档存储目录
mkdir -p data/documents

# 支持的文档格式：
# - PDF: data/documents/pdf/
# - Word: data/documents/word/
# - Markdown: data/documents/markdown/
# - HTML: data/documents/html/
```

### 3. 日志配置

```bash
# 创建日志目录
mkdir -p logs

# 在 config/config.yaml 中配置日志：
logging:
  level: "INFO"
  file: "logs/app.log"
  max_size: 100  # MB
  backup_count: 10
```

### 4. 环境变量配置

创建 `.env` 文件：
```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件
# 设置必要的环境变量
MODEL_PATH=models
VECTOR_DB_PATH=data/vector_db
DOC_PATH=data/documents
LOG_PATH=logs
```

## 系统架构

```mermaid
graph TB
    %% 定义样式
    classDef client fill:#e3f2fd,stroke:#1976d2,stroke-width:2px,color:#0d47a1,rx:10,ry:10;
    classDef server fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px,color:#4a148c,rx:10,ry:10;
    classDef model fill:#e8f5e9,stroke:#388e3c,stroke-width:2px,color:#1b5e20,rx:10,ry:10;
    classDef kb fill:#fff3e0,stroke:#f57c00,stroke-width:2px,color:#e65100,rx:10,ry:10;
    classDef storage fill:#fce4ec,stroke:#c2185b,stroke-width:2px,color:#880e4f,rx:10,ry:10;

    %% 定义连接线样式
    linkStyle default stroke:#616161,stroke-width:2px,stroke-dasharray: 5 5;

    subgraph Client["客户端层"]
        direction TB
        A[Web UI]:::client --> |HTTP/WebSocket| API
        B[GridIO UI]:::client --> |HTTP/WebSocket| API
        C[CLI]:::client --> |HTTP| API
    end

    subgraph Server["服务器层"]
        direction TB
        API[API Service]:::server --> |请求处理| Core
        Core[Core Service]:::server --> |模型调用| Models
        Core --> |知识检索| KB[Knowledge Base]
        
        subgraph Models["模型服务"]
            direction LR
            M1[DeepSeek-R1]:::model
            M2[ChatGLM3]:::model
            M3[Qwen]:::model
        end
        
        subgraph KB["知识库"]
            direction LR
            V1[向量数据库]:::kb
            V2[文档存储]:::kb
            V1 --> |Embedding| V2
        end
    end

    subgraph Storage["存储层"]
        direction LR
        D1[(模型文件)]:::storage
        D2[(配置文件)]:::storage
        D3[(日志文件)]:::storage
    end

    Models --> D1
    Core --> D2
    API --> D3

    %% 添加特殊连接线样式
    linkStyle 0,1,2,3,4,5,6,7,8,9,10,11 stroke:#616161,stroke-width:2px;
```

## 项目结构

```
llm_platform/
├── api/            # FastAPI接口服务
├── core/           # 核心功能实现
├── ui/             # 可视化界面
├── utils/          # 工具函数
├── docs/           # 文档
├── models/         # 模型文件
├── data/           # 数据文件
└── config/         # 配置文件
```

## 使用说明

### 1. 模型部署

支持以下模型：
- DeepSeek-R1 (7B/13B/33B)
- ChatGLM3 (6B/32B)
- Qwen (7B/14B/72B)

### 2. 知识库功能

支持多种文档格式：
- PDF
- Word
- Markdown
- HTML

### 3. API调用

```python
import requests

# 对话接口
response = requests.post(
    "http://localhost:8000/api/chat",
    json={
        "message": "你好",
        "model": "deepseek-r1",
        "use_knowledge": True
    }
)
```

### 4. 界面使用

- Web UI: 提供完整的对话和知识库管理界面
- GridIO: 提供简单的对话界面
- 终端: 支持命令行交互

## 开发计划

- [ ] 支持更多模型
- [ ] 优化推理性能
- [ ] 添加更多知识库格式
- [ ] 改进用户界面
- [ ] 添加监控功能

## 贡献指南

欢迎提交Issue和Pull Request！

## 许可证

MIT License 

```mermaid
graph TB
    %% 定义样式
    classDef start fill:#e3f2fd,stroke:#1976d2,stroke-width:2px,color:#0d47a1,rx:10,ry:10;
    classDef process fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px,color:#4a148c,rx:10,ry:10;
    classDef decision fill:#e8f5e9,stroke:#388e3c,stroke-width:2px,color:#1b5e20,rx:10,ry:10;
    classDef end fill:#fce4ec,stroke:#c2185b,stroke-width:2px,color:#880e4f,rx:10,ry:10;

    %% 开始
    Start[项目启动]:::start
    
    %% 环境配置
    Env[环境配置]:::process
    Start --> Env
    
    %% 模型部署
    Model[模型部署]:::process
    Env --> Model
    
    %% 知识库构建
    KB[知识库构建]:::process
    Model --> KB
    
    %% 界面开发
    UI[界面开发]:::process
    KB --> UI
    
    %% API开发
    API[API开发]:::process
    UI --> API
    
    %% 测试
    Test{测试}:::decision
    API --> Test
    
    %% 测试结果判断
    Test -->|通过| Deploy[部署]:::end
    Test -->|不通过| Fix[修复]:::process
    Fix --> API
    
    %% 连接线样式
    linkStyle default stroke:#616161,stroke-width:2px;
```

## 项目结构 