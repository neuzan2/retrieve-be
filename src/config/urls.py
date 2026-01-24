# Import necessary modules for dynamic router inclusion
import importlib
import logging
import traceback
from pathlib import Path
from typing import Any, Optional

from fastapi import APIRouter, FastAPI

from src.config import settings

logger = logging.getLogger(__name__)


def include_router(app: FastAPI):
    api_configs = settings.API_CONFIGS

    for config in api_configs:
        if config.get("is_active"):
            version = config.get("version", "v1")
            router = APIRouter(
                prefix=f"/api/{version}",
            )

            # Execute the decorated function to populate the router
            load_all_routers(router=router, api_version=version)
            # Include the populated router into the main app
            app.include_router(router)


def load_router_from_file(api_router: APIRouter, file_path: str):
    file_path = file_path.replace("/", ".").rstrip(".py")
    try:
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
def load_all_routers(
    router: APIRouter,
    api_version: str,
    app_dir_path: Optional[Path] = None,
    *args,
    **kwargs,
) -> Any:
    app_dir_path = app_dir_path or settings.APP_DIR

    for _path in app_dir_path.iterdir():
        if _path.name in ["__pycache__", "__init__.py"]:
            continue

        if _path.is_file():
            # Adjust path logic to properly locate the file relative to the project root or app dir
            # If settings.APP_DIR is an absolute path, we need to be careful with string splitting
            relative_path_part = str(_path).split(settings.APP_DIR.name)[-1].strip("/")
            # We might need to construct the module path correctly. Assuming 'src' is the root package.
            # This part depends heavily on your directory structure, blindly fixing based on previous logic:
            load_router_from_file(
                router, f"src.{settings.APP_DIR.name}.{relative_path_part}"
            )
            continue

        if _path.is_dir():
            # Recursively check specifically for the api version folder structure if that's the intent
            # Or just recurse into directories looking for files.
            # The original logic appended /api/{version} which assumes a strict structure.
            api_path = (
                _path
                if {"api", api_version}.issubset(set(_path.parts))
                else _path / f"api/{api_version}"
            )
            if api_path.exists():
                load_all_routers(
                    router=router, api_version=api_version, app_dir_path=api_path
                )
            else:
                # If standard recursion is needed without forcing api/version check here:
                # load_all_routers(router=router, api_version=api_version, path=_path)
                pass
    return None
