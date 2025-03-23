import os
import sys
import pytest
import tempfile
from pathlib import Path
from typing import Generator, Dict, Any

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """创建临时目录"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)

@pytest.fixture(scope='session')
def test_data_dir():
    """Create and return a temporary directory for test data."""
    data_dir = project_root / 'tests' / 'data'
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir

@pytest.fixture(scope='session')
def test_config():
    """Return a test configuration dictionary."""
    return {
        'server': {
            'host': '127.0.0.1',
            'port': 8000,
            'debug': True,
            'workers': 1
        },
        'model': {
            'default': 'gpt-3.5-turbo',
            'max_tokens': 1000,
            'temperature': 0.7,
            'top_p': 0.9
        },
        'knowledge_base': {
            'path': str(project_root / 'tests' / 'data' / 'knowledge_base'),
            'max_file_size': 10485760,
            'allowed_extensions': ['.txt', '.pdf', '.doc', '.docx', '.md']
        },
        'logging': {
            'level': 'DEBUG',
            'file': str(project_root / 'tests' / 'data' / 'test.log'),
            'max_size': 1048576,
            'backup_count': 1
        }
    }

@pytest.fixture(scope='session')
def test_env():
    """Set up test environment variables."""
    os.environ['TESTING'] = 'true'
    os.environ['DEBUG'] = 'true'
    yield
    os.environ.pop('TESTING', None)
    os.environ.pop('DEBUG', None)

@pytest.fixture(scope='function')
def mock_openai_api(monkeypatch):
    """Mock OpenAI API responses."""
    def mock_completion(*args, **kwargs):
        return {
            'choices': [{
                'message': {
                    'content': 'This is a mock response.',
                    'role': 'assistant'
                }
            }]
        }
    
    monkeypatch.setattr('openai.ChatCompletion.create', mock_completion)
    return mock_completion

@pytest.fixture(scope='function')
def mock_redis(monkeypatch):
    """Mock Redis client."""
    class MockRedis:
        def __init__(self, *args, **kwargs):
            self.data = {}
        
        def get(self, key):
            return self.data.get(key)
        
        def set(self, key, value):
            self.data[key] = value
        
        def delete(self, key):
            self.data.pop(key, None)
        
        def exists(self, key):
            return key in self.data
    
    monkeypatch.setattr('redis.Redis', MockRedis)
    return MockRedis

@pytest.fixture(scope='function')
def mock_postgres(monkeypatch):
    """Mock PostgreSQL connection."""
    class MockConnection:
        def __init__(self, *args, **kwargs):
            self.data = {}
        
        def cursor(self):
            return self
        
        def execute(self, query, params=None):
            pass
        
        def fetchall(self):
            return []
        
        def close(self):
            pass
    
    class MockPsycopg2:
        def connect(*args, **kwargs):
            return MockConnection()
    
    monkeypatch.setattr('psycopg2.connect', MockPsycopg2.connect)
    return MockConnection

@pytest.fixture
def test_data_dir(temp_dir: Path) -> Generator[Path, None, None]:
    """创建测试数据目录"""
    data_dir = temp_dir / 'data'
    data_dir.mkdir(parents=True)
    
    # 创建子目录
    (data_dir / 'uploads').mkdir()
    (data_dir / 'knowledge_base').mkdir()
    (data_dir / 'knowledge_base' / 'vector_db').mkdir()
    (data_dir / 'knowledge_base' / 'doc_store').mkdir()
    
    yield data_dir

@pytest.fixture
def test_log_dir(temp_dir: Path) -> Generator[Path, None, None]:
    """创建测试日志目录"""
    log_dir = temp_dir / 'logs'
    log_dir.mkdir(parents=True)
    yield log_dir

@pytest.fixture
def test_model_dir(temp_dir: Path) -> Generator[Path, None, None]:
    """创建测试模型目录"""
    model_dir = temp_dir / 'models'
    model_dir.mkdir(parents=True)
    yield model_dir

@pytest.fixture
def test_document() -> Generator[Path, None, None]:
    """创建测试文档"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write('This is a test document.\nIt contains some sample text.')
        yield Path(f.name)
    os.unlink(f.name) 