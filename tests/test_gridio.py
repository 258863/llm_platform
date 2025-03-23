import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from fastapi.testclient import TestClient
from llm_platform.ui.gridio import GridIO

@pytest.fixture
def driver():
    """创建WebDriver实例"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    yield driver
    driver.quit()

@pytest.fixture
def client():
    """Create a test client."""
    app = GridIO()
    return TestClient(app.app)

def test_gridio_home(driver):
    """测试GridIO首页"""
    driver.get('http://localhost:8000/gridio')
    assert 'GridIO' in driver.title
    
    # 检查导航栏
    nav = driver.find_element(By.CLASS_NAME, 'navbar')
    assert 'Dashboard' in nav.text
    assert 'Models' in nav.text
    assert 'Tasks' in nav.text
    assert 'Resources' in nav.text

def test_dashboard(driver):
    """测试仪表板"""
    driver.get('http://localhost:8000/gridio/dashboard')
    assert 'Dashboard' in driver.title
    
    # 检查仪表板元素
    gpu_usage = driver.find_element(By.ID, 'gpu-usage-chart')
    memory_usage = driver.find_element(By.ID, 'memory-usage-chart')
    task_status = driver.find_element(By.ID, 'task-status-chart')
    
    assert gpu_usage is not None
    assert memory_usage is not None
    assert task_status is not None

def test_models_page(driver):
    """测试模型页面"""
    driver.get('http://localhost:8000/gridio/models')
    assert 'Models' in driver.title
    
    # 检查模型列表
    model_list = driver.find_element(By.ID, 'model-list')
    assert model_list is not None
    
    # 检查模型状态
    model_status = driver.find_element(By.CLASS_NAME, 'model-status')
    assert model_status is not None

def test_tasks_page(driver):
    """测试任务页面"""
    driver.get('http://localhost:8000/gridio/tasks')
    assert 'Tasks' in driver.title
    
    # 检查任务列表
    task_list = driver.find_element(By.ID, 'task-list')
    assert task_list is not None
    
    # 检查任务状态
    task_status = driver.find_element(By.CLASS_NAME, 'task-status')
    assert task_status is not None

def test_resources_page(driver):
    """测试资源页面"""
    driver.get('http://localhost:8000/gridio/resources')
    assert 'Resources' in driver.title
    
    # 检查资源信息
    cpu_info = driver.find_element(By.ID, 'cpu-info')
    memory_info = driver.find_element(By.ID, 'memory-info')
    disk_info = driver.find_element(By.ID, 'disk-info')
    gpu_info = driver.find_element(By.ID, 'gpu-info')
    
    assert cpu_info is not None
    assert memory_info is not None
    assert disk_info is not None
    assert gpu_info is not None

def test_model_management(driver):
    """测试模型管理"""
    driver.get('http://localhost:8000/gridio/models')
    
    # 加载模型
    load_button = driver.find_element(By.ID, 'load-model-button')
    load_button.click()
    
    # 等待加载完成
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'model-loaded'))
    )
    
    # 检查模型状态
    model_status = driver.find_element(By.CLASS_NAME, 'model-status')
    assert 'Loaded' in model_status.text

def test_task_management(driver):
    """测试任务管理"""
    driver.get('http://localhost:8000/gridio/tasks')
    
    # 创建新任务
    create_button = driver.find_element(By.ID, 'create-task-button')
    create_button.click()
    
    # 填写任务表单
    task_name = driver.find_element(By.ID, 'task-name')
    task_name.send_keys('Test Task')
    
    # 提交任务
    submit_button = driver.find_element(By.ID, 'submit-task-button')
    submit_button.click()
    
    # 等待任务创建完成
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'task-created'))
    )
    
    # 检查任务状态
    task_status = driver.find_element(By.CLASS_NAME, 'task-status')
    assert 'Created' in task_status.text

def test_resource_monitoring(driver):
    """测试资源监控"""
    driver.get('http://localhost:8000/gridio/resources')
    
    # 检查实时更新
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'resource-updated'))
    )
    
    # 检查资源使用情况
    gpu_usage = driver.find_element(By.ID, 'gpu-usage')
    memory_usage = driver.find_element(By.ID, 'memory-usage')
    
    assert gpu_usage.text is not None
    assert memory_usage.text is not None

def test_error_handling(driver):
    """测试错误处理"""
    driver.get('http://localhost:8000/gridio/models')
    
    # 尝试加载不存在的模型
    load_button = driver.find_element(By.ID, 'load-model-button')
    load_button.click()
    
    # 检查错误消息
    error_message = driver.find_element(By.CLASS_NAME, 'error-message')
    assert 'Model not found' in error_message.text

def test_responsive_design(driver):
    """测试响应式设计"""
    # 测试移动设备视图
    driver.set_window_size(375, 812)
    driver.get('http://localhost:8000/gridio')
    
    # 检查导航菜单按钮
    menu_button = driver.find_element(By.CLASS_NAME, 'navbar-toggler')
    assert menu_button is not None
    
    # 测试平板设备视图
    driver.set_window_size(768, 1024)
    driver.get('http://localhost:8000/gridio')
    
    # 检查导航栏是否完整显示
    nav = driver.find_element(By.CLASS_NAME, 'navbar')
    assert 'Dashboard' in nav.text
    assert 'Models' in nav.text
    assert 'Tasks' in nav.text
    assert 'Resources' in nav.text

def test_home_page(client):
    """Test the home page."""
    response = client.get('/')
    assert response.status_code == 200
    assert 'text/html' in response.headers['content-type']
    assert 'GridIO' in response.text

def test_dashboard_page(client):
    """Test the dashboard page."""
    response = client.get('/dashboard')
    assert response.status_code == 200
    assert 'text/html' in response.headers['content-type']
    assert 'Dashboard' in response.text

def test_models_page(client):
    """Test the models page."""
    response = client.get('/models')
    assert response.status_code == 200
    assert 'text/html' in response.headers['content-type']
    assert 'Models' in response.text

def test_tasks_page(client):
    """Test the tasks page."""
    response = client.get('/tasks')
    assert response.status_code == 200
    assert 'text/html' in response.headers['content-type']
    assert 'Tasks' in response.text

def test_resources_page(client):
    """Test the resources page."""
    response = client.get('/resources')
    assert response.status_code == 200
    assert 'text/html' in response.headers['content-type']
    assert 'Resources' in response.text

def test_websocket_worker(client):
    """Test the worker WebSocket endpoint."""
    with client.websocket_connect('/ws/worker') as websocket:
        # Send worker registration
        websocket.send_json({
            'type': 'register',
            'worker_id': 'test-worker-1',
            'capabilities': ['chat', 'embedding']
        })
        
        # Receive acknowledgment
        response = websocket.receive_json()
        assert response['type'] == 'registered'
        assert response['worker_id'] == 'test-worker-1'
        
        # Send heartbeat
        websocket.send_json({
            'type': 'heartbeat',
            'worker_id': 'test-worker-1',
            'status': 'idle'
        })
        
        # Receive task
        response = websocket.receive_json()
        assert response['type'] == 'task'
        assert 'task_id' in response
        assert 'task_type' in response
        assert 'parameters' in response

def test_websocket_dashboard(client):
    """Test the dashboard WebSocket endpoint."""
    with client.websocket_connect('/ws/dashboard') as websocket:
        # Receive initial status
        response = websocket.receive_json()
        assert response['type'] == 'status'
        assert 'workers' in response['data']
        assert 'tasks' in response['data']
        assert 'resources' in response['data']

def test_static_files(client):
    """Test static file serving."""
    # Test CSS file
    response = client.get('/static/css/gridio.css')
    assert response.status_code == 200
    assert 'text/css' in response.headers['content-type']
    
    # Test JavaScript file
    response = client.get('/static/js/gridio.js')
    assert response.status_code == 200
    assert 'application/javascript' in response.headers['content-type']

def test_list_workers(client):
    """Test the list workers endpoint."""
    response = client.get('/api/v1/workers')
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_worker_info(client):
    """Test the worker info endpoint."""
    response = client.get('/api/v1/workers/test-worker-1')
    assert response.status_code == 200
    assert 'worker_id' in response.json()
    assert 'status' in response.json()
    assert 'capabilities' in response.json()

def test_create_task(client):
    """Test the create task endpoint."""
    response = client.post(
        '/api/v1/tasks',
        json={
            'type': 'chat',
            'parameters': {
                'messages': [{'role': 'user', 'content': 'Hello'}],
                'model': 'gpt-3.5-turbo'
            }
        }
    )
    assert response.status_code == 200
    assert 'task_id' in response.json()

def test_list_tasks(client):
    """Test the list tasks endpoint."""
    response = client.get('/api/v1/tasks')
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_task_info(client):
    """Test the task info endpoint."""
    # First create a task
    response = client.post(
        '/api/v1/tasks',
        json={
            'type': 'chat',
            'parameters': {
                'messages': [{'role': 'user', 'content': 'Hello'}],
                'model': 'gpt-3.5-turbo'
            }
        }
    )
    task_id = response.json()['task_id']
    
    # Get task info
    response = client.get(f'/api/v1/tasks/{task_id}')
    assert response.status_code == 200
    assert response.json()['task_id'] == task_id
    assert 'status' in response.json()
    assert 'result' in response.json()

def test_delete_task(client):
    """Test the delete task endpoint."""
    # First create a task
    response = client.post(
        '/api/v1/tasks',
        json={
            'type': 'chat',
            'parameters': {
                'messages': [{'role': 'user', 'content': 'Hello'}],
                'model': 'gpt-3.5-turbo'
            }
        }
    )
    task_id = response.json()['task_id']
    
    # Delete task
    response = client.delete(f'/api/v1/tasks/{task_id}')
    assert response.status_code == 200
    
    # Verify task is deleted
    response = client.get(f'/api/v1/tasks/{task_id}')
    assert response.status_code == 404

def test_system_resources(client):
    """Test the system resources endpoint."""
    response = client.get('/api/v1/system/resources')
    assert response.status_code == 200
    assert 'cpu' in response.json()
    assert 'memory' in response.json()
    assert 'disk' in response.json()
    assert 'gpu' in response.json()

def test_error_handling(client):
    """Test error handling in the GridIO interface."""
    # Test invalid worker ID
    response = client.get('/api/v1/workers/invalid-worker')
    assert response.status_code == 404
    
    # Test invalid task ID
    response = client.get('/api/v1/tasks/invalid-task')
    assert response.status_code == 404
    
    # Test invalid task type
    response = client.post(
        '/api/v1/tasks',
        json={
            'type': 'invalid-type',
            'parameters': {}
        }
    )
    assert response.status_code == 400

def test_rate_limiting(client):
    """Test rate limiting in the GridIO interface."""
    # Make multiple requests in quick succession
    for _ in range(10):
        response = client.get('/api/v1/workers')
        if response.status_code == 429:
            assert 'Too Many Requests' in response.text
            break
    else:
        pytest.fail('Rate limiting not triggered')

def test_cors_headers(client):
    """Test CORS headers in the GridIO interface."""
    response = client.options(
        '/api/v1/tasks',
        headers={
            'Origin': 'http://localhost:3000',
            'Access-Control-Request-Method': 'POST'
        }
    )
    assert response.status_code == 200
    assert 'Access-Control-Allow-Origin' in response.headers
    assert 'Access-Control-Allow-Methods' in response.headers 