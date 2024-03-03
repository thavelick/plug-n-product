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

1. Set up a virtualenv
```
python -m venv venv
source venv/activate
```
2. Install dependencies and initialize the db
```
make setup
```
3. Run the local dev server
```
make dev
```
4. Run the tests
```
make test
```
5. Get help
```
make
```
