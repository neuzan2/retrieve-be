# Copilot Instructions: Retrieve FastAPI Backend

## Architecture Overview

This is a **modular FastAPI backend** using async SQLAlchemy, Celery, and PostgreSQL. Each feature is organized as a self-contained app with a strict **Models → Schemas → Repositories → Services → API Endpoints** pattern.

### Key Directory Structure

- `src/app/` - Feature modules (e.g., `auth/`, `health_check/`). Each has: `models/`, `schemas/`, `repositories/`, `services/`, `api/v{1,2}/endpoints.py`
- `src/core/` - Cross-cutting concerns: security (JWT, hashing), middleware (request_id), exception handlers
- `src/config/` - Settings (pydantic), logging, URL routing, Celery config
- `src/db/` - Base ORM classes with UUID primary keys, async session management
- `scripts/` - App scaffolding tool (`startapp.py`)

## Architecture Patterns

### 1. Layered Pattern (per app)

```
API Endpoint → Service → Repository → SQLAlchemy Model
                ↓
         Pydantic Schema (DTO)
```

**Example**: User creation flows through:
1. [Endpoint](src/app/auth/api/v1/endpoints.py) receives `UserCreate` schema
2. [Service](src/app/auth/services/user.py) applies business logic (password hashing via `Hasher`)
3. [Repository](src/app/auth/repositories/user.py) executes DB operations (add, commit, refresh)
4. [Model](src/app/auth/models/user.py) defines SQLAlchemy table

### 2. Dynamic Router Loading

[urls.py](src/config/urls.py) auto-discovers `api/v{1,2}/endpoints.py` in each app and registers routers. Each endpoint file must export a `router` object. No manual URL registration needed.

### 3. Database Patterns

- Models inherit from [BaseModel](src/db/base.py) which auto-adds UUID `id` PK with PostgreSQL UUID type
- All models use SQLAlchemy 2.x async patterns with `AsyncSession`
- Repositories always handle session commit/refresh; services never do
- Migrations via Alembic in [alembic/versions/](scripts/alembic/versions/)

### 4. Middleware & Security

- [RequestIdMiddleware](src/core/middleware/request_id.py) injects `X-Request-ID` header into all requests for distributed tracing
- JWT and password hashing available in [src/core/security/](src/core/security/)
- Global exception handlers in [src/core/exceptions/handlers.py](src/core/exceptions/handlers.py)

## Developer Workflows

### Running the App

```bash
make install          # Install dependencies (uses uv)
make run              # Start uvicorn with auto-reload
make test             # Run pytest
make lint             # Ruff lint + format
```

### Creating a New App

```bash
make startapp name=myfeature
```

Generates standard app structure at `src/app/myfeature/` with templates for models, services, schemas, repositories, and endpoints.

### Database Migrations

```bash
make makemigrations   # Create migration file
make migrate          # Apply migrations
make downgrade        # Revert last migration
```

## Key Developer Notes

1. **Always use async/await**: All DB queries and API operations are async. Use `AsyncSession` from SQLAlchemy.
2. **Password hashing is service layer responsibility**: See [user.py service](src/app/auth/services/user.py#L21) - hash before passing to repository.
3. **Settings via environment**: [Settings](src/config/config.py) loads from `.env` using Pydantic BaseSettings. Add new config vars there, not scattered in code.
4. **UUID everywhere**: All models use UUID PKs; UUIDs are auto-generated as `uuid.uuid4()`.
5. **No status codes in models**: Keep endpoints responsible for `status_code` via FastAPI decorators.
6. **Celery tasks** in [src/core/tasks/](src/core/tasks/user_tasks.py) for async work (email, reporting).

## Multi-Version API Support

[API_CONFIGS](src/config/config.py#L27) allows parallel v1/v2 API versions. Create new version folder (`api/v2/`) with different endpoint logic while sharing models/services.

## Docker & Deployment

```bash
make docker-build         # Build images
make docker-up            # Start services (API, Postgres, Redis)
make docker-migrate       # Run migrations in container
```

Project includes Dockerfile and docker-compose.yml for production readiness.
