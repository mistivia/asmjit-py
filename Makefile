PYTHON := .venv/bin/python
EXT_SUFFIX := $(shell $(PYTHON) -c "import sysconfig; print(sysconfig.get_config_var('EXT_SUFFIX'))")
PYTHON_INCLUDE := $(shell $(PYTHON) -c "import sysconfig; print(sysconfig.get_path('include'))")
UTILS_EXT := build/local/asmjit/utils$(EXT_SUFFIX)

.PHONY: all test benchmark typecheck

all:
	$(PYTHON) -m build

$(UTILS_EXT): src/asmjit/utils.c
	mkdir -p build/local/asmjit
	$(CC) -O3 -shared -fPIC -I$(PYTHON_INCLUDE) $< -o $@

test: $(UTILS_EXT)
	PYTHONPATH=build/local:src:tests $(PYTHON) tests/run.py

benchmark: $(UTILS_EXT)
	PYTHONPATH=build/local:src $(PYTHON) benchmark/sqrt.py

typecheck:
	pyright
