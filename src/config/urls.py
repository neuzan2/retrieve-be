# Import necessary modules for dynamic router inclusion
import importlib
import logging
import traceback
from pathlib import Path
from typing import Any

from fastapi import APIRouter

from src.config.config import settings

# from config.settings import settings

# Initialize logger for this module
logger = logging.getLogger(__name__)
# Create the main API router instance
api_router = APIRouter()

# Loop through all directories within apps and import their urls.py
# Include their router using pathlib and importlib

# Get the apps directory path
BASE_DIR = Path(__file__).parent.parent


def load_router_from_file(file_path: str):
    file_path = file_path.replace("/", ".").rstrip(".py")
    try:
        print(file_path)
        # Dynamically import the urls module from each app
        module = importlib.import_module(f"{file_path}")
        # Get the router attribute from the module
        router = getattr(module, "router", None)
        logger.info(f"Loaded router from {file_path}: {router}")

        # Include the router if it exists
        if router:
            api_router.include_router(router)
    except ModuleNotFoundError:
        # Log error if urls.py is not found for an app
        logger.error(traceback.format_exc())
        logger.error(f"No urls.py found for app: {file_path}")


# Iterate through each app directory
def load_all_routers(dir_path: Path) -> Any:
    for path in dir_path.iterdir():
        if path.name in ["__pycache__", "__init__.py"]:
            continue

        if path.is_file():
            load_router_from_file(str(path).split(BASE_DIR.name)[-1].strip("/"))
            continue

        if path.is_dir():
            # Skip Python cache directories
            return load_all_routers(path)

    return


load_all_routers(BASE_DIR / f"api/{settings.ACTIVE_API_VERSION}")
