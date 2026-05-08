PYTHON ?= python

.PHONY: help install test snapshot clean

help:
	@echo "make install   - install package in editable mode with dev extras"
	@echo "make test      - run pytest"
	@echo "make snapshot  - render the example intake to stdout"
	@echo "make clean     - remove build/test caches"

install:
	pip install -e ".[dev]"

test:
	pytest

snapshot:
	$(PYTHON) -m voice_to_evidence examples/intake_example.json

clean:
	rm -rf build dist *.egg-info .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
