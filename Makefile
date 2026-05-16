PYTHON ?= .venv/bin/python

.PHONY: install test-notebooks

install:
	uv venv .venv
	uv pip install --python $(PYTHON) -r requirements.txt

test-notebooks:
	$(PYTHON) scripts/execute_notebooks.py
