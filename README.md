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
- `uv`

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

    Copy the `.env.example` file to `.env` and update the values as needed.

    ```bash
    cp .env.example .env
    ```

4.  **Install pre-commit hooks:**

    ```bash
    pre-commit install
    ```

### Running the application with Docker

To run the application with Docker Compose, use the following command:

```bash
docker-compose up -d
```

The API will be available at `http://localhost:8000`.

### Running the application locally

To run the application locally, use the following command:

```bash
uvicorn main:app --reload
```

### Running migrations

To create a new migration, use the following command:

```bash
alembic revision --autogenerate -m "Your migration message"
```

To apply the migrations, use the following command:

```bash
alembic upgrade head
```
