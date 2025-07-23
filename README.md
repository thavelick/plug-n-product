# Plug-n-Product

A Template to quickstart Flask apps

## Goals

Eventually this template should include:
* Subscription purchase with Stripe

## What's done now

* CSS framework - pico.css
* htmx for fancy front-end stuff
* SQLite DB support
* Testing with pytest across cpus and with coverage reporting
* Registration and Login

## Quick-start

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

1. Install uv (if you haven't already):
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```
2. Initialize the database:
```
make setup
```
3. Run the local dev server:
```
make dev
```
4. Run the tests:
```
make test
```
5. Get help:
```
make
```

## Development

- `make update` - Update all dependencies to their latest versions
- `make test-with-coverage` - Run tests with coverage reporting
- `make test-dist` - Run tests across multiple CPUs
