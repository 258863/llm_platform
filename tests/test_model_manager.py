import pytest
from unittest.mock import MagicMock, patch
from core.model_manager import ModelManager

@pytest.fixture
def model_manager(test_config):
    """创建模型管理器实例"""
    with patch('core.model_manager.load_config', return_value=test_config):
        manager = ModelManager()
        yield manager
        del manager

def test_init(model_manager):
    """测试初始化"""
    assert model_manager.config is not None
    assert isinstance(model_manager.models, dict)
    assert isinstance(model_manager.gpu_settings, dict)

def test_load_model(model_manager):
    """测试加载模型"""
    model_name = "deepseek-r1"
    model = model_manager.load_model(model_name)
    assert model is not None
    assert model_name in model_manager.models

def test_unload_model(model_manager):
    """测试卸载模型"""
    model_name = "deepseek-r1"
    model_manager.load_model(model_name)
    model_manager.unload_model(model_name)
    assert model_name not in model_manager.models

def test_generate(model_manager):
    """测试生成文本"""
    model_name = "deepseek-r1"
    prompt = "Hello, how are you?"
    response = model_manager.generate(prompt, model_name)
    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0

def test_get_available_models(model_manager):
    """测试获取可用模型列表"""
    models = model_manager.get_available_models()
    assert isinstance(models, list)
    assert len(models) > 0
    assert "deepseek-r1" in models

def test_get_model_config(model_manager):
    """测试获取模型配置"""
    model_name = "deepseek-r1"
    config = model_manager.get_model_config(model_name)
    assert config is not None
    assert "type" in config
    assert "size" in config
    assert "gpu_memory" in config

def test_invalid_model(model_manager):
    """测试无效模型"""
    with pytest.raises(ValueError):
        model_manager.load_model("invalid_model")

def test_invalid_prompt(model_manager):
    """测试无效提示"""
    with pytest.raises(ValueError):
        model_manager.generate("", "deepseek-r1")

def test_invalid_parameters(model_manager):
    """测试无效参数"""
    with pytest.raises(ValueError):
        model_manager.generate(
            "Hello",
            "deepseek-r1",
            max_length=-1,
            temperature=2.0,
            top_p=2.0
        )

def test_model_cleanup(model_manager):
    """测试模型清理"""
    model_name = "deepseek-r1"
    model_manager.load_model(model_name)
    del model_manager
    # 验证资源是否被正确清理
    # 这里需要根据具体的实现来验证

def test_parallel_inference(model_manager):
    """测试并行推理"""
    model_name = "deepseek-r1"
    prompts = ["Hello", "How are you?", "What's the weather?"]
    responses = model_manager.generate(prompts, model_name)
    assert isinstance(responses, list)
    assert len(responses) == len(prompts)
    assert all(isinstance(r, str) for r in responses)
 