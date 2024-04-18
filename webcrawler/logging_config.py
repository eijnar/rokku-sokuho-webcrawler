# logger_config.py
import logging
import logging.config


def setup_logging():
    """Sets up the logging configuration."""
    LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'detailed': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            },
            'simple': {
                'format': '%(levelname)s - %(message)s'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'detailed',
                'stream': 'ext://sys.stdout',  # Default is stdout
            },
            'file': {
                'class': 'logging.FileHandler',
                'level': 'INFO',
                'formatter': 'detailed',
                'filename': '../logs/webcrawler.log',
                'mode': 'a'  # append mode
            }
        },
        'loggers': {
            '': {  # root logger
                'handlers': ['console', 'file'],
                'level': 'DEBUG',
                'propagate': False
            },
            "pyppeteer": {
                "handlers": ["console"],
                "level": "WARNING",
                "propagate": False
            },
            "websockets": {
                "handlers": ["console"],
                "level": "WARNING",
                "propagate": False
            }
        }
    }

    logging.config.dictConfig(LOGGING_CONFIG)

# Get the configured logger


def get_logger(name):
    return logging.getLogger(name)
