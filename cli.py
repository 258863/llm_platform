"""
Command-line interface for the LLM Platform
"""

import click
import json
from typing import Dict, List, Optional
from .core.model_manager import ModelManager
from .core.knowledge_base import KnowledgeBase
from .core.system_monitor import SystemMonitor
from .utils.config import load_config
from .utils.logger import setup_logger

# Initialize logger
logger = setup_logger(__name__)

# Load configuration
config = load_config()

# Initialize components
model_manager = ModelManager()
knowledge_base = KnowledgeBase()
system_monitor = SystemMonitor()

@click.group()
def cli():
    """LLM Platform Command Line Interface"""
    pass

@cli.command()
def list_models():
    """List available models"""
    try:
        models = model_manager.list_models()
        click.echo(json.dumps(models, indent=2))
    except Exception as e:
        logger.error(f"Error listing models: {e}")
        click.echo(f"Error: {e}", err=True)

@cli.command()
@click.option("--model", "-m", required=True, help="Model ID to use")
@click.option("--prompt", "-p", required=True, help="Input prompt")
@click.option("--max-tokens", "-t", type=int, help="Maximum number of tokens to generate")
@click.option("--temperature", "-temp", type=float, help="Sampling temperature")
@click.option("--top-p", "-p", type=float, help="Top-p sampling parameter")
def chat(model: str, prompt: str, max_tokens: Optional[int] = None, temperature: Optional[float] = None, top_p: Optional[float] = None):
    """Chat with a model"""
    try:
        messages = [{"role": "user", "content": prompt}]
        response = model_manager.chat(
            model_id=model,
            messages=messages,
            max_tokens=max_tokens or config.get("max_tokens", 2048),
            temperature=temperature or config.get("temperature", 0.7),
            top_p=top_p or config.get("top_p", 0.9)
        )
        click.echo(json.dumps(response, indent=2))
    except Exception as e:
        logger.error(f"Error in chat: {e}")
        click.echo(f"Error: {e}", err=True)

@cli.command()
@click.option("--model", "-m", required=True, help="Model ID to use")
@click.option("--prompt", "-p", required=True, help="Input prompt")
@click.option("--max-tokens", "-t", type=int, help="Maximum number of tokens to generate")
@click.option("--temperature", "-temp", type=float, help="Sampling temperature")
def completion(model: str, prompt: str, max_tokens: Optional[int] = None, temperature: Optional[float] = None):
    """Generate text completion"""
    try:
        response = model_manager.completion(
            model_id=model,
            prompt=prompt,
            max_tokens=max_tokens or config.get("max_tokens", 2048),
            temperature=temperature or config.get("temperature", 0.7)
        )
        click.echo(json.dumps(response, indent=2))
    except Exception as e:
        logger.error(f"Error in completion: {e}")
        click.echo(f"Error: {e}", err=True)

@cli.command()
@click.option("--model", "-m", required=True, help="Model ID to use")
@click.option("--text", "-t", required=True, help="Text to embed")
def embeddings(model: str, text: str):
    """Generate embeddings"""
    try:
        response = model_manager.embeddings(
            model_id=model,
            input_texts=text
        )
        click.echo(json.dumps(response, indent=2))
    except Exception as e:
        logger.error(f"Error generating embeddings: {e}")
        click.echo(f"Error: {e}", err=True)

@cli.command()
@click.option("--directory", "-d", required=True, help="Directory containing documents")
@click.option("--chunk-size", "-c", type=int, help="Size of text chunks")
def load_documents(directory: str, chunk_size: Optional[int] = None):
    """Load documents into knowledge base"""
    try:
        knowledge_base.load_documents(
            directory=directory,
            chunk_size=chunk_size or config.get("chunk_size", 256)
        )
        click.echo("Documents loaded successfully")
    except Exception as e:
        logger.error(f"Error loading documents: {e}")
        click.echo(f"Error: {e}", err=True)

@cli.command()
@click.option("--query", "-q", required=True, help="Query text")
@click.option("--similarity-top-k", "-k", type=int, help="Number of similar documents to retrieve")
@click.option("--response-mode", "-m", help="Response synthesis mode")
def query_knowledge_base(query: str, similarity_top_k: Optional[int] = None, response_mode: Optional[str] = None):
    """Query knowledge base"""
    try:
        response = knowledge_base.query(
            query_text=query,
            similarity_top_k=similarity_top_k or config.get("similarity_top_k", 5),
            response_mode=response_mode or "default"
        )
        click.echo(json.dumps(response, indent=2))
    except Exception as e:
        logger.error(f"Error querying knowledge base: {e}")
        click.echo(f"Error: {e}", err=True)

@cli.command()
def list_collections():
    """List knowledge base collections"""
    try:
        collections = knowledge_base.list_collections()
        click.echo(json.dumps(collections, indent=2))
    except Exception as e:
        logger.error(f"Error listing collections: {e}")
        click.echo(f"Error: {e}", err=True)

@cli.command()
@click.option("--collection", "-c", required=True, help="Collection name to delete")
def delete_collection(collection: str):
    """Delete knowledge base collection"""
    try:
        knowledge_base.delete_collection(collection)
        click.echo(f"Collection {collection} deleted successfully")
    except Exception as e:
        logger.error(f"Error deleting collection: {e}")
        click.echo(f"Error: {e}", err=True)

@cli.command()
def system_status():
    """Get system resource information"""
    try:
        system_info = system_monitor.get_system_info()
        click.echo(json.dumps(system_info, indent=2))
    except Exception as e:
        logger.error(f"Error getting system resources: {e}")
        click.echo(f"Error: {e}", err=True)

if __name__ == "__main__":
    cli() 