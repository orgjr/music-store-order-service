# Music Store Order Service

Order microservice for a music store. Exposes a REST API for managing orders (`order`)
and order items (`order_item`) with full CRUD, application identification and
monitoring endpoints, OpenAPI/Swagger/Redoc documentation extended to the whole domain,
Docker support, and a test suite organized by area (endpoints, functional, serializers
and model validation).

## Stack

| Technology          | Version | Purpose                                 |
| ------------------- | ------- | --------------------------------------- |
| Python              | 3.13    | Language                                |
| Django              | 6.1     | Web framework                           |
| Django REST Framework | 3.18  | REST API                                |
| drf-spectacular     | 0.30    | OpenAPI 3 documentation (Swagger/Redoc) |
| django-environ      | 0.14    | Configuration via environment variables |
| Docker              | —       | Containerization (image + compose)      |
| ruff / ty           | —       | Linting, formatting and type checking   |

## Project structure

```
├── config/                 # Project configuration
│   ├── settings/           #   Per-environment settings
│   │   ├── base.py         #   Shared base
│   │   ├── dev.py          #   Development
│   │   ├── prod.py         #   Production
│   │   └── test.py         #   Tests (in-memory database)
│   ├── urls.py             # Root routes (/api/v1/)
│   ├── asgi.py             # ASGI
│   └── wsgi.py             # WSGI
├── core/                   # Core app (index + health)
│   ├── urls.py             #   App routes (also mounts order and order_item)
│   ├── views.py            #   Endpoints (annotated with OpenAPI schemas)
│   └── uptime.py           #   Tracks process uptime
├── order/                  # Orders app
│   ├── migrations/         #   Database migrations (incl. 0002 — payment types)
│   ├── serializers.py      #   OrderSerializer (nested items)
│   ├── views.py            #   OrderViewSet (full CRUD)
│   ├── urls.py             #   Router under /api/v1/order/
│   └── models.py           #   Order model (UUID pk, status/payment choices)
├── order_item/             # Order items app
│   ├── serializers.py      #   OrderItemSerializer
│   ├── views.py            #   OrderItemViewSet (full CRUD)
│   ├── urls.py             #   Router under /api/v1/order-item/
│   └── models.py           #   OrderItem model (one product per order)
├── docs/openapi/           # OpenAPI documentation (one module per app/endpoint)
│   ├── config.py           #   Shared schema helpers
│   ├── core/               #   index and health schemas
│   ├── order/              #   create/list/retrieve/update/partial_update/destroy
│   └── order_item/         #   create/list/retrieve/update/partial_update/destroy
├── tests/                  # Test suite
│   ├── core/               #   endpoints + functional
│   ├── order/              #   endpoints + functional (model, serializers, validation)
│   └── order_item/         #   endpoints + functional (model, serializers, validation)
├── Dockerfile              # Application image
├── compose.yaml            # Local orchestration (port 8002)
├── entrypoint.sh           # Container entrypoint (migrate + runserver)
├── .dockerignore           # Exclusions for the image build
├── pyproject.toml          # ruff / ty configuration
├── manage.py               # CLI (uses config.settings.dev by default)
└── requirements.txt        # Pinned dependencies
```

## Prerequisites

- Python 3.13
- `pip`
- Docker (optional, for the containerized workflow)

## Environment setup

1. Create and activate the virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Prepare the environment variables:

   ```bash
   cp .env.example .env
   ```

4. Load the variables from `.env` and export `DEV_PROJECT_KEY` (required by Django's
   `SECRET_KEY`):

   ```bash
   $(grep -v '^#' .env | grep -Ev '^\s*$' | sed 's/^/export /')
   ```

   or export it manually:

   ```bash
   export DEV_PROJECT_KEY=project_secret_key
   ```

5. Apply migrations and start the server:

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

   The API will be available at `http://127.0.0.1:8000/api/v1/`.

### Environments

The project uses per-environment settings (inheriting from `base.py`). `manage.py`
defaults to `config.settings.dev`; for other environments, pass `--settings` or set
`DJANGO_SETTINGS_MODULE`:

| Environment | Settings               | Database      | Purpose                                 |
| ----------- | ---------------------- | ------------- | ---------------------------------------- |
| dev         | `config.settings.dev`  | `db.sqlite3`  | Development (DEBUG enabled)              |
| prod        | `config.settings.prod` | `DATABASE_URL` | Production (SSL/SMTP enabled)             |
| test        | `config.settings.test` | `:memory:`    | Test suite                               |

## Docker

Build and run the service with Docker Compose (mapped to host port **8002**):

```bash
docker compose up --build
```

