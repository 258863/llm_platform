#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import venv
from pathlib import Path

def create_virtual_environment():
    """Create a virtual environment if it doesn't exist."""
    venv_path = Path('venv')
    if not venv_path.exists():
        print('Creating virtual environment...')
        venv.create('venv', with_pip=True)
    else:
        print('Virtual environment already exists.')

def install_dependencies():
    """Install project dependencies."""
    print('Installing dependencies...')
    
    # Get the path to the virtual environment's pip
    if sys.platform == 'win32':
        pip_path = Path('venv/Scripts/pip')
    else:
        pip_path = Path('venv/bin/pip')
    
    # Install requirements
    subprocess.run([str(pip_path), 'install', '-r', 'requirements.txt'])
    subprocess.run([str(pip_path), 'install', '-e', '.'])

def create_directories():
    """Create necessary directories."""
    print('Creating directories...')
    directories = [
        'data',
        'data/knowledge_base',
        'logs',
        'config',
        'tests'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

def create_config_files():
    """Create configuration files if they don't exist."""
    print('Creating configuration files...')
    
    # Copy .env.example to .env if it doesn't exist
    env_example = Path('.env.example')
    env_file = Path('.env')
    if env_example.exists() and not env_file.exists():
        env_file.write_text(env_example.read_text())
        print('Created .env file from .env.example')

def setup_git():
    """Set up git configuration."""
    print('Setting up git...')
    
    # Initialize git repository if it doesn't exist
    if not Path('.git').exists():
        subprocess.run(['git', 'init'])
    
    # Create .gitignore if it doesn't exist
    gitignore = Path('.gitignore')
    if not gitignore.exists():
        gitignore.write_text('''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Testing
.coverage
htmlcov/
.pytest_cache/
.tox/
.nox/
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/

# Logs
logs/
*.log

# Local development
.env
.env.local
.env.*.local

# Data
data/
*.db
*.sqlite3

# Other
.DS_Store
Thumbs.db
''')

def main():
    """Set up the development environment."""
    try:
        create_virtual_environment()
        install_dependencies()
        create_directories()
        create_config_files()
        setup_git()
        print('\nDevelopment environment setup complete!')
        print('\nTo activate the virtual environment:')
        if sys.platform == 'win32':
            print('    .\\venv\\Scripts\\activate')
        else:
            print('    source venv/bin/activate')
    except Exception as e:
        print(f'Error setting up development environment: {e}')
        sys.exit(1)

if __name__ == '__main__':
    main() 