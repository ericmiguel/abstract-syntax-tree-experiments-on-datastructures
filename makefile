.PHONY: help install dev format lint type-check test check

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install the package
	uv sync

dev: ## Install development dependencies
	uv sync --dev

format: ## Format code with ruff
	uv run ruff format ./src ./tests

lint: ## Lint code with ruff
	uv run ruff check ./src ./tests --fix

type-check: ## Type check with pyright
	uv run pyright ./src ./tests

test: ## Run tests with pytest
	uv run pytest -v

check: format lint type-check test ## Run all checks
