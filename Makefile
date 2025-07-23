SHELL := /bin/bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

.DEFAULT_GOAL := help
.PHONY: help

TAB := '%-20s'
bold := $(shell tput bold)
underline := $(shell tput smul)
reset := $(shell tput sgr0)

dev: # Start local development server
	@echo "Starting dev environment..."
	uv run flask --app application run --debug

update: # Update dependencies
	@echo "Updating dependencies..."
	uv sync -U

setup: # Setup local dev environment
	@echo "Initializing database..."
	uv run flask --app application init-db
	@echo "Setup complete."

test: # Run tests
	@echo "Running tests..."
	uv run pytest
	@echo "Tests complete."

test-with-coverage: # Run tests with coverage
	@echo "Running tests with coverage..."
	uv run pytest --cov=application --cov-report=html --cov-report=term

test-dist: # Run tests across CPUs
	@echo "Running tests with dist..."
	uv run pytest -n auto
	@echo "Tests complete."

help: # Show available commands
	@printf '\n'
	@printf '    $(underline)Available make commands:$(reset)\n\n'
	@grep -E '^([a-zA-Z0-9_-]+\.?)+:.+#.+$$' $(MAKEFILE_LIST) \
		| sed 's/:.*#/: #/g' \
		| awk 'BEGIN {FS = "[: ]+#[ ]+"}; \
		{printf "    make $(bold)$(TAB)$(reset) # %s\n", \
			$$1, $$2}'
	@grep -E '^([a-zA-Z0-9_-]+\.?)+:( +\w+-\w+)*$$' $(MAKEFILE_LIST) \
		| grep -v help \
		| awk 'BEGIN {FS = ":"}; \
		{printf "    make $(bold)$(TAB)$(reset)\n", \
			$$1}' || true
	@echo -e ""