The API becomes available at `http://127.0.0.1:8002/api/v1/`. The compose file enables
Docker's `develop.watch` mode, syncing local source changes into the container and
rebuilding when `requirements.txt` changes. The container entrypoint runs
`makemigrations`, `migrate` and then `runserver`.

## Endpoints

All endpoints live under the `/api/v1/` prefix.

| Method | Route                          | Description                                  |
| ------ | ------------------------------ | -------------------------------------------- |
| GET    | `/api/v1/`                     | Index — application identity (name, version, environment, URLs) |
| GET    | `/api/v1/health/`              | Health check — status, timestamp and process uptime |
| GET    | `/api/v1/order/`               | List orders                                  |
| POST   | `/api/v1/order/`               | Create order                                 |
| GET    | `/api/v1/order/{uuid}/`        | Retrieve order (includes nested items)       |
| PUT    | `/api/v1/order/{uuid}/`        | Update order                                 |
| PATCH  | `/api/v1/order/{uuid}/`        | Partial update order                         |
| DELETE | `/api/v1/order/{uuid}/`        | Delete order                                 |
| GET    | `/api/v1/order-item/`          | List order items                             |
| POST   | `/api/v1/order-item/`          | Create order item                            |
| GET    | `/api/v1/order-item/{id}/`     | Retrieve order item                          |
| PUT    | `/api/v1/order-item/{id}/`     | Update order item                            |
| PATCH  | `/api/v1/order-item/{id}/`     | Partial update order item                    |
| DELETE | `/api/v1/order-item/{id}/`     | Delete order item                            |
| GET    | `/api/v1/schema/`              | OpenAPI schema (JSON)                        |
| GET    | `/api/v1/docs/`                | Swagger UI                                   |
| GET    | `/api/v1/redoc/`               | Redoc                                        |

The `Order` model uses a UUID primary key and exposes `customer_id`, `customer_name`,
`price`, `payment_type` (`payment slip` / `credit card`) and `status` (`PENDING`,
`PAID`, `SHIPPED`, `DELIVERED`, `CANCELED`), with items nested in responses.
The `OrderItem` model references an `Order` and holds `product_code`, `product_name`,
`product_description`, `product_quantity` and `item_price`, constrained to one product
per order. Orders validate themselves through `full_clean()` on save.

Example index response:

```json
{
  "name": "Music Store Order Service",
  "version": "0.9.0",
  "description": "Service for managing orders in a music store, exposing a REST API for orders and order items.",
  "environment": "dev",
  "redoc_url": "/api/v1/redoc/",
  "health_url": "/api/v1/health/",
  "api_version": "V1"
}
```

Example health response:

```json
{
  "status": "ok",
  "timestamp": "2026-08-07T14:30:00.123456-03:00",
  "uptime_seconds": 42.12
}
```

## OpenAPI documentation

Documentation is written in a dedicated `docs/openapi/` module, one file per endpoint,
instead of inline in the views. Each view is annotated with `@extend_schema_view` /
`@extend_schema`, providing summary, description, tags, request/response bodies and
examples for the whole domain — core (index/health), order and order_item. The schema
is served at `/api/v1/schema/`, with Swagger UI at `/api/v1/docs/` and Redoc at
`/api/v1/redoc/`.

## Tests

The suite lives in the `tests/` package, organized by app and category, and runs with
the test settings (in-memory database, local cache):

```bash
python manage.py test tests --settings=config.settings.test
```

Add `--verbosity 2` to see each individual test. Coverage by area:

- `tests/core/endpoints` — core endpoint contract (status codes, fields, not-allowed
  methods, schema/swagger/redoc)
- `tests/core/functional` — functional behavior (uptime increases between requests,
  index URLs pointing to live endpoints, etc.)
- `tests/order/endpoints` and `tests/order_item/endpoints` — CRUD contract for every
  endpoint (list, create, retrieve, update, partial update, delete)
- `tests/order/functional` and `tests/order_item/functional` — model behavior,
  serializer output and model validation (choices, constraints, required fields)

## Code quality

Configuration lives in `pyproject.toml`.

- **ruff** — linting and formatting:

  ```bash
  ruff check .        # lint
  ruff format .       # formatting
  ```

- **ty** — type checking (with Django-specific rules to silence false positives on
  model metaclass attributes).

- **djlint / djhtml** — HTML template linting (applicable once templates exist).

## Roadmap — next milestone

- **Authentication / authorization** (e.g., JWT) for protected endpoints.
- **Pagination and filtering** tuning for list endpoints.
- **Production database** integration (PostgreSQL) in `compose.yaml`.
- **CI pipeline** running lint, type checks and tests on every push.

## Contributing

Study/delivery project. Feel free to open issues and pull requests.

## License

MIT.