import logging
import logging.config
from pathlib import Path

from src.config import settings

try:
    import boto3
    import watchtower
except ImportError:
    watchtower = None


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


def get_cloudwatch_handler():
    """
    Create CloudWatch handler only if properly configured.
    """
    AWS_REGION = settings.AWS_REGION
    LOG_GROUP = settings.CLOUDWATCH_LOG_GROUP
    LOG_STREAM = settings.CLOUDWATCH_LOG_STREAM

    if not (watchtower and AWS_REGION and LOG_GROUP):
        return None

    session = boto3.Session(region_name=AWS_REGION)

    return watchtower.CloudWatchLogHandler(
        boto3_session=session,
        log_group=LOG_GROUP,
        stream_name=LOG_STREAM,
        create_log_group=True,
        create_log_stream=True,
    )


def setup_logging() -> None:
    handlers = {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "INFO",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            "filename": LOG_DIR / "app.log",
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 5,
            "level": "INFO",
        },
    }

    root_handlers = ["console", "file"]

    cloudwatch_handler = get_cloudwatch_handler()
    if cloudwatch_handler:
        logging.getLogger().addHandler(cloudwatch_handler)

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "access": {
                "format": "[%(asctime)s] [ACCESS] %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": handlers,
        "loggers": {
            "": {
                "handlers": root_handlers,
                "level": "INFO",
            },
            "uvicorn.error": {
                "level": "INFO",
            },
            "uvicorn.access": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            },
        },
    }

    logging.config.dictConfig(logging_config)

    if cloudwatch_handler:
        logging.getLogger().info("CloudWatch logging enabled")
    else:
        logging.getLogger().info("CloudWatch logging not configured")
