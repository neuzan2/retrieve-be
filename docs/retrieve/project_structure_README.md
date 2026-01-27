
# Project Architecture & File Structure Documentation

## 1. Overview

This document describes the architecture, folder structure, and responsibilities of all files and directories in the **Retrieve** project. The project follows a **Modular Monolith architecture inspired by Domain-Driven Design (DDD)** and is built using **FastAPI**, **SQLAlchemy**, **Alembic**, **Celery**, and containerized using **Docker**.

The primary goals of this structure are:

- Clear separation of concerns
- Feature-based modularity
- Scalability without premature microservices
- Testability and maintainability

---

## 2. Root Directory (`retrieve/`)

### 2.1 Configuration & Build Files

| File | Description |
| --- | --- |
| `pyproject.toml` | Defines project metadata, dependencies, and build configuration (compatible with uv/poetry). |
| `Dockerfile` | Builds the FastAPI application container for deployment. |
| `docker-compose.yml` | Orchestrates local development services such as API, database, Redis, etc. |
| `Makefile` | Provides developer-friendly commands (e.g., run, test, migrate). |
| `alembic.ini` | Alembic configuration file defining database URL, migration paths, and logging. |

---

## 3. Documentation (`docs/`)

Contains all project-level documentation.

| File | Description |
| --- | --- |
| `PROJECT.md` | High-level overview of the project, architecture, and conventions. |
| `PROJECT_DOCUMENTATION.md` | Detailed functional and technical documentation. |
| `ALEMBIC.md` | Database migration strategy and Alembic usage guidelines. |
| `db-schema.md` | Database schema definitions and relationships. |

---

## 4. Logs (`logs/`)

Stores application logs during local development or debugging. In production environments, logs are expected to be streamed to stdout or external log aggregators such as AWS CloudWatch or ELK.

> Note: This directory should be excluded from version control.
> 

---

## 5. Scripts (`scripts/`)

Contains utility and automation scripts that are not part of runtime application code.

### 5.1 Root Scripts

| File | Description |
| --- | --- |
| `init.py` | Bootstrapping or initialization logic for the project. |
| `startapp.py` | Utility script to scaffold a new feature module following project conventions. |

### 5.2 Alembic Scripts (`scripts/alembic/`)

Custom Alembic environment separated from application runtime code.

| File | Description |
| --- | --- |
| `env.py` | Configures Alembic context, database engine, and metadata. |
| `script.py.mako` | Template used for generating new migration files. |
| `versions/` | Contains all generated migration scripts. |

---

## 6. Source Code (`src/`)

This directory contains all runtime application code.

### 6.1 Application Entry Point

| File | Description |
| --- | --- |
| `main.py` | Creates the FastAPI application instance, registers middleware, routers, and startup/shutdown events. |

---

## 7. Application Modules (`src/app/`)

Holds all feature-based modules. Each feature is self-contained and follows a consistent internal structure.

```
<feature_app>/
 ├── enum/
 ├── models/
 ├── schemas/
 ├── repositories/
 ├── services/
 └── api/

```

### 7.1 Models (`models/`)

- SQLAlchemy ORM models
- Database table mappings
- No business logic

### 7.2 Schemas (`schemas/`)

- Pydantic models
- Request and response validation
- API data contracts

### 7.3 Repositories (`repositories/`)

- Data access layer
- Encapsulates all database queries
- Abstracts persistence logic from services

### 7.4 Services (`services/`)

- Application and business logic
- Coordinates repositories and domain rules
- Stateless and testable

### 7.5 API (`api/v1/`)

- FastAPI route definitions
- Dependency injection
- Delegates logic to services only

What needs to be consider while creating endpoints?

Example:

```jsx
...
from fastapi.router import APIRouter

router = APIRouter(
	prefix="/<router-prefix>",
	tags=["<proper-tag-name>"]
)

@router.get("/")
def get_list():
	return [{"message": "Successful"}]
```

We need to create `APIRouter` instance with prefix and tags supplied. While creating api we need to use `router` instead of `app` from `main.py` file.

### 7.5 Enum (`enum/`)



---

## 8. Configuration Layer (`src/config/`)

This folder contains **infrastructure and environment-specific configuration**. No business logic should exist here.

### 8.1 `config.py`

- Centralized application settings
- Uses environment variables for configuration
- Defines database URLs, secrets, debug flags, and service endpoints

Typical responsibilities:

- Loading `.env` values
- Environment-based configuration (dev/staging/prod)
- Strong typing of settings

---

### 8.2 `logging.py`

