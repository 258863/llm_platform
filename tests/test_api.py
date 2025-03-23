import pytest
from fastapi.testclient import TestClient
from llm_platform.api.main import app

@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)

def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {'status': 'healthy'}

def test_list_models(client, mock_openai_api):
    """Test the list models endpoint."""
    response = client.get('/api/v1/models')
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_chat_completion(client, mock_openai_api):
    """Test the chat completion endpoint."""
    response = client.post(
        '/api/v1/chat',
        json={
            'messages': [{'role': 'user', 'content': 'Hello, how are you?'}],
            'model': 'gpt-3.5-turbo',
            'temperature': 0.7,
            'max_tokens': 1000
        }
    )
    assert response.status_code == 200
    assert 'choices' in response.json()
    assert response.json()['choices'][0]['message']['content'] == 'This is a mock response.'

def test_upload_document(client, test_data_dir):
    """Test the document upload endpoint."""
    # Create a test file
    test_file = test_data_dir / 'test.txt'
    test_file.write_text('This is a test document.')
    
    # Test file upload
    with open(test_file, 'rb') as f:
        response = client.post(
            '/api/v1/documents',
            files={'file': ('test.txt', f, 'text/plain')}
        )
    assert response.status_code == 200
    assert 'document_id' in response.json()
    
    # Test document retrieval
    document_id = response.json()['document_id']
    response = client.get(f'/api/v1/documents/{document_id}')
    assert response.status_code == 200
    assert response.json()['content'] == 'This is a test document.'

def test_query_knowledge_base(client, test_data_dir):
    """Test the knowledge base query endpoint."""
    # First upload a document
    test_file = test_data_dir / 'test.txt'
    test_file.write_text('This is a test document.')
    
    with open(test_file, 'rb') as f:
        response = client.post(
            '/api/v1/documents',
            files={'file': ('test.txt', f, 'text/plain')}
        )
    document_id = response.json()['document_id']
    
    # Test querying the knowledge base
    response = client.post(
        '/api/v1/query',
        json={
            'query': 'What is in the test document?',
            'document_ids': [document_id]
        }
    )
    assert response.status_code == 200
    assert 'results' in response.json()

def test_list_collections(client):
    """Test the collections list endpoint."""
    response = client.get('/api/v1/collections')
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_collection(client, test_data_dir):
    """Test the collection deletion endpoint."""
    # First create a collection
    test_file = test_data_dir / 'test.txt'
    test_file.write_text('This is a test document.')
    
    with open(test_file, 'rb') as f:
        response = client.post(
            '/api/v1/documents',
            files={'file': ('test.txt', f, 'text/plain')}
        )
    collection_id = response.json()['collection_id']
    
    # Test collection deletion
    response = client.delete(f'/api/v1/collections/{collection_id}')
    assert response.status_code == 200
    
    # Verify collection is deleted
    response = client.get('/api/v1/collections')
    assert collection_id not in [c['id'] for c in response.json()]

def test_system_status(client):
    """Test the system status endpoint."""
    response = client.get('/api/v1/system/status')
    assert response.status_code == 200
    assert 'cpu' in response.json()
    assert 'memory' in response.json()
    assert 'disk' in response.json()

def test_error_handling(client):
    """Test error handling endpoints."""
    # Test invalid model
    response = client.post(
        '/api/v1/chat',
        json={
            'messages': [{'role': 'user', 'content': 'Hello'}],
            'model': 'invalid-model'
        }
    )
    assert response.status_code == 400
    
    # Test invalid document ID
    response = client.get('/api/v1/documents/invalid-id')
    assert response.status_code == 404
    
    # Test invalid collection ID
    response = client.delete('/api/v1/collections/invalid-id')
    assert response.status_code == 404

