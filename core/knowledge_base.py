import os
import yaml
from typing import List, Optional, Dict
import chromadb
from chromadb.config import Settings
from langchain.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    UnstructuredMarkdownLoader,
    UnstructuredHTMLLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
import logging

class KnowledgeBase:
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config = self._load_config(config_path)
        self.vector_db = None
        self._init_vector_db()
        
    def _load_config(self, config_path: str) -> dict:
        """加载配置文件"""
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def _init_vector_db(self):
        """初始化向量数据库"""
        if not self.config['knowledge_base']['enabled']:
            return
            
        try:
            self.vector_db = chromadb.PersistentClient(
                path=self.config['knowledge_base']['vector_db']['path'],
                settings=Settings(
                    anonymized_telemetry=False
                )
            )
            logging.info("Successfully initialized vector database")
        except Exception as e:
            logging.error(f"Error initializing vector database: {str(e)}")
            raise
    
    def _get_document_loader(self, file_path: str):
        """根据文件类型获取对应的文档加载器"""
        file_ext = os.path.splitext(file_path)[1].lower()
        
        loaders = {
            '.pdf': PyPDFLoader,
            '.docx': Docx2txtLoader,
            '.md': UnstructuredMarkdownLoader,
            '.html': UnstructuredHTMLLoader
        }
        
        if file_ext not in loaders:
            raise ValueError(f"Unsupported file type: {file_ext}")
            
        return loaders[file_ext](file_path)
    
    def add_document(self, file_path: str, collection_name: str = "default") -> bool:
        """添加文档到知识库"""
        if not self.vector_db:
            logging.error("Vector database not initialized")
            return False
            
        try:
            # 加载文档
            loader = self._get_document_loader(file_path)
            documents = loader.load()
            
            # 分割文档
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            texts = text_splitter.split_documents(documents)
            
            # 获取或创建集合
            collection = self.vector_db.get_or_create_collection(collection_name)
            
            # 添加文档到向量数据库
            for i, text in enumerate(texts):
                collection.add(
                    documents=[text.page_content],
                    metadatas=[{
                        "source": file_path,
                        "chunk": i,
                        "page": text.metadata.get("page", 0)
                    }],
                    ids=[f"{os.path.basename(file_path)}_{i}"]
                )
            
            logging.info(f"Successfully added document: {file_path}")
            return True
            
        except Exception as e:
            logging.error(f"Error adding document {file_path}: {str(e)}")
            return False
    
    def search(
        self,
        query: str,
        collection_name: str = "default",
        n_results: int = 5
    ) -> List[Dict]:
        """搜索相关文档"""
        if not self.vector_db:
            logging.error("Vector database not initialized")
            return []
            
        try:
            collection = self.vector_db.get_collection(collection_name)
            results = collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            return [
                {
                    "content": doc,
                    "metadata": meta,
                    "distance": dist
                }
                for doc, meta, dist in zip(
                    results['documents'][0],
                    results['metadatas'][0],
                    results['distances'][0]
                )
            ]
            
        except Exception as e:
            logging.error(f"Error searching documents: {str(e)}")
            return []
    
    def delete_document(self, file_path: str, collection_name: str = "default") -> bool:
        """从知识库中删除文档"""
        if not self.vector_db:
            logging.error("Vector database not initialized")
            return False
            
        try:
            collection = self.vector_db.get_collection(collection_name)
            
            # 删除所有与该文档相关的条目
            collection.delete(
                where={"source": file_path}
            )
            
            logging.info(f"Successfully deleted document: {file_path}")
            return True
            
        except Exception as e:
            logging.error(f"Error deleting document {file_path}: {str(e)}")
            return False
    
    def get_collections(self) -> List[str]:
        """获取所有集合名称"""
        if not self.vector_db:
            return []
            
        try:
            return self.vector_db.list_collections()
        except Exception as e:
            logging.error(f"Error getting collections: {str(e)}")
            return []
    
    def delete_collection(self, collection_name: str) -> bool:
        """删除集合"""
        if not self.vector_db:
            logging.error("Vector database not initialized")
            return False
            
        try:
            self.vector_db.delete_collection(collection_name)
            logging.info(f"Successfully deleted collection: {collection_name}")
            return True
        except Exception as e:
            logging.error(f"Error deleting collection {collection_name}: {str(e)}")
            return False 