- Central logging configuration for the entire application
- Defines log formatters, handlers, and log levels
- Supports structured logging
- Designed to integrate with log aggregation services (e.g., AWS CloudWatch)

Responsibilities:

- Configure root logger
- Enable JSON or structured logs if required
- Standardize log output across API, Celery, and background tasks

---

### 8.3 `celery_app.py`

- Initializes the Celery application instance
- Configures broker (Redis/RabbitMQ) and backend
- Auto-discovers tasks from `core.tasks` and feature modules

Responsibilities:

- Decouple async task execution from FastAPI runtime
- Central Celery configuration

---

### 8.4 `urls.py`

- Central router registry
- Aggregates routers from all feature modules
- Applies global route prefixes and versioning
- Auto import all app related routers/endpoint

Responsibilities:

- Avoid circular imports
- Single source of truth for API routing

---

## 9. Core Module (`src/core/`)

Contains cross-cutting concerns shared across the application.

### 9.1 Exceptions (`exceptions/`)

| File | Description |
| --- | --- |
| `handlers.py` | Global exception handlers mapping domain errors to HTTP responses. |

### 9.2 Middleware (`middleware/`)

- Custom FastAPI middleware
- Examples: authentication, request logging, tracing, timing

### 9.3 Tasks (`tasks/`)

- Shared Celery tasks
- Long-running or asynchronous operations
- Infrastructure-level background jobs

---

## 10. Database Layer (`src/db/`)

Responsible for database infrastructure only.

| File | Description |
| --- | --- |
| `base.py` | SQLAlchemy declarative base and metadata registry. |
| `session.py` | Database engine and session lifecycle management. |

> Rule: This layer must not depend on application services.
> 

---

## 11. Tests (`tests/`)

Mirrors the production structure to encourage feature ownership and isolation.

```
tests/
 └── app/
     └── <feature_app>/

```

- Unit tests for services and repositories
- API tests for endpoints
- Encourages modular and scalable testing

---

## 12. Architectural Summary

- **Architecture:** Modular Monolith (DDD-inspired)
- **Framework:** FastAPI
- **Persistence:** SQLAlchemy + Alembic
- **Async Processing:** Celery
- **Deployment:** Docker

This structure ensures the project remains maintainable, testable, and scalable while avoiding the complexity of premature microservices.

**Folder Structure**

```
retrieve/
│
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── Makefile
├── pyproject.toml
│
├── docs/
│   ├── [ALEMBIC.md](http://alembic.md/)
│   ├── [db-schema.md](http://db-schema.md/)
│   ├── PROJECT_DOCUMENTATION.md
│   └── [PROJECT.md](http://project.md/)
│
├── logs/
│
├── scripts/
│   ├── __init__.py
│   ├── [startapp.py](http://startapp.py/)
│   └── alembic/
│       ├── __init__.py
│       ├── [env.py](http://env.py/)
│       ├── script.py.mako
│       └── versions/
│           ├── __init__.py
│           └── <migration_files>.py
│
├── src/
│   ├── __init__.py
│   ├── [main.py](http://main.py/)
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   └── <feature_app>/
│   │       ├── __init__.py
│   │       ├── models/
│   │       │   ├── __init__.py
│   │       │   └── <model_files>.py
│   │       ├── schemas/
│   │       │   ├── __init__.py
│   │       │   └── <schema_files>.py
│   │       ├── repositories/
│   │       │   ├── __init__.py
│   │       │   └── <repository_files>.py
│   │       ├── services/
│   │       │   ├── __init__.py
│   │       │   └── <service_files>.py
│   │       └── api/
│   │           └── v1/
│   │               ├── __init__.py
│   │               └── [endpoints.py](http://endpoints.py/)
│   │       
│   ├── config/
│   │   ├── __init__.py
│   │   ├── celery_app.py
│   │   ├── [config.py](http://config.py/)
│   │   ├── [logging.py](http://logging.py/)
│   │   └── [urls.py](http://urls.py/)
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── exceptions/
│   │   │   ├── __init__.py
│   │   │   └── [handlers.py](http://handlers.py/)
│   │   ├── middleware/
│   │   │   ├── __init__.py
│   │   │   └──  <middleware>.py
│   │   │   
│   │   └── tasks/
│   │       ├── __init__.py
│   │       └── <celery_task_files>.py
│   │
│   └── db/
│       ├── __init__.py
│       ├── [base.py](http://base.py/)
│       └── [session.py](http://session.py/)
│
└── tests/
    ├── __init__.py
    └── app/
        └── <feature_app>/
        └── <test_files>.py
```
