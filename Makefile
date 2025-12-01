.PHONY: help venv install install-dev run lint format clean test setup env cli cli-help cli-list cli-explain type-check

help:
	@echo "MathEqs - Physics Equation Explainer"
	@echo ""
	@echo "Available targets:"
	@echo "  venv          - Create Python virtual environment"
	@echo "  install       - Install dependencies from requirements.txt"
	@echo "  install-dev   - Install dependencies including dev tools (black, flake8, mypy)"
	@echo "  run           - Run the example application"
	@echo "  lint          - Run flake8 linter"
	@echo "  format        - Format code with black"
	@echo "  test          - Run pytest test suite"
	@echo "  type-check    - Run mypy type checker"
	@echo "  setup         - Setup environment (create .env from .env.example)"
	@echo "  cli-help      - Show CLI help message"
	@echo "  cli-list      - List all available equations"
	@echo "  cli-explain   - Example: make cli-explain EQUATION='F = ma'"
	@echo "  clean         - Remove __pycache__ and .pyc files"
	@echo "  help          - Show this help message"

venv:
	@echo "Creating Python 3.12 virtual environment..."
	python3.12 -m venv mathenv
	@echo ""
	@echo "Virtual environment created!"
	@echo "Activate with: source mathenv/bin/activate"

install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

install-dev: install
	@echo "Installing development dependencies..."
	pip install black flake8 mypy pytest

run:
	@echo "Running example application..."
	python example.py

lint:
	@echo "Running flake8 linter..."
	flake8 cli.py --max-line-length=120

format:
	@echo "Formatting code with black..."
	black *.py --line-length=120

test:
	@echo "Running pytest..."
	pytest -v --strict-markers tests/

type-check:
	@echo "Running mypy type checker..."
	@mypy cli.py

setup:
	@if [ ! -f .env ]; then \
		echo "Creating .env from .env.example..."; \
		cp .env.example .env; \
		echo "Please edit .env and set your GOOGLE_API_KEY"; \
	else \
		echo ".env already exists"; \
	fi

cli-help:
	@echo "MathEqs CLI - Physics Equation Explainer"
	@echo ""
	@python cli.py --help

cli-list:
	@python cli.py list-equations

cli-explain:
	@python cli.py explain $(EQUATION)

clean:
	@echo "Cleaning up cache files..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
