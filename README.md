# fastapi-data-service
![CI](https://github.com/dounyaa/fastapi-data-service/actions/workflows/ci.yml/badge.svg)
[![Docker Image](https://img.shields.io/badge/Docker-ghcr.io%2Fdounyaa%2Ffastapi--data--service-blue?logo=docker)](https://github.com/dounyaa/fastapi-data-service/pkgs/container/fastapi-data-service)
![Coverage](https://img.shields.io/badge/coverage-%E2%89%A580%25-brightgreen)



Backend REST API built with FastAPI, designed with production-grade practices:
- Structured logging (JSON)
- Request ID middleware
- Centralized error handling
- Strict typing (mypy)
- Linting & formatting (ruff)
- Docker multi-stage build
- CI with GitHub Actions

---
## Deployed Version

Live production deployment:

`https://fastapi-data-service.onrender.com`

- Health check:

`curl https://fastapi-data-service.onrender.com/api/v1/health`

- Expected response:

`{"status":"ok"}`

- Request ID propagation example:

`curl -H "X-Request-ID: abc123" \
https://fastapi-data-service.onrender.com/api/v1/health`

- The response will include:

`X-Request-ID: abc123`

If no X-Request-ID is provided, the service automatically generates a 32-character unique ID and returns it in the response header.

---
## Features

- Health check endpoint
- Custom business exception handling
- Centralized validation error formatting
- Global 500 handler
- Request ID propagation (X-Request-ID)
- Environment-based configuration (Pydantic Settings)
- JSON structured logging
- Fully tested with pytest (async)
- Docker-ready
- CI validated on push & PR
- Production deployment on Render
  
---
## Architecture

src/

app/

api/v1/ → routes

core/ → settings, logger, errors, middleware

schemas/ → Pydantic models

tests/


---

## Configuration

Configuration is handled via environment variables using `pydantic-settings`.

Available variables:

| Variable        | Default                  |
|----------------|--------------------------|
| APP_NAME       | fastapi-data-service     |
| APP_VERSION    | 0.1.0                    |
| ENVIRONMENT    | dev                      |
| API_PREFIX     | /api/v1                  |
| LOG_LEVEL      | INFO                     |

---

## Run locally

Install dependencies:

`poetry install`

Run the app:

`poetry run uvicorn app.main:app --reload`

Test:

`poetry run pytest`

Lint & type check:

`poetry run ruff format --check .`

`poetry run ruff check .`

`poetry run mypy src/`


---

## Run with Docker

Build image:

`docker build -t fastapi-data-service .`


Run container:

`docker run -p 8000:8000 fastapi-data-service`


Health check:

`curl http://localhost:8000/api/v1/health`


---

## Observability

Each request is assigned a Request ID:
- Generated automatically if missing
- Propagated via `X-Request-ID`
- Included in structured logs

Example log:

```json
{
  "asctime": "...",
  "name": "app.api.v1.health",
  "levelname": "INFO",
  "request_id": "52e4f655c07c43ee875ef216c281f87e",
  "message": "Health check called"
}
```

---
## CI/CD
On every push / PR:

- Ruff format check
- Ruff lint
- Mypy strict type checking
- Pytest execution

On push to main:

- Docker image is built
- Image is pushed to GitHub Container Registry
- Render automatically deploys the new version
  
---
## Tech Stack
- FastAPI
- Pydantic v2
- Python 3.11
- Docker (multi-stage build)
- GitHub Actions CI
- Render deployment
- Structured logging (python-json-logger)
- ContextVar-based request tracking
