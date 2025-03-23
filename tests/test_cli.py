import pytest
from click.testing import CliRunner
from llm_platform.cli.main import cli

@pytest.fixture
def runner():
    """Create a CLI runner."""
    return CliRunner()

def test_list_models(runner, mock_openai_api):
    """Test the list models command."""
    result = runner.invoke(cli, ['models', 'list'])
    assert result.exit_code == 0
    assert 'Available models:' in result.output

def test_chat(runner, mock_openai_api):
    """Test the chat command."""
    result = runner.invoke(cli, ['chat', '--message', 'Hello, how are you?'])
    assert result.exit_code == 0
    assert 'This is a mock response.' in result.output

def test_chat_with_model(runner, mock_openai_api):
    """Test the chat command with a specific model."""
    result = runner.invoke(cli, [
        'chat',
        '--message', 'Hello, how are you?',
        '--model', 'gpt-3.5-turbo'
    ])
    assert result.exit_code == 0
    assert 'This is a mock response.' in result.output

def test_chat_with_temperature(runner, mock_openai_api):
    """Test the chat command with temperature setting."""
    result = runner.invoke(cli, [
        'chat',
        '--message', 'Hello, how are you?',
        '--temperature', '0.8'
    ])
    assert result.exit_code == 0
    assert 'This is a mock response.' in result.output

def test_upload_document(runner, test_data_dir):
    """Test the document upload command."""
    # Create a test file
    test_file = test_data_dir / 'test.txt'
    test_file.write_text('This is a test document.')
    
    # Test file upload
    result = runner.invoke(cli, [
        'documents',
        'upload',
        str(test_file)
    ])
    assert result.exit_code == 0
    assert 'Document uploaded successfully' in result.output

def test_list_documents(runner):
    """Test the list documents command."""
    result = runner.invoke(cli, ['documents', 'list'])
    assert result.exit_code == 0
    assert 'Documents:' in result.output

def test_query_knowledge_base(runner, test_data_dir):
    """Test the knowledge base query command."""
    # First upload a document
    test_file = test_data_dir / 'test.txt'
    test_file.write_text('This is a test document.')
    
    result = runner.invoke(cli, [
        'documents',
        'upload',
        str(test_file)
    ])
    
    # Test querying
    result = runner.invoke(cli, [
        'query',
        '--text', 'What is in the test document?'
    ])
    assert result.exit_code == 0
    assert 'Results:' in result.output

def test_list_collections(runner):
    """Test the list collections command."""
    result = runner.invoke(cli, ['collections', 'list'])
    assert result.exit_code == 0
    assert 'Collections:' in result.output

def test_delete_collection(runner, test_data_dir):
    """Test the collection deletion command."""
    # First create a collection
    test_file = test_data_dir / 'test.txt'
    test_file.write_text('This is a test document.')
    
    result = runner.invoke(cli, [
        'documents',
        'upload',
        str(test_file)
    ])
    
    # Get the collection ID from the output
    collection_id = result.output.split()[-1]
    
    # Test collection deletion
    result = runner.invoke(cli, [
        'collections',
        'delete',
        collection_id
    ])
    assert result.exit_code == 0
    assert 'Collection deleted successfully' in result.output

def test_system_status(runner):
    """Test the system status command."""
    result = runner.invoke(cli, ['system', 'status'])
    assert result.exit_code == 0
    assert 'CPU Usage:' in result.output
    assert 'Memory Usage:' in result.output
    assert 'Disk Usage:' in result.output

def test_invalid_model(runner):
    """Test error handling for invalid model."""
    result = runner.invoke(cli, [
        'chat',
        '--message', 'Hello',
        '--model', 'invalid-model'
    ])
    assert result.exit_code == 1
    assert 'Error: Invalid model' in result.output

def test_invalid_file(runner):
    """Test error handling for invalid file."""
    result = runner.invoke(cli, [
        'documents',
        'upload',
        'nonexistent.txt'
    ])
    assert result.exit_code == 1
    assert 'Error: File not found' in result.output

def test_invalid_collection(runner):
    """Test error handling for invalid collection."""
    result = runner.invoke(cli, [
        'collections',
        'delete',
        'invalid-id'
    ])
    assert result.exit_code == 1
    assert 'Error: Collection not found' in result.output

def test_help(runner):
    """测试帮助信息"""
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert "Commands:" in result.output
    assert "Options:" in result.output

def test_command_help(runner):
    """测试命令帮助信息"""
    result = runner.invoke(cli, ['chat', '--help'])
    assert result.exit_code == 0
    assert "Options:" in result.output
    assert "--prompt" in result.output
    assert "--model" in result.output
    assert "--max-length" in result.output
    assert "--temperature" in result.output
    assert "--top-p" in result.output

def test_version(runner):
    """测试版本信息"""
    result = runner.invoke(cli, ['--version'])
    assert result.exit_code == 0
    assert "version" in result.output

def test_config_file(runner):
    """测试配置文件"""
    result = runner.invoke(cli, [
        'chat',
        '--prompt', 'Hello',
        '--model', 'deepseek-r1',
        '--config', 'config/config.yaml'
    ])
    assert result.exit_code == 0
    assert "Response:" in result.output

def test_output_format(runner):
    """测试输出格式"""
    result = runner.invoke(cli, [
        'chat',
        '--prompt', 'Hello',
        '--model', 'deepseek-r1',
        '--format', 'json'
    ])
    assert result.exit_code == 0
    assert result.output.strip().startswith('{')
    assert result.output.strip().endswith('}')

def test_interactive_mode(runner):
    """测试交互模式"""
    result = runner.invoke(cli, ['chat', '--interactive'])
    assert result.exit_code == 0
    assert "Interactive mode" in result.output 