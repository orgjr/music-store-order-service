# Music Store Order Service

Order microservice for a music store. It processes a checkout by obtaining customer,
cart and catalog data from their respective services, validates the cart against the
catalog, and persists an order with immutable item snapshots. It also exposes
application identification, monitoring and OpenAPI/Swagger/Redoc documentation.

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
│   ├── urls.py             #   App routes (mounts order)
│   ├── views.py            #   Endpoints (annotated with OpenAPI schemas)
│   └── uptime.py           #   Tracks process uptime
├── order/                  # Orders app
│   ├── migrations/         #   Database migrations (incl. 0002 — payment types)
│   ├── serializers.py      #   Checkout request and nested order response serializers
│   ├── services/process.py #   Checkout orchestration and persistence
│   ├── views.py            #   OrderViewSet (create, query and delete)
│   ├── urls.py             #   Router under /api/v1/order/
│   └── models.py           #   Order model (UUID pk, customer snapshot and timestamps)
├── order_item/             # Order items app
│   └── models.py           #   Persisted catalog snapshot (not exposed independently)
├── docs/openapi/           # OpenAPI documentation (one module per app/endpoint)
│   ├── config.py           #   Shared schema helpers
│   ├── core/               #   index and health schemas
│   └── order/              #   create/list/retrieve/destroy
├── helpers/                 # HTTP clients for customer, cart and catalog services
├── validators/              # Catalog price and stock validation
├── tests/                  # Test suite
│   ├── core/               #   endpoints + functional
│   ├── order/              #   endpoints + functional (model, serializers, validation)
│   └── order_item/         #   model validation for internal order snapshots
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

4. Fill in `DEV_PROJECT_KEY` and the downstream service URLs in `.env`.
   Django loads this file automatically. `CUSTOMER_SERVICE_URL`, `CART_SERVICE_URL`
   and `CATALOG_SERVICE_URL` must point to the services used when an order is created.

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
| DELETE | `/api/v1/order/{uuid}/`        | Delete order                                 |
| GET    | `/api/v1/schema/`              | OpenAPI schema (JSON)                        |
| GET    | `/api/v1/docs/`                | Swagger UI                                   |
| GET    | `/api/v1/redoc/`               | Redoc                                        |

`POST /api/v1/order/` accepts the checkout references below. It does not receive
customer, cart or item snapshots directly.

```json
{
  "customer": "5e8b0c11-d2f3-4a5b-8c9d-1e2f3a4b5c6d",
  "cart": "1a2b3c4d-5e6f-4a7b-8c9d-0e1f2a3b4c5d",
  "payment_type": "PS"
}
```

`payment_type` is `PS` (Payment slip) or `CC` (Credit card). During processing, the
service fetches the customer and cart, checks every cart item against the catalog's
current price and stock, and writes the order atomically. A failed dependency,
validation or database operation returns `500` with `{"order": "Order could not be
processed"}`.

Orders use UUID primary keys and expose the customer snapshot (`customer_id`,
`customer_name`, optional `customer_email`, `customer_doc`), total `price`, displayed
payment type, status, `created_at` and `updated_at`. Items are nested in responses and
contain their UUID, product code, name, catalog URL, unit price, quantity and line
price. They are internal order snapshots: no standalone `order_item` endpoint exists.

Example index response:

```json
{
  "name": "Music Store Order Service",
  "version": "0.9.0",
  "description": "Service for processing music-store checkouts and managing their orders.",
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
instead of inline in the views. Each public operation is annotated with
`@extend_schema_view` / `@extend_schema`, providing summary, description, tags,
request/response bodies and examples for core (index/health) and orders. The schema is
served at `/api/v1/schema/`, with Swagger UI at `/api/v1/docs/` and Redoc at
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
- `tests/order/endpoints` — order endpoint contract (list, checkout creation,
  retrieve and delete)
- `tests/order/functional` — model behavior, serializer output and model validation

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
