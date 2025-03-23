import os
import yaml
import torch
from typing import Dict, List, Optional
from transformers import AutoModel, AutoTokenizer
import ollama
from concurrent.futures import ThreadPoolExecutor
import logging

class ModelManager:
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config = self._load_config(config_path)
        self.models: Dict[str, Dict] = {}
        self.executors: Dict[str, ThreadPoolExecutor] = {}
        self._init_models()
        self._init_gpu()
        
    def _load_config(self, config_path: str) -> dict:
        """加载配置文件"""
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def _init_gpu(self):
        """初始化GPU设置"""
        if torch.cuda.is_available():
            torch.cuda.set_device(self.config['gpu']['devices'][0])
            for device in self.config['gpu']['devices']:
                torch.cuda.set_per_process_memory_fraction(
                    self.config['gpu']['memory_fraction'],
                    device
                )
    
    def _init_models(self):
        """初始化所有配置的模型"""
        for model_config in self.config['models']['available']:
            model_name = model_config['name']
            self.models[model_name] = {
                'config': model_config,
                'instance': None,
                'tokenizer': None
            }
            
            # 为每个模型创建线程池
            self.executors[model_name] = ThreadPoolExecutor(max_workers=1)
    
    def load_model(self, model_name: str) -> bool:
        """加载指定模型"""
        if model_name not in self.models:
            logging.error(f"Model {model_name} not found in configuration")
            return False
            
        try:
            model_config = self.models[model_name]['config']
            
            if model_config['type'] == 'ollama':
                # 使用Ollama加载模型
                self.models[model_name]['instance'] = ollama.Client()
            else:
                # 使用Transformers加载模型
                self.models[model_name]['tokenizer'] = AutoTokenizer.from_pretrained(
                    model_name,
                    trust_remote_code=True
                )
                self.models[model_name]['instance'] = AutoModel.from_pretrained(
                    model_name,
                    trust_remote_code=True,
                    device_map="auto"
                )
            
            logging.info(f"Successfully loaded model: {model_name}")
            return True
            
        except Exception as e:
            logging.error(f"Error loading model {model_name}: {str(e)}")
            return False
    
    def unload_model(self, model_name: str) -> bool:
        """卸载指定模型"""
        if model_name not in self.models:
            return False
            
        try:
            if self.models[model_name]['instance']:
                del self.models[model_name]['instance']
                self.models[model_name]['instance'] = None
            if self.models[model_name]['tokenizer']:
                del self.models[model_name]['tokenizer']
                self.models[model_name]['tokenizer'] = None
            return True
        except Exception as e:
            logging.error(f"Error unloading model {model_name}: {str(e)}")
            return False
    
    async def generate(
        self,
        model_name: str,
        prompt: str,
        max_length: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        use_knowledge: bool = False,
        knowledge_context: Optional[str] = None
    ) -> str:
        """生成文本响应"""
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not found")
            
        model_config = self.models[model_name]['config']
        
        # 使用配置或传入的参数
        max_length = max_length or model_config['max_length']
        temperature = temperature or model_config['temperature']
        top_p = top_p or model_config['top_p']
        
        # 构建完整提示词
        if use_knowledge and knowledge_context:
            prompt = f"Context: {knowledge_context}\n\nQuestion: {prompt}"
        
        try:
            if model_config['type'] == 'ollama':
                # 使用Ollama生成
                response = await self.executors[model_name].submit(
                    self.models[model_name]['instance'].generate,
                    model=model_name,
                    prompt=prompt,
                    max_tokens=max_length,
                    temperature=temperature,
                    top_p=top_p
                )
                return response['response']
            else:
                # 使用Transformers生成
                inputs = self.models[model_name]['tokenizer'](
                    prompt,
                    return_tensors="pt"
                ).to(self.models[model_name]['instance'].device)
                
                outputs = await self.executors[model_name].submit(
                    self.models[model_name]['instance'].generate,
                    **inputs,
                    max_length=max_length,
                    temperature=temperature,
                    top_p=top_p
                )
                
                return self.models[model_name]['tokenizer'].decode(
                    outputs[0],
                    skip_special_tokens=True
                )
                
        except Exception as e:
            logging.error(f"Error generating response: {str(e)}")
            raise
    
    def get_available_models(self) -> List[str]:
        """获取所有可用模型列表"""
        return list(self.models.keys())
    
    def get_model_config(self, model_name: str) -> Optional[dict]:
        """获取指定模型的配置"""
        return self.models.get(model_name, {}).get('config')
    
    def __del__(self):
        """清理资源"""
        for executor in self.executors.values():
            executor.shutdown()
        for model_name in self.models:
            self.unload_model(model_name) 