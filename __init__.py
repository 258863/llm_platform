"""
LLM Platform - 大语言模型服务平台
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .core.model_manager import ModelManager
from .core.knowledge_base import KnowledgeBase
from .core.system_monitor import SystemMonitor
from .api.main import app
from .cli import cli

__all__ = [
    "ModelManager",
    "KnowledgeBase",
    "SystemMonitor",
    "app",
    "cli"
] 