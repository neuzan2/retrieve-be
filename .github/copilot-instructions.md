# Python FastAPI - Copilot Instructions

Multi-module FastAPI backend service with async support and PostgreSQL.

## Project Overview

- **Framework**: FastAPI 0.100+
- **Python**: 3.12+
- **Database**: PostgreSQL via SQLAlchemy 2.0 (async), shared schema
- **Validation**: Pydantic v2

## Modules

| Module | Purpose |
|--------|---------|
| `client_request` | Client request processing |
| `distribution` | Request distribution |
| `intake` | Intake processing |
| `payment` | Payment handling |

## Code Style

- Use `snake_case` for variables and functions
- Use `PascalCase` for classes
- Use `UPPER_SNAKE_CASE` for constants
- Prefer type hints on all functions
- Use Google-style docstrings for public functions
- Max function length: 50 lines
- Max nesting depth: 3 levels

## Architecture

```
src/
├── core/                        # Shared: exceptions, security
|   ├── exceptions/              # Custom exception classes
|   └── security/                # Auth, password hashing
├── config                       # All system settings and configuration (Third-party keys, DB URLs, Celery, Logging, Urls etc.)
├── shared/                      # Cross-module: base models, common schemas
│   ├── models/                  # Base SQLAlchemy model, mixins
│   └── schemas/                 # Common Pydantic schemas
├── modules/
│   ├── client_request/
│   │   ├── api/                 # Routes
│   │   ├── services/            # Business logic
│   │   ├── models/              # SQLAlchemy models
│   │   ├── repositories/        # Data access layer
│   │   ├── utils/               # Utility functions
│   │   └── schemas/             # Pydantic schemas
│   ├── distribution/
│   │   ├── api/
│   │   ├── services/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── utils/
│   │   └── schemas/
│   ├── intake/
│   │   ├── api/
│   │   ├── services/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── utils/
│   │   └── schemas/
│   └── payment/
│       ├── api/
│       ├── services/
│       ├── models/
│       ├── repositories/
│       ├── utils/
│       └── schemas/
├── main.py                      # App + router aggregation
└── db.py                        # Database session
```

## Module Guidelines

- Each module is self-contained with its own api, services, models, repositories, utils, and schemas 
- Cross-module communication via **service imports**, not direct model access
- Foreign keys across modules are allowed (shared database)
- Shared base classes and utilities go in `src/shared/`

## Preferred Patterns

### Router registration (main.py)
```python
from src.config.urls import include_router

def create_app() -> FastAPI:
    app = FastAPI(title="Healthcare Backend API")
    include_router(app)
    ...
    return app

app = create_app()
```

Routers defined in `src/app/.../api/v*/endpoints.py` are auto-loaded. Each endpoint file must export a `router` object.

```python
from fastapi.router import APIRouter

router = APIRouter(prefix="/api/v1/client-requests", tags=["Client Requests"])

@router.post("/", response_model=ClientRequestResponse)
async def create_client_request(...):
    ...
    
```

### Async endpoints with dependency injection
```python
from fastapi.router import APIRouter

router = APIRouter(prefix="/api/v1/requests", tags=["Requests"])

@router.get("/requests/{request_id}")
async def get_request(
    request_id: int,
    db: DBSession,
    client_request_service: ClientRequestServiceDep,
):
    return await client_request_service.get_request_by_id(db, request_id)
```

### Service functions (db as first parameter)
```python
async def get_request_by_id(db: AsyncSession, request_id: int) -> ClientRequest | None:
    result = await db.execute(select(ClientRequest).where(ClientRequest.id == request_id))
    return result.scalar_one_or_none()

async def create_request(db: AsyncSession, request_in: ClientRequestCreate) -> ClientRequest:
    request = ClientRequest(**request_in.model_dump())
    db.add(request)
    await db.commit()
    await db.refresh(request)
    return request
```

### Cross-module service calls
```python
# In distribution/services/distribution_service.py
from src.modules.client_request.services import client_request_service

async def distribute_request(db: AsyncSession, request_id: int) -> Distribution:
    # Get request from another module via its service
    request = await client_request_service.get_request_by_id(db, request_id)
    if not request:
        raise NotFoundError("ClientRequest", request_id)

    distribution = Distribution(request_id=request.id, status="pending")
    db.add(distribution)
    await db.commit()
    return distribution
```

