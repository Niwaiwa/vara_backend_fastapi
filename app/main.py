import logging

from app import config
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, Depends
from typing_extensions import Annotated
from app.config import get_settings

logger = logging.getLogger('app')

app = FastAPI(on_startup=[config.configure_logging])
app.add_middleware(CorrelationIdMiddleware)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/info")
async def info(settings: Annotated[config.Settings, Depends(get_settings)]):
    logger.info("info")
    return {
        "debug": settings.DEBUG,
    }