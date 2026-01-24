# Retrieve FastAPI Backend - Complete Project Documentation

## Table of Contents

1. [Project Overview](#project-overview)
2. [Used Packages](#used-packages)
3. [Architecture & Design Patterns](#architecture--design-patterns)
4. [Folder Structure](#folder-structure)
5. [Detailed Component Descriptions](#detailed-component-descriptions)
6. [Development Workflow](#development-workflow)
7. [Technology Stack](#technology-stack)
8. [Coding Standards & Guidelines](#coding-standards--guidelines)
9. [Best Practices](#best-practices)

---

## Project Overview

**Retrieve** is a production-ready FastAPI backend project designed following industry best practices. It implements a modular, scalable architecture with async support, comprehensive database management, and a clear separation of concerns.

## Used Packages
[x] Python ≥  3.12
[x] FastAPI ≥ 0.114.0
[x] Pydantic ≥ 2.x
[ ] Postgresql ≥ 17
[x] SQLalchemy ≥ 2.x
[ ] Xlsxwriter >= 3.x
[ ] Pandas  >= 2.x
[x] Pypika >= 0.48
[ ] Redis >=7.1.0
[ ] Celery>=5.6.2
[ ] Redshift_connector >= 2.x

### Key Characteristics

- **Modular Architecture**: Each feature is self-contained with dedicated layers
- **Async-First**: Full async/await support throughout the stack
- **Type-Safe**: Comprehensive type hints and Pydantic validation
- **Database-First**: Async SQLAlchemy with automatic migrations
- **Production-Ready**: Includes Docker support, logging, error handling, and security features
- **Developer-Friendly**: Automated tools for scaffolding new apps and managing database migrations

### Tech Stack

| Layer | Technology |
|-------|-----------|
| **Framework** | FastAPI >= 0.114 |
| **Python** | Python >= 3.12 |
| **ORM** | Async SQLAlchemy 2.x |
| **Database** | PostgreSQL 15+ |
| **Caching & Queues** | Redis |
| **Async Tasks** | Celery |
| **Data Validation** | Pydantic v2 |
| **Migrations** | Alembic |
| **Package Management** | UV |
| **Linting/Formatting** | Ruff |
| **Type Checking** | MyPy |
| **Testing** | Pytest |
| **Containerization** | Docker & Docker Compose |

---

## Architecture & Design Patterns

### 1. Layered Architecture (per Feature/App)

Each feature module follows a strict 4-layer pattern:

```
┌──────────────────────────────────────────┐
│  API Endpoints (FastAPI Routes)          │
├──────────────────────────────────────────┤
│  Services (Business Logic)               │
├──────────────────────────────────────────┤
│  Repositories (Data Access)              │
├──────────────────────────────────────────┤
│  Models (SQLAlchemy ORM)                 │
└──────────────────────────────────────────┘
         ↓ (uses)
    Schemas (Pydantic)
```

**Flow Example - User Creation:**

1. **Endpoint** receives HTTP POST request with `UserCreate` schema
2. **Service** applies business logic (password hashing, validation)
3. **Repository** executes database operations (INSERT, commit, refresh)
4. **Model** defines SQLAlchemy table structure
5. **Schema** provides request/response DTO

### 2. Dynamic Router Discovery

The `urls.py` configuration system automatically discovers and registers routers from all apps without manual registration. Each app's `api/v{1,2}/endpoints.py` file must export a `router` object.

**Auto-discovery process:**
- Scans `src/app/` directory
- Loads `api/v{1,2}/endpoints.py` from each app
- Registers routers with version-based prefixes
- Enables multi-version API support without duplication

### 3. Multi-Version API Support

Configuration in `settings.py` allows parallel v1/v2 APIs:

```python
API_CONFIGS = [
    {"version": "v1", "is_active": True},
    {"version": "v2", "is_active": True}
]
```

Each version maintains independent endpoint logic while sharing models and services.

### 4. Dependency Injection Pattern

FastAPI's built-in dependency injection is used for:
- Database sessions
- Authentication context
- Request-scoped data
- Repository instances

### 5. Repository Pattern

**Purpose**: Abstract data access logic from business logic

- Each repository is responsible for CRUD operations
- Services never directly interact with database
- Repositories handle session commit/refresh
- Single-responsibility for data access

### 6. Middleware & Cross-Cutting Concerns

**RequestIdMiddleware**: Injects `X-Request-ID` header for distributed tracing
**Error Handling**: Global exception handlers for consistent API responses
**Tenant Context**: Multi-tenancy support via middleware

---

## Folder Structure

### Root Level

```
retrieve-be/
├── .github/               # GitHub Actions CI/CD and Copilot instructions
├── .vscode/               # VS Code workspace settings and extensions
├── .env                   # Environment variables (not in git)
├── .env.example           # Template for environment variables
├── .gitignore             # Git ignore rules
├── .pre-commit-config.yaml# Pre-commit hooks configuration
├── alembic.ini            # Alembic migration configuration
├── Dockerfile             # Container image definition
├── docker-compose.yml     # Multi-container orchestration
├── Makefile               # Development task automation
├── pyproject.toml         # Project metadata and dependencies
├── uv.lock                # Locked dependency versions
├── docs/                  # Project documentation
├── scripts/               # Utility and scaffolding scripts
├── src/                   # Source code
└── tests/                 # Test suite
```

### `/src` - Source Code Directory

```
src/
├── __init__.py            # Package marker
├── main.py                # FastAPI app factory
├── app/                   # Feature modules (apps)
│   ├── __init__.py
│   ├── auth/              # Authentication app
│   ├── health_check/      # Health check app
│   └── [new_feature]/     # Generated via make startapp
├── config/                # Configuration management
│   ├── __init__.py
│   ├── config.py          # Pydantic Settings
│   ├── logging.py         # Logging configuration
│   ├── urls.py            # Dynamic router loading
│   └── celery_app.py      # Celery configuration
├── core/                  # Cross-cutting concerns
│   ├── exceptions/        # Exception handlers
│   ├── middleware/        # ASGI middleware
│   ├── security/          # JWT, password hashing
│   └── tasks/             # Celery background tasks
├── db/                    # Database configuration
│   ├── __init__.py
│   ├── base.py            # SQLAlchemy Base with UUID PK
│   └── session.py         # Async session management
```

### `/src/app` - Feature Module Template

Each feature is a self-contained module with this structure:

```
src/app/[feature_name]/
├── __init__.py
├── models/                # SQLAlchemy ORM models
│   ├── __init__.py
│   ├── entity1.py
│   └── entity2.py
├── schemas/               # Pydantic request/response schemas
│   ├── __init__.py
│   └── entity1.py
├── repositories/          # Data access layer
│   ├── __init__.py
│   └── entity1.py
├── services/              # Business logic layer
│   ├── __init__.py
│   └── entity1.py
├── api/                   # API endpoints
│   ├── __init__.py
│   ├── v1/
│   │   ├── __init__.py
│   │   └── endpoints.py   # FastAPI router (required)
│   └── v2/                # Optional v2 endpoints
│       ├── __init__.py
│       └── endpoints.py
└── tests/                 # App-specific tests
    ├── __init__.py
    └── test_entity1.py
```

### `/src/config` - Configuration Management

```
src/config/
├── config.py              # Pydantic Settings (environment-based)
├── logging.py             # structlog setup with JSON formatting
├── urls.py                # Dynamic router discovery & registration
├── celery_app.py          # Celery worker configuration
└── __init__.py
```

**Key Features:**
- Environment-based configuration via `.env` files
- Multi-version API support
- Cached properties for path calculation
- Database URL construction

### `/src/core` - Cross-Cutting Concerns

```
src/core/
├── exceptions/
│   ├── __init__.py
│   └── handlers.py        # Global exception handlers
├── middleware/
│   ├── __init__.py
│   ├── request_id.py      # X-Request-ID injection
│   └── tenant_context.py  # Multi-tenancy context
├── security/
│   ├── __init__.py
│   ├── hashing.py         # Argon2 password hashing (argon2-cffi)
│   └── jwt.py             # JWT token handling (python-jose)
├── tasks/
│   ├── __init__.py
│   └── user_tasks.py      # Celery task definitions
└── __init__.py
```

**Purpose**: Shared utilities and infrastructure code used across all apps.

### `/src/db` - Database Layer

```
src/db/
├── base.py                # BaseModel with UUID primary key
├── session.py             # AsyncSession factory
└── __init__.py
```

**Key Components:**

- **BaseModel**: SQLAlchemy declarative base with:
  - Automatic UUID primary key
  - PostgreSQL UUID type
  - Metadata with naming conventions
  
- **Session Management**: Async session configuration for PostgreSQL with asyncpg driver

### `/scripts` - Development Tools

```
scripts/
├── __init__.py
├── startapp.py            # App scaffolding CLI tool
├── alembic/               # Database migration system
│   ├── env.py             # Auto-discovery of models
│   ├── script.py.mako     # Migration template
│   └── versions/          # Migration files
│       └── d65eeea81afc_initial_migration.py
└── _scratch/              # Template files
    └── app_template/      # Scaffolding templates
        ├── __init__.py-tpl
        ├── models.py-tpl
        ├── repositories.py-tpl
        ├── schemas.py-tpl
        ├── services.py-tpl
        ├── api/v1/endpoints.py-tpl
        └── tests/test_*.py-tpl
```

**Development Scripts:**
- `startapp.py`: CLI tool to generate new feature modules
- `alembic/`: Database version control system

### `/tests` - Test Suite

```
tests/
├── __init__.py
└── app/                   # App-specific test modules
    ├── test_auth.py       # Authentication tests
    └── ...
```

### `/docs` - Documentation

```
docs/
├── PROJECT.md             # Project overview and setup
├── ALEMBIC.md             # Database migration guide
├── PROJECT_DOCUMENTATION.md # This comprehensive guide
└── ECLAT Analytics Backend - Coding Guidelines.pdf
```

---

## Detailed Component Descriptions

### Main Entry Point (`src/main.py`)

```python
from fastapi import FastAPI
from src.config import settings
from src.config.logging import setup_logging
from src.config.urls import include_router
from src.core.exceptions.handlers import add_exception_handlers
from src.core.middleware.request_id import RequestIdMiddleware

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.DEBUG
    )
    
    app.add_middleware(RequestIdMiddleware)
    add_exception_handlers(app)
    include_router(app=app)
    
    return app

app = create_app()
```

**Responsibilities:**
- Creates and configures the FastAPI application
- Registers middleware
- Adds exception handlers
- Loads API routers dynamically

### Settings (`src/config/config.py`)

Pydantic-based configuration with environment variable support:

```python
class Settings(BaseSettings):
    # Application
    APP_NAME: str = "FastAPI Backend"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    
    # Database (PostgreSQL)
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    
    # Cache (Redis)
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    
    # Security (JWT)
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Multi-version API
    API_CONFIGS: List[Dict[str, Union[str, bool]]]
    
    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{...}"
```

**Features:**
- Environment-based configuration
- Computed properties (database_url, paths)
- Cached properties for filesystem paths
- API version configuration

### Database Models (`src/db/base.py`)

Base model with automatic UUID primary key:

```python
class BaseModel(Base):
    __abstract__ = True
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
```

**Features:**
- All models inherit from BaseModel
- Automatic UUID generation
- PostgreSQL UUID type support
- Metadata with naming conventions for constraints

### Example App Structure - Auth Module

#### Model (`auth/models/user.py`)
```python
from sqlalchemy import Boolean, Column, String
from src.db.base import BaseModel

class User(BaseModel):
    __tablename__ = "users"
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
```

#### Schema (`auth/schemas/user.py`)
```python
from pydantic import BaseModel, EmailStr
import uuid

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: uuid.UUID
    is_active: bool
    
    class Config:
        from_attributes = True
```

#### Repository (`auth/repositories/user.py`)
```python
class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_user(self, user_in: UserCreate) -> User:
        user = User(email=user_in.email, hashed_password=user_in.password)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalars().first()
```

**Repository Responsibilities:**
- Execute database queries
- Handle session commit/refresh
- Return ORM model instances
- Abstract SQL from business logic

#### Service (`auth/services/user.py`)
```python
class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    async def create_user(self, user_in: UserCreate) -> User:
        # Business logic: password hashing
        hashed_password = hash_password(user_in.password)
        user_in.password = hashed_password
        
        # Delegate to repository
        return await self.repository.create_user(user_in)
```

**Service Responsibilities:**
- Apply business logic
- Hash passwords before repository operations
- Validate business rules
- Orchestrate multiple repository calls

#### API Endpoint (`auth/api/v1/endpoints.py`)
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/users/", response_model=User)
async def create_user(
    user_in: UserCreate,
    session: AsyncSession = Depends(get_db_session)
):
    repository = UserRepository(session)
    service = UserService(repository)
    return await service.create_user(user_in)
```

**Endpoint Responsibilities:**
- Define HTTP routes and methods
- Handle request/response validation via Pydantic
- Set status codes
- Manage dependencies (sessions, auth)
- Convert between schemas and services

### URL Router System (`src/config/urls.py`)

Dynamic router discovery that:
1. Scans all apps in `src/app/`
2. Loads `api/v{1,2}/endpoints.py` modules
3. Extracts `router` objects
4. Registers them with API version prefixes

**Benefits:**
- No manual router registration
- Automatic API versioning
- Scalable app addition (just create app structure)

### Exception Handling (`src/core/exceptions/handlers.py`)

Global exception handlers for consistent error responses:
- HTTPException
- ValidationError
- DatabaseError
- CustomApplicationErrors

### Security Module (`src/core/security/`)

**hashing.py**: Argon2 password hashing
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

**jwt.py**: JWT token operations
- Token creation
- Token verification
- Claims extraction

### Celery Tasks (`src/core/tasks/`)

Asynchronous background tasks:
```python
from src.config.celery_app import celery_app

@celery_app.task
async def send_email_notification(user_id: str, message: str):
    # Send email asynchronously
    pass
```

**Use Cases:**
- Email notifications
- Report generation
- Data processing
- Scheduled jobs

---

## Development Workflow

### Setting Up Development Environment

```bash
# Install dependencies
make install

# Set up environment files
cp .env.example .env
cp .env.example .env.local  # For local development with localhost DB
```

### Creating a New Feature

```bash
# Generate new app with full structure
make startapp name=feature_name

# The command generates:
# src/app/feature_name/
# ├── models/
# ├── schemas/
# ├── repositories/
# ├── services/
# ├── api/v1/endpoints.py
# └── tests/
```

### Running the Application

```bash
# Local development with auto-reload
make run

# Docker-based development
make docker-build
make docker-up
make docker-migrate
```

### Database Migrations

```bash
# Create a new migration
make makemigrations

# Apply pending migrations
make migrate

# Rollback last migration
make downgrade

# Docker-based migrations
make docker-makemigrations
make docker-migrate
make docker-downgrade
```

### Code Quality

```bash
# Run linters (Ruff + MyPy)
make lint

# Auto-format code
make format

# Run tests
make test
```

### Docker Workflow

```bash
# Build images
make docker-build

# Start all services (API, Postgres, Redis)
make docker-up

# Run migrations in container
make docker-migrate

# View logs
make docker-logs

# Shell into container
make docker-shell

# Stop services
make docker-down
```

---

## Coding Standards & Guidelines

### 1. Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Classes | PascalCase | `UserRepository`, `UserService` |
| Functions/Methods | snake_case | `create_user()`, `get_user_by_id()` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRIES`, `API_VERSION` |
| Private Methods | _snake_case | `_validate_email()` |
| Database Tables | snake_case | `users`, `user_posts` |
| Columns | snake_case | `created_at`, `updated_at` |

### 2. Type Hints (PEP 484)

**Mandatory for all functions and methods:**

```python
# ✓ Correct
async def get_user(user_id: uuid.UUID) -> Optional[User]:
    ...

async def create_users(users: List[UserCreate]) -> List[User]:
    ...

# ✗ Incorrect
async def get_user(user_id):
    ...
```

### 3. Docstring Format (Google Style)

```python
def create_user(email: str, password: str) -> User:
    """Create a new user with email and password.
    
    Args:
        email: The user's email address.
        password: The user's plain text password.
    
    Returns:
        The created User instance.
    
    Raises:
        ValueError: If email is already registered.
        ValidationError: If email format is invalid.
    """
```

### 4. Async/Await Requirements

**All I/O operations must be async:**

```python
# ✓ Correct - Async database queries
async def get_user(self, user_id: uuid.UUID) -> Optional[User]:
    result = await self.session.execute(select(User).where(User.id == user_id))
    return result.scalars().first()

# ✗ Incorrect - Synchronous (blocks event loop)
def get_user(self, user_id: uuid.UUID) -> Optional[User]:
    result = self.session.execute(select(User).where(User.id == user_id))
    return result.scalars().first()
```

### 5. Layer Responsibilities

**Endpoints:**
- HTTP request/response handling
- Status code definition
- Dependency injection
- Schema validation

```python
@router.post("/users/", response_model=User, status_code=201)
async def create_user(user_in: UserCreate, session: AsyncSession = Depends(get_session)):
    repository = UserRepository(session)
    service = UserService(repository)
    return await service.create_user(user_in)
```

**Services:**
- Business logic
- Validation
- Cross-repository orchestration
- Password hashing (before repository calls)

```python
class UserService:
    async def create_user(self, user_in: UserCreate) -> User:
        # Business logic: validate, hash password
        if await self.repository.get_user_by_email(user_in.email):
            raise ValueError("Email already registered")
        
        user_in.password = hash_password(user_in.password)
        return await self.repository.create_user(user_in)
```

**Repositories:**
- Database operations only
- Session commit/refresh
- Query building
- Result mapping

```python
class UserRepository:
    async def create_user(self, user_in: UserCreate) -> User:
        user = User(**user_in.dict())
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
```

**Models:**
- SQLAlchemy table definition
- Column definitions
- Relationships
- Constraints

```python
class User(BaseModel):
    __tablename__ = "users"
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
```

**Schemas:**
- Pydantic models for validation
- Request/response DTOs
- No database knowledge
- Nested models for complex structures

```python
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    id: uuid.UUID
    email: EmailStr
    is_active: bool
    
    class Config:
        from_attributes = True
```

### 6. Error Handling

**Use FastAPI HTTPException:**

```python
from fastapi import HTTPException, status

# Resource not found
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found"
)

# Validation error
raise HTTPException(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    detail="Invalid email format"
)

# Server error
raise HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Database error"
)
```

### 7. Database Transactions

```python
async def transfer_funds(self, from_user: uuid.UUID, to_user: uuid.UUID, amount: float):
    try:
        await self.session.execute(...)
        await self.session.execute(...)
        await self.session.commit()  # All or nothing
    except Exception as e:
        await self.session.rollback()
        raise
```

### 8. Environment Configuration

**Never hardcode secrets or config values:**

```python
# ✓ Correct - Use environment variables
from src.config import settings

db_url = settings.database_url
secret_key = settings.SECRET_KEY

# ✗ Incorrect - Hardcoded values
db_url = "postgresql://user:pass@localhost:5432/db"
secret_key = "very-secret-key-123"
```

### 9. Import Organization

```python
# Standard library
import uuid
from typing import List, Optional
from pathlib import Path

# Third-party
from fastapi import APIRouter, Depends
from sqlalchemy import select
from pydantic import BaseModel

# Local application
from src.db.base import BaseModel
from src.app.auth.models import User
from src.app.auth.schemas import UserCreate
from src.core.security.hashing import hash_password
```

### 10. Code Formatting

- **Line length**: 88 characters (Ruff default)
- **Formatter**: Ruff (`make format`)
- **Linter**: Ruff (`make lint`)
- **Type checker**: MyPy (`make lint`)

---

## Best Practices

### 1. Database Best Practices

✓ **DO:**
- Use UUID primary keys
- Add indexes to frequently queried columns
- Use foreign keys with ON DELETE constraints
- Create migrations for all schema changes
- Use transactions for multi-operation updates

✗ **DON'T:**
- Use sequential integer IDs in distributed systems
- Directly modify database schema
- Perform blocking queries in endpoints
- Skip migrations for schema changes

### 2. Security Best Practices

✓ **DO:**
- Hash passwords with Argon2
- Use JWT tokens with expiration
- Validate all user inputs via Pydantic
- Use HTTPS in production
- Implement rate limiting
- Log security events

✗ **DON'T:**
- Store plain text passwords
- Expose sensitive errors to clients
- Hardcode secrets
- Skip input validation
- Use weak password hashing (MD5, SHA1)

### 3. API Design Best Practices

✓ **DO:**
- Use consistent naming (snake_case for fields)
- Version APIs from the start
- Implement pagination for list endpoints
- Use proper HTTP status codes
- Document endpoints with docstrings
- Return consistent error formats

✗ **DON'T:**
- Mix naming conventions
- Return bare 200 with error messages
- Expose stack traces to clients
- Create undocumented endpoints

### 4. Testing Best Practices

✓ **DO:**
- Test each layer independently
- Use fixtures for setup/teardown
- Mock external dependencies
- Achieve >80% code coverage
- Test edge cases and error paths

✗ **DON'T:**
- Skip unit tests
- Use real databases in tests
- Create brittle tests
- Test implementation details

### 5. Performance Best Practices

✓ **DO:**
- Use async/await for I/O operations
- Implement caching for expensive operations
- Paginate large result sets
- Use database indexes
- Monitor slow queries
- Use connection pooling

✗ **DON'T:**
- Use synchronous database queries
- Load entire datasets into memory
- Query in loops (N+1 problem)
- Skip database optimization

### 6. Logging Best Practices

✓ **DO:**
- Use structured logging with JSON
- Include request IDs for tracing
- Log at appropriate levels
- Log security-relevant events
- Include context information

✗ **DON'T:**
- Log sensitive data (passwords, tokens)
- Use print() statements
- Log at wrong levels
- Create unstructured logs

### 7. Documentation Best Practices

✓ **DO:**
- Document public functions
- Explain business logic
- Keep docs up to date
- Document API changes
- Include examples

✗ **DON'T:**
- Write obvious comments
- Leave docs outdated
- Skip critical documentation
- Comment out code (use git instead)

---

## Project File Locations Reference

| Functionality | Location |
|---|---|
| Main app entry point | [src/main.py](../src/main.py) |
| Settings configuration | [src/config/config.py](../src/config/config.py) |
| Logging setup | [src/config/logging.py](../src/config/logging.py) |
| URL routing | [src/config/urls.py](../src/config/urls.py) |
| Database base models | [src/db/base.py](../src/db/base.py) |
| Exception handlers | [src/core/exceptions/handlers.py](../src/core/exceptions/handlers.py) |
| Request ID middleware | [src/core/middleware/request_id.py](../src/core/middleware/request_id.py) |
| Password hashing | [src/core/security/hashing.py](../src/core/security/hashing.py) |
| JWT handling | [src/core/security/jwt.py](../src/core/security/jwt.py) |
| Celery tasks | [src/core/tasks/user_tasks.py](../src/core/tasks/user_tasks.py) |
| Auth app | [src/app/auth/](../src/app/auth/) |
| Health check app | [src/app/health_check/](../src/app/health_check/) |
| Migrations | [scripts/alembic/versions/](../scripts/alembic/versions/) |
| App scaffold tool | [scripts/startapp.py](../scripts/startapp.py) |
| Makefile commands | [Makefile](../Makefile) |
| Docker config | [docker-compose.yml](../docker-compose.yml) |
| Dependencies | [pyproject.toml](../pyproject.toml) |

---

## Quick Reference - Command Cheat Sheet

```bash
# Development
make install              # Install dependencies
make run                  # Start app with auto-reload
make test                 # Run tests
make lint                 # Check code quality
make format               # Auto-format code

# App Management
make startapp name=myapp  # Generate new app

# Database
make makemigrations       # Create migration
make migrate              # Apply migrations
make downgrade            # Revert migration

# Docker
make docker-build         # Build containers
make docker-up            # Start services
make docker-down          # Stop services
make docker-logs          # View logs
make docker-shell         # Enter container shell
make docker-migrate       # Migrate in container
```

---

## Summary

The Retrieve FastAPI Backend provides a robust, scalable foundation for building modern web applications. By following the modular architecture, adhering to coding standards, and leveraging the provided tools and patterns, developers can build maintainable, secure, and performant APIs.

Key takeaways:
- **Modularity**: Self-contained feature apps with clear separation of concerns
- **Async-First**: Fully async throughout the stack for better performance
- **Type-Safe**: Comprehensive type hints and validation with Pydantic
- **Developer-Friendly**: Automated tooling and scaffolding for rapid development
- **Production-Ready**: Built with security, logging, error handling, and testing in mind
