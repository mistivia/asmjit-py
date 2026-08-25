.PHONY: all test typecheck

all:
	.venv/bin/python -m build

test:
	PYTHONPATH=src:tests .venv/bin/python tests/run.py

typecheck:
	pyright
