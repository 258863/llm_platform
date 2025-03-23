import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

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

def test_home_page(driver):
    """测试首页"""
    driver.get('http://localhost:8000')
    assert 'LLM Platform' in driver.title
    
    # 检查导航栏
    nav = driver.find_element(By.CLASS_NAME, 'navbar')
    assert 'Home' in nav.text
    assert 'Chat' in nav.text
    assert 'Knowledge Base' in nav.text
    assert 'System Monitor' in nav.text

def test_chat_page(driver):
    """测试聊天页面"""
    driver.get('http://localhost:8000/chat')
    assert 'Chat' in driver.title
    
    # 检查聊天界面元素
    chat_input = driver.find_element(By.ID, 'chat-input')
    send_button = driver.find_element(By.ID, 'send-button')
    chat_history = driver.find_element(By.ID, 'chat-history')
    
    assert chat_input is not None
    assert send_button is not None
    assert chat_history is not None

def test_chat_functionality(driver):
    """测试聊天功能"""
    driver.get('http://localhost:8000/chat')
    
    # 输入消息
    chat_input = driver.find_element(By.ID, 'chat-input')
    chat_input.send_keys('Hello, how are you?')
    
    # 发送消息
    send_button = driver.find_element(By.ID, 'send-button')
    send_button.click()
    
    # 等待响应
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'message-response'))
    )
    
    # 检查响应
    response = driver.find_element(By.CLASS_NAME, 'message-response')
    assert response.text is not None
    assert len(response.text) > 0

def test_knowledge_base_page(driver):
    """测试知识库页面"""
    driver.get('http://localhost:8000/knowledge-base')
    assert 'Knowledge Base' in driver.title
    
    # 检查知识库界面元素
    upload_form = driver.find_element(By.ID, 'upload-form')
    collections_list = driver.find_element(By.ID, 'collections-list')
    
    assert upload_form is not None
    assert collections_list is not None

def test_document_upload(driver):
    """测试文档上传"""
    driver.get('http://localhost:8000/knowledge-base')
    
    # 选择文件
    file_input = driver.find_element(By.ID, 'file-input')
    file_input.send_keys('tests/test_document.txt')
    
    # 选择集合
    collection_select = driver.find_element(By.ID, 'collection-select')
    collection_select.send_keys('test_collection')
    
    # 上传文件
    upload_button = driver.find_element(By.ID, 'upload-button')
    upload_button.click()
    
    # 等待上传完成
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'upload-success'))
    )
    
    # 检查上传成功消息
    success_message = driver.find_element(By.CLASS_NAME, 'upload-success')
    assert 'Document uploaded successfully' in success_message.text

def test_system_monitor_page(driver):
    """测试系统监控页面"""
    driver.get('http://localhost:8000/system-monitor')
    assert 'System Monitor' in driver.title
    
    # 检查监控界面元素
    cpu_usage = driver.find_element(By.ID, 'cpu-usage')
    memory_usage = driver.find_element(By.ID, 'memory-usage')
    disk_usage = driver.find_element(By.ID, 'disk-usage')
    gpu_usage = driver.find_element(By.ID, 'gpu-usage')
    
    assert cpu_usage is not None
    assert memory_usage is not None
    assert disk_usage is not None
    assert gpu_usage is not None

def test_model_selection(driver):
    """测试模型选择"""
    driver.get('http://localhost:8000/chat')
    
    # 选择模型
    model_select = driver.find_element(By.ID, 'model-select')
    model_select.send_keys('deepseek-r1')
    
    # 检查模型参数
    max_length = driver.find_element(By.ID, 'max-length')
    temperature = driver.find_element(By.ID, 'temperature')
    top_p = driver.find_element(By.ID, 'top-p')
    
    assert max_length is not None
    assert temperature is not None
    assert top_p is not None

def test_error_handling(driver):
    """测试错误处理"""
    driver.get('http://localhost:8000/chat')
    
    # 发送空消息
    send_button = driver.find_element(By.ID, 'send-button')
    send_button.click()
    
    # 检查错误消息
    error_message = driver.find_element(By.CLASS_NAME, 'error-message')
    assert 'Please enter a message' in error_message.text

def test_responsive_design(driver):
    """测试响应式设计"""
    # 测试移动设备视图
    driver.set_window_size(375, 812)
    driver.get('http://localhost:8000')
    
    # 检查导航菜单按钮
    menu_button = driver.find_element(By.CLASS_NAME, 'navbar-toggler')
    assert menu_button is not None
    
    # 测试平板设备视图
    driver.set_window_size(768, 1024)
    driver.get('http://localhost:8000')
    
    # 检查导航栏是否完整显示
    nav = driver.find_element(By.CLASS_NAME, 'navbar')
    assert 'Home' in nav.text
    assert 'Chat' in nav.text
    assert 'Knowledge Base' in nav.text
    assert 'System Monitor' in nav.text 