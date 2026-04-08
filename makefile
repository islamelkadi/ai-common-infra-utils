# =============================================================================
# ai-infra-common — Shared Python Utilities
# =============================================================================

.DEFAULT_GOAL := help
SHELL := /bin/bash

VENV_DIR := .venv
PYTHON3  := $(shell command -v python3.13 || command -v python3.12 || command -v python3.11 || command -v python3.10 || echo python3)
PIP      := $(VENV_DIR)/bin/pip
IMAGE    := ai-infra-common
TAG      := latest
RUNTIME  ?= finch

.PHONY: help venv install lint format test coverage clean clean-venv docker-build docker-test all

## help: Show available targets
help:
	@echo ""
	@echo "ai-infra-common — Shared Python Utilities"
	@echo ""
	@echo "Usage: make <target>"
	@echo ""
	@awk '/^## / { sub(/^## /, ""); split($$0, a, ": "); printf "  \033[36m%-15s\033[0m %s\n", a[1], a[2] }' $(MAKEFILE_LIST)
	@echo ""

## venv: Create virtual environment and install all dependencies
venv: $(VENV_DIR)/bin/activate

$(VENV_DIR)/bin/activate: pyproject.toml
	$(PYTHON3) -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip
	$(PIP) install -e ".[dev]"
	@touch $(VENV_DIR)/bin/activate

## install: Install package in editable mode with dev deps
install: venv

## lint: Run ruff linter
lint: venv
	$(VENV_DIR)/bin/ruff check ai_infra_common/ tests/

## format: Auto-format code with ruff
format: venv
	$(VENV_DIR)/bin/ruff format ai_infra_common/ tests/

## test: Run tests with pytest
test: venv
	$(PYTHON3) -m pytest -v

## coverage: Run tests with coverage report
coverage: venv
	$(PYTHON3) -m pytest --cov=ai_infra_common --cov-report=term --cov-report=xml -v

## clean: Remove build artifacts and caches
clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache .ruff_cache coverage.xml
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

## clean-venv: Remove the virtual environment
clean-venv:
	rm -rf $(VENV_DIR)

## docker-build: Build the container image
docker-build:
	$(RUNTIME) build -t $(IMAGE):$(TAG) .

## docker-test: Run tests inside container
docker-test: docker-build
	$(RUNTIME) run --rm -v $(PWD)/ai_infra_common:/app/ai_infra_common -v $(PWD)/tests:/app/tests $(IMAGE):$(TAG) pytest -v

## all: Install, lint, and test
all: install lint test
