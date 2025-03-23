import pytest
from fastapi.testclient import TestClient
from llm_platform.ui.web import WebUI

@pytest.fixture
def client():
    """Create a test client."""
    app = WebUI()
    return TestClient(app.app)

def test_home_page(client):
    """Test the home page."""
    response = client.get('/')
    assert response.status_code == 200
    assert 'text/html' in response.headers['content-type']
    assert 'LLM Platform' in response.text

def test_chat_page(client):
    """Test the chat page."""
    response = client.get('/chat')
    assert response.status_code == 200
    assert 'text/html' in response.headers['content-type']
    assert 'Chat' in response.text

def test_knowledge_base_page(client):
    """Test the knowledge base page."""
    response = client.get('/knowledge-base')
    assert response.status_code == 200
    assert 'text/html' in response.headers['content-type']
    assert 'Knowledge Base' in response.text

def test_system_monitor_page(client):
    """Test the system monitor page."""
    response = client.get('/system-monitor')
    assert response.status_code == 200
    assert 'text/html' in response.headers['content-type']
    assert 'System Monitor' in response.text

def test_websocket_chat(client, mock_openai_api):
    """Test the chat WebSocket endpoint."""
    with client.websocket_connect('/ws/chat') as websocket:
        # Send a message
        websocket.send_json({
            'type': 'message',
            'content': 'Hello, how are you?'
        })
        
        # Receive response
        response = websocket.receive_json()
        assert response['type'] == 'message'
        assert response['content'] == 'This is a mock response.'

def test_websocket_system_monitor(client):
    """Test the system monitor WebSocket endpoint."""
    with client.websocket_connect('/ws/system') as websocket:
        # Receive initial status
        response = websocket.receive_json()
        assert response['type'] == 'status'
        assert 'cpu' in response['data']
        assert 'memory' in response['data']
        assert 'disk' in response['data']

def test_static_files(client):
    """Test static file serving."""
    # Test CSS file
    response = client.get('/static/css/main.css')
    assert response.status_code == 200
    assert 'text/css' in response.headers['content-type']
    
    # Test JavaScript file
    response = client.get('/static/js/main.js')
    assert response.status_code == 200
    assert 'application/javascript' in response.headers['content-type']

def test_upload_document(client, test_data_dir):
    """Test document upload through the web interface."""
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

def test_query_knowledge_base(client, test_data_dir):
    """Test knowledge base query through the web interface."""
    # First upload a document
    test_file = test_data_dir / 'test.txt'
    test_file.write_text('This is a test document.')
    
    with open(test_file, 'rb') as f:
        response = client.post(
            '/api/v1/documents',
            files={'file': ('test.txt', f, 'text/plain')}
        )
    document_id = response.json()['document_id']
    
    # Test querying
    response = client.post(
        '/api/v1/query',
        json={
            'query': 'What is in the test document?',
            'document_ids': [document_id]
        }
    )
    assert response.status_code == 200
    assert 'results' in response.json()

def test_error_handling(client):
    """Test error handling in the web interface."""
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

def test_rate_limiting(client):
    """Test rate limiting in the web interface."""
    # Make multiple requests in quick succession
    for _ in range(10):
        response = client.get('/api/v1/models')
        if response.status_code == 429:
            assert 'Too Many Requests' in response.text
            break
    else:
        pytest.fail('Rate limiting not triggered')

def test_cors_headers(client):
    """Test CORS headers in the web interface."""
    response = client.options(
        '/api/v1/chat',
        headers={
            'Origin': 'http://localhost:3000',
            'Access-Control-Request-Method': 'POST'
        }
    )
    assert response.status_code == 200
    assert 'Access-Control-Allow-Origin' in response.headers
    assert 'Access-Control-Allow-Methods' in response.headers 