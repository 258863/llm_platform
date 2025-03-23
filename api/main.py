from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import uvicorn
from pathlib import Path
import logging
import os

from core.model_manager import ModelManager
from core.knowledge_base import KnowledgeBase

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="LLM Platform API",
    description="Large Language Model Service Platform API",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化模型管理器和知识库
model_manager = ModelManager()
knowledge_base = KnowledgeBase()

class ChatRequest(BaseModel):
    prompt: str
    model: Optional[str] = None
    max_length: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    use_knowledge_base: Optional[bool] = False

class ChatResponse(BaseModel):
    response: str
    model: str
    knowledge_base_used: bool
    knowledge_base_results: Optional[List[Dict]] = None

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """处理聊天请求"""
    try:
        # 如果启用了知识库，先搜索相关文档
        knowledge_base_results = None
        if request.use_knowledge_base:
            knowledge_base_results = knowledge_base.search(request.prompt)
            if knowledge_base_results:
                # 将知识库结果添加到提示中
                context = "\n".join([r["content"] for r in knowledge_base_results])
                request.prompt = f"Context:\n{context}\n\nQuestion:\n{request.prompt}"
        
        # 生成回复
        response = await model_manager.generate(
            prompt=request.prompt,
            model_name=request.model,
            max_length=request.max_length,
            temperature=request.temperature,
            top_p=request.top_p
        )
        
        return ChatResponse(
            response=response,
            model=request.model or model_manager.config['model']['default'],
            knowledge_base_used=request.use_knowledge_base,
            knowledge_base_results=knowledge_base_results
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/models")
async def get_models():
    """获取可用模型列表"""
    try:
        return model_manager.get_available_models()
    except Exception as e:
        logger.error(f"Error getting models: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/knowledge-base/upload")
async def upload_document(
    file: UploadFile = File(...),
    collection_name: str = "default"
):
    """上传文档到知识库"""
    try:
        # 创建上传目录
        upload_dir = Path("data/uploads")
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        # 保存文件
        file_path = upload_dir / file.filename
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # 添加到知识库
        success = knowledge_base.add_document(
            str(file_path),
            collection_name=collection_name
        )
        
        if not success:
            raise HTTPException(
                status_code=500,
                detail="Failed to add document to knowledge base"
            )
        
        return {"message": "Document uploaded successfully"}
        
    except Exception as e:
        logger.error(f"Error uploading document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/knowledge-base/collections")
async def get_collections():
    """获取知识库集合列表"""
    try:
        return knowledge_base.get_collections()
    except Exception as e:
        logger.error(f"Error getting collections: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/knowledge-base/collections/{collection_name}")
async def delete_collection(collection_name: str):
    """删除知识库集合"""
    try:
        success = knowledge_base.delete_collection(collection_name)
        if not success:
            raise HTTPException(
                status_code=500,
                detail="Failed to delete collection"
            )
        return {"message": "Collection deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting collection: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 