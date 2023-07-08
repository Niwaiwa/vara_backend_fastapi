from functools import lru_cache
from fastapi import FastAPI, Depends
from typing_extensions import Annotated
from app import config

app = FastAPI()

@lru_cache()
def get_settings():
    return config.Settings()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/info")
async def info(settings: Annotated[config.Settings, Depends(get_settings)]):
    return {
        "debug": settings.debug,
    }