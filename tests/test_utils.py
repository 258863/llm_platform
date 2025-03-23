import pytest
import os
import yaml
from pathlib import Path
from llm_platform.utils.config import load_config
from llm_platform.utils.logger import setup_logger
from llm_platform.utils.validators import validate_model_config, validate_kb_config

def test_load_config(test_data_dir):
    """Test configuration loading."""
    # Create a test config file
    config_path = test_data_dir / 'test_config.yaml'
    test_config = {
        'server': {
            'host': '127.0.0.1',
            'port': 8000
        },
        'model': {
            'default': 'gpt-3.5-turbo',
            'max_tokens': 1000
        }
    }
    with open(config_path, 'w') as f:
        yaml.dump(test_config, f)
    
    # Test loading config
    config = load_config(config_path)
    assert config['server']['host'] == '127.0.0.1'
    assert config['server']['port'] == 8000
    assert config['model']['default'] == 'gpt-3.5-turbo'
    assert config['model']['max_tokens'] == 1000

def test_load_config_missing_file():
    """Test configuration loading with missing file."""
    with pytest.raises(FileNotFoundError):
        load_config('nonexistent.yaml')

def test_load_config_invalid_yaml(test_data_dir):
    """Test configuration loading with invalid YAML."""
    config_path = test_data_dir / 'invalid_config.yaml'
    with open(config_path, 'w') as f:
        f.write('invalid: yaml: content:')
    
    with pytest.raises(yaml.YAMLError):
        load_config(config_path)

def test_setup_logger(test_data_dir):
    """Test logger setup."""
    log_file = test_data_dir / 'test.log'
    logger = setup_logger(
        name='test_logger',
        log_file=str(log_file),
        level='DEBUG'
    )
    
    # Test logging
    logger.debug('Debug message')
    logger.info('Info message')
    logger.warning('Warning message')
    logger.error('Error message')
    
    # Verify log file
    assert log_file.exists()
    with open(log_file) as f:
        log_content = f.read()
        assert 'Debug message' in log_content
        assert 'Info message' in log_content
        assert 'Warning message' in log_content
        assert 'Error message' in log_content

def test_setup_logger_rotation(test_data_dir):
    """Test logger rotation."""
    log_file = test_data_dir / 'rotating.log'
    logger = setup_logger(
        name='rotating_logger',
        log_file=str(log_file),
        level='DEBUG',
        max_size=100,
        backup_count=2
    )
    
    # Generate enough logs to trigger rotation
    for i in range(100):
        logger.info(f'Test message {i}')
    
    # Verify rotation
    assert log_file.exists()
    assert (test_data_dir / 'rotating.log.1').exists()
    assert (test_data_dir / 'rotating.log.2').exists()

def test_validate_model_config():
    """Test model configuration validation."""
    # Valid config
    valid_config = {
        'default': 'gpt-3.5-turbo',
        'max_tokens': 1000,
        'temperature': 0.7,
        'top_p': 0.9
    }
    assert validate_model_config(valid_config) is True
    
    # Invalid config - missing required fields
    invalid_config = {
        'max_tokens': 1000
    }
    with pytest.raises(ValueError):
        validate_model_config(invalid_config)
    
    # Invalid config - invalid values
    invalid_config = {
        'default': 'gpt-3.5-turbo',
        'max_tokens': -1,
        'temperature': 2.0,
        'top_p': 2.0
    }
    with pytest.raises(ValueError):
        validate_model_config(invalid_config)

def test_validate_kb_config():
    """Test knowledge base configuration validation."""
    # Valid config
    valid_config = {
        'path': 'data/knowledge_base',
        'max_file_size': 10485760,
        'allowed_extensions': ['.txt', '.pdf', '.doc', '.docx']
    }
    assert validate_kb_config(valid_config) is True
    
    # Invalid config - missing required fields
    invalid_config = {
        'max_file_size': 10485760
    }
    with pytest.raises(ValueError):
        validate_kb_config(invalid_config)
    
    # Invalid config - invalid values
    invalid_config = {
        'path': 'data/knowledge_base',
        'max_file_size': -1,
        'allowed_extensions': ['invalid']
    }
    with pytest.raises(ValueError):
        validate_kb_config(invalid_config)

def test_environment_variables():
    """Test environment variable handling."""
    # Set test environment variables
    os.environ['TEST_VAR'] = 'test_value'
    os.environ['TEST_NUM'] = '123'
    
    # Test environment variable access
    assert os.environ.get('TEST_VAR') == 'test_value'
    assert int(os.environ.get('TEST_NUM')) == 123
    
    # Test missing environment variable
    assert os.environ.get('MISSING_VAR') is None
    
    # Clean up
    del os.environ['TEST_VAR']
    del os.environ['TEST_NUM']

def test_path_handling():
    """Test path handling utilities."""
    # Test path joining
    path = Path('data') / 'knowledge_base' / 'test.txt'
    assert str(path) == 'data/knowledge_base/test.txt'
    
    # Test path creation
    path = Path('data').mkdir(exist_ok=True)
    assert Path('data').exists()
    assert Path('data').is_dir()
    
    # Test path resolution
    abs_path = Path('data').resolve()
    assert abs_path.is_absolute()
    
    # Clean up
    Path('data').rmdir()
    assert not Path('data').exists() 