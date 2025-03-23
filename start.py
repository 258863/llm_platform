#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description='Start the LLM Platform')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=8000, help='Port to bind to')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--workers', type=int, default=4, help='Number of workers')
    return parser.parse_args()

def setup_environment():
    # Create necessary directories
    directories = [
        'data',
        'data/knowledge_base',
        'logs',
        'config'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    # Set up environment variables
    os.environ.setdefault('PYTHONPATH', str(Path(__file__).parent))
    
    # Load environment variables from .env file if it exists
    env_file = Path(__file__).parent / '.env'
    if env_file.exists():
        from dotenv import load_dotenv
        load_dotenv(env_file)

def main():
    args = parse_args()
    setup_environment()
    
    # Import after environment setup
    from llm_platform.ui.web import WebUI
    
    # Start the application
    app = WebUI()
    app.run(
        host=args.host,
        port=args.port,
        debug=args.debug,
        workers=args.workers
    )

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nShutting down...')
        sys.exit(0)
    except Exception as e:
        print(f'Error: {e}')
        sys.exit(1) 