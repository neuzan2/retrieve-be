# Alembic Models Auto-Discovery

## Overview

The Alembic configuration has been updated to automatically discover and import all database models from all apps in the
`src/app` directory. This eliminates the need to manually import each model in the `env.py` file.

## How It Works

The `import_all_models()` function in `env.py` automatically:

1. Scans all subdirectories in `src/app/`
2. For each app directory, checks for:
    - A `models/` directory with model files
    - A `models.py` file
3. Automatically imports all model modules found
4. Registers all models with SQLAlchemy's Base metadata

## Supported Structures

### Models Directory Structure

```
src/app/
├── auth/
│   └── models/
│       ├── __init__.py
│       ├── user.py          # Will be auto-imported
│       └── permissions.py   # Will be auto-imported
├── user/
│   └── models.py            # Will be auto-imported
└── products/
    └── models/
        ├── __init__.py
        ├── product.py       # Will be auto-imported
        └── category.py      # Will be auto-imported
```

### Single File Structure

```
src/app/
└── orders/
    └── models.py            # Will be auto-imported
```

## Usage

### Creating a New App with Models

1. Create your app directory in `src/app/`
2. Create either:
    - A `models/` directory with `__init__.py` and your model files
    - A single `models.py` file

Example model file:

```python
from src.db.base import BaseModel
from sqlalchemy import Column, String, Integer

class Product(BaseModel):
    __tablename__ = "products"
    
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
```

3. Run Alembic commands as usual:

```bash
# Generate migration
alembic revision --autogenerate -m "Add Product model"

# Apply migration
alembic upgrade head
```

## Alembic Commands

### Create a new migration (autogenerate)

```bash
alembic revision --autogenerate -m "description of changes"
```

### Apply migrations

```bash
# Upgrade to latest
alembic upgrade head

# Upgrade one version
alembic upgrade +1

# Downgrade one version
alembic downgrade -1
```

### View migration history

```bash
alembic current
alembic history
```

## Troubleshooting

### Model Not Detected

If a model is not being detected:

1. **Check directory structure**: Ensure your app is in `src/app/` and has either `models/` directory or `models.py`
   file
2. **Check imports**: Ensure your models import from `src.db.base.BaseModel`
3. **Check __init__.py**: If using `models/` directory, ensure it has an `__init__.py` file
4. **Run with verbose output**: Check the console output when running Alembic commands - it will print which models were
   imported

### Import Errors

If you see import errors:

- Ensure all dependencies are installed
- Check that the project root is correctly set in `sys.path`
- Verify that model files don't have circular imports

## Configuration Files

- **alembic.ini**: Main Alembic configuration file (points to `scripts/alembic`)
- **scripts/alembic/env.py**: Contains the auto-discovery logic
- **scripts/alembic/versions/**: Contains migration files

## Benefits

✅ **No manual imports needed** - Just create your models, and they're automatically detected  
✅ **Scalable** - Works with any number of apps and models  
✅ **Flexible** - Supports both single file and directory structures  
✅ **Maintainable** - No need to update env.py when adding new apps or models  
✅ **Debug-friendly** - Prints imported models to console for verification
