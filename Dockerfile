# 使用CUDA基础镜像
FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu20.04

# 设置环境变量
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PATH="/root/miniconda3/bin:${PATH}"

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    wget \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 安装Miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    bash ~/miniconda.sh -b -p /root/miniconda3 && \
    rm ~/miniconda.sh

# 创建项目目录
WORKDIR /app

# 复制项目文件
COPY . .

# 创建并激活conda环境
RUN conda create -n llm_platform python=3.9 -y && \
    conda activate llm_platform && \
    pip install -r requirements.txt

# 设置环境变量
ENV PATH="/root/miniconda3/envs/llm_platform/bin:${PATH}"

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["python", "start.py"] 