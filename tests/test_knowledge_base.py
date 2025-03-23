import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from core.knowledge_base import KnowledgeBase

@pytest.fixture
def knowledge_base(test_config, test_data_dir):
    """创建知识库实例"""
    config = test_config.copy()
    config['knowledge_base']['vector_db']['path'] = str(test_data_dir / 'vector_db')
    config['knowledge_base']['document_store']['path'] = str(test_data_dir / 'doc_store')
    
    with patch('core.knowledge_base.load_config', return_value=config):
        kb = KnowledgeBase()
        yield kb
        del kb

def test_init(knowledge_base):
    """测试初始化"""
    assert knowledge_base.config is not None
    assert knowledge_base.vector_db is not None
    assert knowledge_base.document_store is not None

def test_upload_document(knowledge_base, test_document):
    """测试上传文档"""
    collection = "test_collection"
    result = knowledge_base.upload_document(test_document, collection)
    assert result is not None
    assert "document_id" in result
    assert "collection" in result
    assert result["collection"] == collection

def test_search_documents(knowledge_base, test_document):
    """测试搜索文档"""
    collection = "test_collection"
    knowledge_base.upload_document(test_document, collection)
    
    query = "test document"
    results = knowledge_base.search_documents(query, collection)
    assert isinstance(results, list)
    assert len(results) > 0
    assert "document_id" in results[0]
    assert "score" in results[0]
    assert "content" in results[0]

def test_list_collections(knowledge_base, test_document):
    """测试获取集合列表"""
    collection = "test_collection"
    knowledge_base.upload_document(test_document, collection)
    
    collections = knowledge_base.list_collections()
    assert isinstance(collections, list)
    assert collection in collections

def test_delete_collection(knowledge_base, test_document):
    """测试删除集合"""
    collection = "test_collection"
    knowledge_base.upload_document(test_document, collection)
    
    result = knowledge_base.delete_collection(collection)
    assert result is not None
    assert "message" in result
    
    collections = knowledge_base.list_collections()
    assert collection not in collections

def test_get_document(knowledge_base, test_document):
    """测试获取文档"""
    collection = "test_collection"
    upload_result = knowledge_base.upload_document(test_document, collection)
    
    document = knowledge_base.get_document(upload_result["document_id"], collection)
    assert document is not None
    assert "content" in document
    assert "metadata" in document

def test_update_document(knowledge_base, test_document):
    """测试更新文档"""
    collection = "test_collection"
    upload_result = knowledge_base.upload_document(test_document, collection)
    
    new_content = "Updated test document content"
    result = knowledge_base.update_document(
        upload_result["document_id"],
        collection,
        content=new_content
    )
    assert result is not None
    assert "message" in result
    
    document = knowledge_base.get_document(upload_result["document_id"], collection)
    assert document["content"] == new_content

def test_delete_document(knowledge_base, test_document):
    """测试删除文档"""
    collection = "test_collection"
    upload_result = knowledge_base.upload_document(test_document, collection)
    
    result = knowledge_base.delete_document(upload_result["document_id"], collection)
    assert result is not None
    assert "message" in result
    
    document = knowledge_base.get_document(upload_result["document_id"], collection)
    assert document is None

def test_invalid_collection(knowledge_base):
    """测试无效集合"""
    with pytest.raises(ValueError):
        knowledge_base.search_documents("query", "invalid_collection")

def test_invalid_document_id(knowledge_base):
    """测试无效文档ID"""
    with pytest.raises(ValueError):
        knowledge_base.get_document("invalid_id", "test_collection")

def test_invalid_file(knowledge_base):
    """测试无效文件"""
    with pytest.raises(ValueError):
        knowledge_base.upload_document(Path("invalid_file.txt"), "test_collection")

def test_cleanup(knowledge_base):
    """测试清理"""
    collection = "test_collection"
    knowledge_base.upload_document(test_document, collection)
    del knowledge_base
    # 验证资源是否被正确清理
    # 这里需要根据具体的实现来验证 