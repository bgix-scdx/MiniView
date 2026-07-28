.SILENT:
.PHONY: install run debug clean lint lint-strict

MAIN := MiniView
VENV := $(MAIN)-venv
PYTHON := $(VENV)/bin/python3
PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/pytest
FLAKE8 := $(VENV)/bin/flake8
MYPY := $(VENV)/bin/mypy
ModuleFile := MiniView

install:
	@echo "Installing Project $(MAIN)"
	python3 -m venv $(VENV)
	chmod 777 $(VENV)/bin/activate 
	$(VENV)/bin/activate
	$(PIP) install --upgrade pip
	$(PIP) install pytest flake8 mypy poetry uv pydantic numpy
	$(VENV)/bin/uv sync
run:
	echo "Running Project $(MAIN)"
	$(VENV)/bin/uv run python -m tester

debug:
	$(PYTHON) -m pdb $(MAIN)

lclean:
	rm -rf __pycache__ src/__pycache__ .mypy_cache .pytest_cache $(ModuleFile)/__pycache__ .vscode $(RESULTFILE) llm_sdk/__pycache__

clean:
	rm -rf $(VENV)
	rm -rf __pycache__ src/__pycache__ .mypy_cache .pytest_cache $(ModuleFile)/__pycache__ .vscode $(RESULTFILE) .venv llm_sdk/__pycache__ poetry.lock uv.lock

lint:
	$(MYPY) ./MiniView --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
	$(FLAKE8) ./MiniView

lint-strict:
	$(MYPY) ./MiniView --strict
	$(FLAKE8) ./MiniView