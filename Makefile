PYTHON ?= python

.PHONY: help install test snapshot transcript-snapshot protocol clean

help:
	@echo "make install             - install package in editable mode with dev extras"
	@echo "make test                - run pytest"
	@echo "make snapshot            - render the example JSON intake to stdout"
	@echo "make transcript-snapshot - render the example transcript to stdout"
	@echo "make protocol            - render the intake question protocol to stdout"
	@echo "make clean               - remove build/test caches"

install:
	pip install -e ".[dev]"

test:
	pytest

snapshot:
	$(PYTHON) -m voice_to_evidence examples/intake_example.json

transcript-snapshot:
	$(PYTHON) -m voice_to_evidence transcript examples/transcript_example.txt --incident-id VTE-2026-0002 --agent-name support-triage-agent

protocol:
	$(PYTHON) -m voice_to_evidence protocol

clean:
	rm -rf build dist *.egg-info .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
