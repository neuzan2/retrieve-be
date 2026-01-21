# FastAPI Production-Ready Backend

This is a production-ready FastAPI backend project, initialized with best practices.

## Tech Stack

- Python >= 3.12
- FastAPI >= 0.114
- Pydantic v2
- Async SQLAlchemy 2.x
- PostgreSQL
- Alembic (migrations)
- Redis (caching + background tasks)
- Celery (async workers)
- UV (dependency + lockfile management)
- Ruff (format + lint)
- MyPy (type checking)
- Pytest (testing)
- Docker + Docker Compose

## Project Structure

```
app/
├── api/
│   └── v1/
│       ├── health/
│       └── users/
├── core/
│   ├── middleware/
│   ├── security/
│   └── exceptions/
├── db/
│   └── migrations/
├── models/
├── schemas/
├── services/
├── repositories/
└── tests/
main.py
```

## Getting Started

### Prerequisites

- Python 3.12+
- Docker
- `uv` (installed via `pip install uv`)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2.  **Create a virtual environment and install dependencies:**

    ```bash
    uv venv
    source .venv/bin/activate
    uv pip install -e .[dev]
    ```

3.  **Set up the environment variables:**

    Copy the `.env.example` file to `.env`. This file will be used by the Docker containers.

    ```bash
    cp .env.example .env
    ```

    For local development and running migrations on the host, create a `.env.local` file with database settings pointing to `localhost`:

    ```bash
    cp .env.example .env.local
    # Edit .env.local to change POSTGRES_HOST to localhost and POSTGRES_PORT to 5432
    ```
    Ensure `POSTGRES_HOST=localhost` and `POSTGRES_PORT=5432` in your `.env.local` if you plan to run Alembic migrations directly on your host machine against the Dockerized database.

4.  **Install pre-commit hooks:**

    ```bash
    pre-commit install
    ```

### Using the Makefile

This project includes a `Makefile` to simplify common development tasks.

```bash
make help
```

### Running the application with Docker

To build and run the application using Docker Compose:

```bash
make docker-build
make docker-up
```
The API will be available at `http://localhost:8000`.
The PostgreSQL database will be accessible at `localhost:5432`.

### Running the application locally (for development)

Ensure you have activated your virtual environment (`source .venv/bin/activate`).

```bash
make run
```

### Running migrations (on host against Dockerized DB)

To create a new migration:

```bash
make makemigrations m="Your migration message"
```
This command will create a new migration file in `app/db/migrations/versions/`. These files will be automatically picked up by Docker when the image is rebuilt or containers are restarted.

To apply the migrations:

```bash
make migrate
```

### Running Tests

```bash
make test
```

### Linting and Formatting

```bash
make lint
make format
```
