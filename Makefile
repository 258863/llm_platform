.PHONY: install test lint format clean run docs

# Python interpreter to use
PYTHON = python

# Install dependencies
install:
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) -m pip install -e .

# Run tests
test:
	$(PYTHON) -m pytest tests/ -v

# Run linting
lint:
	$(PYTHON) -m flake8 llm_platform/
	$(PYTHON) -m black --check llm_platform/

# Format code
format:
	$(PYTHON) -m black llm_platform/

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/

# Run the application
run:
	$(PYTHON) -m llm_platform

# Generate documentation
docs:
	$(PYTHON) -m pdoc --html --output-dir docs/ llm_platform/

# Create virtual environment
venv:
	$(PYTHON) -m venv venv
	. venv/bin/activate && pip install -r requirements.txt

# Run type checking
typecheck:
	$(PYTHON) -m mypy llm_platform/

# Run security checks
security:
	$(PYTHON) -m bandit -r llm_platform/

# Run all checks
check: lint typecheck security test

# Default target
all: install check 