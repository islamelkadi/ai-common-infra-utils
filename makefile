# =============================================================================
# ai-infra-common — Shared Python Utilities
# =============================================================================

.DEFAULT_GOAL := help
SHELL := /bin/bash

VENV_DIR := .venv
PYTHON   := $(VENV_DIR)/bin/python
PIP      := $(VENV_DIR)/bin/pip
IMAGE    := ai-infra-common
TAG      := latest

.PHONY: help venv install lint format test coverage clean clean-venv docker-build docker-test all

## help: Show available targets
help:
	@echo ""
	@echo "ai-infra-common — Shared Python Utilities"
	@echo ""
	@echo "Usage: make <target>"
	@echo ""
	@grep -E '^## ' $(MAKEFILE_LIST) | sed 's/^## /  /' | column -t -s ':'
	@echo ""

## venv: Create virtual environment and install all dependencies
venv: $(VENV_DIR)/bin/activate

$(VENV_DIR)/bin/activate: requirements.txt pyproject.toml
	python3 -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install -e .
	@touch $(VENV_DIR)/bin/activate

## install: Install package in editable mode with dev deps
install: venv

## lint: Run ruff linter
lint: venv
	$(VENV_DIR)/bin/ruff check src/ tests/

## format: Auto-format code with ruff
format: venv
	$(VENV_DIR)/bin/ruff format src/ tests/

## test: Run tests with pytest
test: venv
	$(PYTHON) -m pytest -v

## coverage: Run tests with coverage report
coverage: venv
	$(PYTHON) -m pytest --cov=src --cov-report=term --cov-report=xml -v

## clean: Remove build artifacts and caches
clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache .ruff_cache coverage.xml
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

## clean-venv: Remove the virtual environment
clean-venv:
	rm -rf $(VENV_DIR)

## docker-build: Build the Docker image
docker-build:
	docker build -t $(IMAGE):$(TAG) .

## docker-test: Run tests inside Docker
docker-test: docker-build
	docker run --rm $(IMAGE):$(TAG) pytest -v

## all: Install, lint, and test
all: install lint test
