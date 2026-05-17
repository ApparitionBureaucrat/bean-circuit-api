# Bean Circuit API

Bean Circuit API is a small Django application that curates neighborhood coffee routes.
It provides a concise JSON API for:

- Registering coffee shops
- Building named circuits that connect multiple shops in a stop order
- Generating AI assisted route stories with PydanticAI

The project uses Django 5 and a layered layout with models, schemas, services, and views.

## Requirements

- Python 3.13
- Django 5
- PostgreSQL is optional; default config uses SQLite locally

## Setup

1. Copy the sample environment file and adjust values:

```bash
cp .env.example .env
```

2. Create a Python 3.13 environment and install packages:

```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

3. Apply database schema:

```bash
python manage.py migrate
```

4. Start the development server:

```bash
python manage.py runserver
```

## API shape

- `GET /api/v1/shops/`
- `POST /api/v1/shops/`
- `GET /api/v1/circuits/`
- `POST /api/v1/circuits/`
- `GET /api/v1/circuits/<id>/story/`
- `POST /api/v1/circuits/<id>/story/`

Each write endpoint validates request bodies with Pydantic schemas and returns JSON
objects with deterministic fields for client integration.

## Configuration files

- `pyproject.toml` for project/dependency metadata and tool configuration (pytest, Ruff, Pyright)
- `.env.example` with environment defaults and AI key placeholder
- `.gitignore` for local build and IDE artifacts
- `manage.py`, Django settings, URL configuration, and WSGI/ASGI app bootstrap

## Testing

The test suite lives under `circuits/tests/` and covers schema validation and service
story behavior.