### Cross-module foreign keys (shared database)
```python
# In distribution/models/distribution.py
class Distribution(Base):
    __tablename__ = "distributions"

    id: Mapped[int] = mapped_column(primary_key=True)
    request_id: Mapped[int] = mapped_column(ForeignKey("client_requests.id"))
    status: Mapped[str] = mapped_column(String(50))

    # Relationship (optional, for convenience)
    request: Mapped["ClientRequest"] = relationship(back_populates="distributions")
```

### Pydantic v2 schemas
```python
class ClientRequestCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    client_id: int
    request_type: str = Field(..., min_length=1)

class ClientRequestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    client_id: int
    request_type: str
    status: str
    created_at: datetime
```

### Dependency injection
```python
DBSession = Annotated[AsyncSession, Depends(get_db)]
ClientRequestServiceDep = Annotated[type(client_request_service), Depends(get_client_request_service)]
```

### Custom exceptions
```python
class NotFoundError(AppException):
    def __init__(self, resource: str, id: int):
        super().__init__(f"{resource} {id} not found", "NOT_FOUND")
```

## Avoid

- Sync database calls in async functions
- Business logic in route handlers
- Direct model imports across modules (use services)
- Pydantic v1 syntax (`orm_mode`, `@validator`)
- Hardcoded configuration values
- Catching generic `Exception` without re-raising
- Raw SQL queries (use SQLAlchemy)
- Circular imports between modules

## Naming Conventions

- Module folders: `snake_case` (`client_request`, `distribution`)
- Files: `snake_case.py`
- Routes: `/api/v1/{module-name}/resource` (kebab-case in URLs)
- DB tables: `snake_case`, plural (`client_requests`, `distributions`, `intakes`, `payments`)
- Schemas: `ResourceCreate`, `ResourceUpdate`, `ResourceResponse`
- Service functions: `get_request_by_id()`, `create_request()`, `list_requests()`

## Testing

```
tests/
├── conftest.py                  # Shared fixtures, test db setup
├── modules/
│   ├── client_request/
│   │   ├── test_api.py
│   │   └── test_services.py
│   ├── distribution/
│   ├── intake/
│   └── payment/
└── integration/                 # Cross-module integration tests
    └── test_request_to_payment_flow.py
```

### Unit test (mock other modules)
```python
@pytest.mark.asyncio
async def test_distribute_request_success():
    mock_db = AsyncMock()
    mock_request = ClientRequest(id=1, status="pending")

    with patch.object(client_request_service, "get_request_by_id", return_value=mock_request):
        result = await distribution_service.distribute_request(mock_db, request_id=1)

    assert result.request_id == 1
    mock_db.commit.assert_called_once()
```

### Integration test (real services)
```python
@pytest.mark.asyncio
async def test_full_request_flow(test_db: AsyncSession):
    # Create request
    request = await client_request_service.create_request(test_db, request_data)

    # Distribute
    distribution = await distribution_service.distribute_request(test_db, request.id)

    # Process intake
    intake = await intake_service.process_intake(test_db, distribution.id)

    # Complete payment
    payment = await payment_service.create_payment(test_db, intake.id)

    assert payment.status == "completed"
```

## Security

- Validate all inputs via Pydantic
- Use `Depends(get_current_user)` for auth
- Never hardcode secrets
- Use environment variables via Pydantic Settings
- Parameterized queries only (SQLAlchemy default)

## Common Commands
- **Setup & Execution**:
    - `make install`: Install dependencies using `uv`.
    - `make run`: Start the development server with auto-reload.
    - `make test`: Run the pytest test suite.
    - `make lint`: Run Ruff for linting and formatting.
- **Creating a New Feature**:
    - `make startapp name=<feature_name>`: Scaffolds a new app module in `src/app/`.
- **Database Migrations**:
    - `make makemigrations`: Generate a new Alembic migration file.
    - `make migrate`: Apply migrations to the database.
- **Docker**:
    - Use `make docker-build`, `docker-up`, and `docker-migrate` for containerized development and deployment.