def test_read_root():
    """测试根路径"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to LLM Platform API"}

def test_list_models():
    """测试获取模型列表"""
    response = client.get("/api/v1/models")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_chat():
    """测试聊天接口"""
    response = client.post(
        "/api/v1/chat",
        json={
            "prompt": "Hello, how are you?",
            "model": "deepseek-r1",
            "max_length": 2048,
            "temperature": 0.7,
            "top_p": 0.9
        }
    )
    assert response.status_code == 200
    assert "response" in response.json()

def test_upload_document():
    """测试文档上传"""
    with open("tests/test_document.txt", "w") as f:
        f.write("This is a test document.")
    
    with open("tests/test_document.txt", "rb") as f:
        response = client.post(
            "/api/v1/knowledge-base/upload",
            files={"file": ("test_document.txt", f, "text/plain")},
            data={"collection": "test_collection"}
        )
    
    assert response.status_code == 200
    assert "message" in response.json()

def test_list_collections():
    """测试获取知识库集合列表"""
    response = client.get("/api/v1/knowledge-base/collections")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_collection():
    """测试删除知识库集合"""
    response = client.delete("/api/v1/knowledge-base/collections/test_collection")
    assert response.status_code == 200
    assert "message" in response.json()

def test_system_resources():
    """测试系统资源信息"""
    response = client.get("/api/v1/system/resources")
    assert response.status_code == 200
    data = response.json()
    assert "cpu" in data
    assert "memory" in data
    assert "disk" in data
    assert "gpu" in data

def test_invalid_model():
    """测试无效模型"""
    response = client.post(
        "/api/v1/chat",
        json={
            "prompt": "Hello",
            "model": "invalid_model",
            "max_length": 2048,
            "temperature": 0.7,
            "top_p": 0.9
        }
    )
    assert response.status_code == 400
    assert "error" in response.json()

def test_invalid_prompt():
    """测试无效提示"""
    response = client.post(
        "/api/v1/chat",
        json={
            "prompt": "",
            "model": "deepseek-r1",
            "max_length": 2048,
            "temperature": 0.7,
            "top_p": 0.9
        }
    )
    assert response.status_code == 400
    assert "error" in response.json()

def test_invalid_parameters():
    """测试无效参数"""
    response = client.post(
        "/api/v1/chat",
        json={
            "prompt": "Hello",
            "model": "deepseek-r1",
            "max_length": -1,
            "temperature": 2.0,
            "top_p": 2.0
        }
    )
    assert response.status_code == 400
    assert "error" in response.json()

def test_websocket_chat():
    """测试WebSocket聊天"""
    with client.websocket_connect("/ws/chat") as websocket:
        websocket.send_json({
            "prompt": "Hello, how are you?",
            "model": "deepseek-r1",
            "max_length": 2048,
            "temperature": 0.7,
            "top_p": 0.9
        })
        response = websocket.receive_json()
        assert "response" in response

def test_websocket_system_monitor():
    """测试WebSocket系统监控"""
    with client.websocket_connect("/ws/system-monitor") as websocket:
        response = websocket.receive_json()
        assert "cpu" in response
        assert "memory" in response
        assert "disk" in response
        assert "gpu" in response

def test_rate_limit():
    """测试速率限制"""
    for _ in range(100):
        response = client.post(
            "/api/v1/chat",
            json={
                "prompt": "Hello",
                "model": "deepseek-r1",
                "max_length": 2048,
                "temperature": 0.7,
                "top_p": 0.9
            }
        )
    
    response = client.post(
        "/api/v1/chat",
        json={
            "prompt": "Hello",
            "model": "deepseek-r1",
            "max_length": 2048,
            "temperature": 0.7,
            "top_p": 0.9
        }
    )
    assert response.status_code == 429
    assert "error" in response.json()

def test_api_key_auth():
    """测试API密钥认证"""
    response = client.post(
        "/api/v1/chat",
        json={
            "prompt": "Hello",
            "model": "deepseek-r1",
            "max_length": 2048,
            "temperature": 0.7,
            "top_p": 0.9
        },
        headers={"X-API-Key": "invalid_key"}
    )
    assert response.status_code == 401
    assert "error" in response.json()

def test_cors():
    """测试CORS"""
    response = client.options(
        "/api/v1/chat",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type"
        }
    )
    assert response.status_code == 200
    assert "Access-Control-Allow-Origin" in response.headers
    assert "Access-Control-Allow-Methods" in response.headers
    assert "Access-Control-Allow-Headers" in response.headers 