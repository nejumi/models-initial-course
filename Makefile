PYTHON ?= .venv/bin/python

.PHONY: install test test-notebooks test-offline

install:
	uv venv .venv
	uv pip install --python $(PYTHON) -r requirements.txt

test:
	$(PYTHON) -m unittest discover -s tests -v

test-notebooks:
	$(PYTHON) scripts/execute_notebooks.py

test-offline:
	$(PYTHON) scripts/execute_notebooks.py --offline
