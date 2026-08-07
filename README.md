# Music Store Order Service

Order microservice for a music store. Exposes a REST API for managing orders (`order`)
and order items (`order_item`), with application identification and monitoring
endpoints, OpenAPI/Swagger/Redoc documentation, and a test suite organized by area
(endpoints and functional).

## Stack

| Technology          | Version | Purpose                                 |
| ------------------- | ------- | --------------------------------------- |
| Python              | 3.13    | Language                                |
| Django              | 6.1     | Web framework                           |
| Django REST Framework | 3.18  | REST API                                |
| drf-spectacular     | 0.30    | OpenAPI 3 documentation (Swagger/Redoc) |
| django-environ      | 0.14    | Configuration via environment variables |

## Project structure

```
├── config/                 # Project configuration
│   ├── settings/           #   Per-environment settings
│   │   ├── base.py         #   Shared base
│   │   ├── dev.py          #   Development
│   │   ├── prod.py         #   Production
│   │   └── test.py         #   Tests (in-memory database)
│   ├── urls.py             # Root routes
│   ├── asgi.py             # ASGI
│   └── wsgi.py             # WSGI
├── core/                   # Core app (index + health)
│   ├── urls.py             #   App routes
│   ├── views.py            #   Endpoints
│   └── uptime.py           #   Tracks process uptime
├── order/                  # Orders app (model created; endpoints planned)
├── order_item/             # Order items app (model created; endpoints planned)
├── testes/                 # Test suite
│   ├── core/
│   │   ├── endpoints/      #   Endpoint/contract tests
│   │   └── functional/     #   Functional tests
│   ├── order/functional/   #   Order model tests
│   └── order_item/functional/  # OrderItem model tests
├── manage.py               # CLI (uses config.settings.dev by default)
└── requirements.txt        # Pinned dependencies
```

## Prerequisites

- Python 3.13
- `pip`

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

## Endpoints

All current endpoints live under the `/api/v1/` prefix.

| Method | Route                  | Description                                  |
| ------ | ---------------------- | -------------------------------------------- |
| GET    | `/api/v1/`             | Index — application identity (name, version, environment, URLs) |
| GET    | `/api/v1/health/`      | Health check — status, timestamp and process uptime |
| GET    | `/api/v1/schema/`      | OpenAPI schema (JSON)                        |
| GET    | `/api/v1/docs/`        | Swagger UI                                   |
| GET    | `/api/v1/redoc/`       | Redoc                                        |
| —      | `/order/`, `/order-item/` | Orders and order items (planned; models already exist) |

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

## Tests

The suite lives in the `testes/` package, organized by app and category, and runs with
the test settings (in-memory database, local cache):

```bash
python manage.py test testes --settings=config.settings.test
```

Add `--verbosity 2` to see each individual test. Coverage by area:

- `testes/core/endpoints` — endpoint contract (status codes, fields, not-allowed
  methods, schema/swagger/redoc)
- `testes/core/functional` — functional behavior (uptime increases between requests,
  index URLs pointing to live endpoints, etc.)
- `testes/order/functional` and `testes/order_item/functional` — model tests

## Code quality

- **ruff** — linting and formatting:

  ```bash
  ruff check .        # lint
  ruff format .       # formatting
  ```

- **djlint / djhtml** — HTML template linting (applicable once templates exist).

## Roadmap — next milestone

- **Endpoint configuration** for `order` and `order_item` (DRF `ViewSet` CRUD), with
  routes under `/api/v1/`.
- **Detailed OpenAPI documentation** (`drf-spectacular`): `@extend_schema` annotations
  per endpoint (responses, examples, tags) and, if needed, organization in a dedicated
  `docs/api/` module.
- **Docker / Docker Compose** — application image and local orchestration (app + database).
- **Test suite expansion** — covering the new endpoints and error scenarios.

## Contributing

Study/delivery project. Feel free to open issues and pull requests.

## License

MIT.