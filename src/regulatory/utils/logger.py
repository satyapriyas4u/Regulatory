# src/regulatory/utils/logger.py
# This file contains the configuration for the logger used in the FastAPI application.
import os
from uvicorn.logging import DefaultFormatter, AccessFormatter

# Ensure the logs directory exists
os.makedirs("logs", exist_ok=True)

log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": DefaultFormatter,
            "fmt": "%(asctime)s - %(levelprefix)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "use_colors": True,
        },
        "access": {
            "()": AccessFormatter,
            "fmt": "%(asctime)s - %(client_addr)s - %(request_line)s - %(status_code)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "use_colors": True,
        },
        "services": {
            "()": DefaultFormatter,
            "fmt": "%(asctime)s - %(levelname)s - %(name)s - %(module)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "use_colors": False,
        },
        "logstash_json": {
            "format": '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "module": "%(module)s", "message": "%(message)s"}',
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "default": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stderr",
        },
        "access": {
            "class": "logging.StreamHandler",
            "formatter": "access",
            "stream": "ext://sys.stdout",
        },
        "file_logstash": {
            "class": "logging.FileHandler",
            "formatter": "services",
            "filename": "logs/logstash.log",
            "mode": "a",
            "encoding": "utf-8"
        },
        # "logstash": {
        #     "class": "logging.handlers.SocketHandler",
        #     "host": "localhost",
        #     "port": 1514,
        #     "formatter": "logstash_json"
        # },
        "error_file": {
			"class": "logging.FileHandler",
			"formatter": "services",
			"filename": "logs/error.log",
			"mode": "a",
			"encoding": "utf-8",
			"level": "ERROR"
		},
        "rotating_file": {
			"class": "logging.handlers.TimedRotatingFileHandler",
			"formatter": "services",
			"filename": "logs/rotated.log",
			"when": "midnight",         # Rotate at midnight
			"interval": 1,              # Every 1 day
			"backupCount": 7,           # Keep 7 days of logs
			"encoding": "utf-8"
		},
    },
    "loggers": {
        "uvicorn": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False
        },
        "uvicorn.error": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["access"],
            "level": "INFO",
            "propagate": False,
        },
        "services": {
            "handlers": ["default", "file_logstash"],
            "level": "DEBUG",
            "propagate": False,
        }
    },
}
