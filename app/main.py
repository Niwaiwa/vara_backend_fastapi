from fastapi import FastAPI
from configs.config import settings

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/info")
async def info():
    return "test"