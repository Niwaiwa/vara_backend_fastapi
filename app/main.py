import logging

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware
from typing_extensions import Annotated

from app import config
from app.config import get_settings
from app.api.v1.router import api_router


logger = logging.getLogger('app')

app = FastAPI(on_startup=[config.configure_logging], openapi_url="/api/openapi.json")
app.add_middleware(CorrelationIdMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=['X-Requested-With', 'X-Request-ID', 'Content-Type', 'Accept', 'Authorization'],
    expose_headers=['X-Request-ID'])
app.include_router(api_router, prefix="/api")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/info")
async def info(settings: Annotated[config.Settings, Depends(get_settings)]):
    logger.info("info")
    return {
        "debug": settings.DEBUG,
    }

