PYTHON := python
PIP := pip3
VENV := venv
ACTIVATE := source $(VENV)/bin/activate

.PHONY: help check setup install lint run clean

help:
	@echo "Available commands:"
	@echo "  make check     -> Verify prerequisites (python, pip, git)"
	@echo "  make setup     -> Create virtual environment and install dependencies"
	@echo "  make install   -> Install dependencies from requirements.txt"
	@echo "  make lint      -> Run pre-commit hooks on all files"
	@echo "  make run       -> Run main script (adjust as needed)"
	@echo "  make clean     -> Remove temporary and cache files"

check:
	@command -v $(PYTHON) >/dev/null 2>&1 || { echo >&2 "❌ Python is not installed. Please install it first."; exit 1; }
	@command -v $(PIP) >/dev/null 2>&1 || { echo >&2 "❌ pip is not installed. Please install it first."; exit 1; }
	@command -v git >/dev/null 2>&1 || { echo >&2 "❌ git is not installed. Please install it first."; exit 1; }
	@$(PYTHON) -c "import sys; exit(0) if sys.version_info[:2] == (3, 12) else exit(1)" || { echo >&2 "❌ Python 3.12 is required. Current version is: $$($(PYTHON) --version)"; exit 1; }
	@echo "✅ All prerequisites are installed."

setup:
	$(PYTHON) -m venv $(VENV)
	source ./venv/Scripts/activate
	$(VENV)/Scripts/python -m pip install --upgrade pip
	$(VENV)/Scripts/pip install -r requirements.txt
	$(VENV)/Scripts/pre-commit install
	@mkdir -p reports/
	@mkdir -p logs/
	@echo "✅ Setup Completed."

lint:
	$(VENV)/Scripts/pre-commit run --all-files

run:
	$(VENV)/Scripts/python src/main.py $(ARGS) | tee ./logs/run_$(shell date +%Y-%m-%d_%H-%M-%S).log

clean:
	@echo "🧹 Cleaning cache..."
	@find . -type d -name "__pycache__" -exec rm -r {} +
	@rm -rf .pytest_cache .mypy_cache .coverage htmlcov
	@echo "✅ Cache cleaned successfully"
	@echo "🧹 Cleaning logs and reports..."
	@rm -rf ./logs/* ./reports/*
	@echo "✅ Logs and reports cleaned successfully"

load:
	#In windows this make only works on git shell
	source venv/Scripts/activate
