import logging
from pydantic import BaseSettings
from functools import lru_cache
from logging.config import dictConfig


logger = logging.getLogger('app')

class Settings(BaseSettings):
    SECRET_KEY: str = "secret"
    DEBUG: bool = False
    DB_URL: str = "postgresql://postgres:password@localhost:5432/vara"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = "../.env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

LOGGIN_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {  # correlation ID filter must be added here to make the %(correlation_id)s formatter work
        'correlation_id': {
            '()': 'asgi_correlation_id.CorrelationIdFilter',
            'uuid_length': 32,
            'default_value': '-',
        },
    },
    'formatters': {
        'console': {
            'class': 'logging.Formatter',
            # 'datefmt': '%H:%M:%S',
            # formatter decides how our console logs look, and what info is included.
            # adding %(correlation_id)s to this format is what make correlation IDs appear in our logs
            'format': '%(levelname)s: [%(asctime)s] %(name)s:%(module)s:%(lineno)d [%(correlation_id)s] %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            # Filter must be declared in the handler, otherwise it won't be included
            'filters': ['correlation_id'],
            'formatter': 'console',
        },
    },
    # Loggers can be specified to set the log-level to log, and which handlers to use
    'loggers': {
        # project logger
        'app': {'handlers': ['console'], 'level': 'DEBUG', 'propagate': True},
        'uvicorn': {'handlers': ['console'], 'level': 'DEBUG', 'propagate': False},
        # third-party package loggers
        # 'databases': {'handlers': ['console'], 'level': 'WARNING'},
        # 'httpx': {'handlers': ['console'], 'level': 'INFO'},
        'asgi_correlation_id': {'handlers': ['console'], 'level': 'WARNING'},
        'sqlalchemy': {'handlers': ['console'], 'level': 'WARNING'},
    },
}

def configure_logging() -> None:
    dictConfig(LOGGIN_CONFIG)