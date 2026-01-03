.PHONY: help setup-env test del-env

help:
	@echo "Available targets:"
	@echo "  make setup-env  - Create virtual environment (.venv) with Python 3.12 and install requirements"
	@echo "  make test       - Run test commands with sublist3r.py"
	@echo "  make del-env    - Remove virtual environment (.venv)"
	@echo "  make help       - Show this help message"

setup-env:
	@echo "Creating virtual environment with Python 3.12..."
	python3.12 -m venv .venv
	@echo "Installing requirements..."
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt
	@echo "Virtual environment created and requirements installed!"

test:
	@echo "Running test 1: python sublist3r.py -v -d google.com"
	python sublist3r.py -v -d google.com
	@echo ""
	@echo "Running test 2: python sublist3r.py -v -d example.com"
	python sublist3r.py -v -d example.com

del-env:
	@echo "Removing virtual environment..."
	rm -rf .venv
	@echo "Virtual environment removed!"

