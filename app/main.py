from fastapi import FastAPI

from app.api import api_router
from app.db import database

app = FastAPI(
    title="Test_task"
)

app.include_router(api_router, prefix='/api/v1')


@app.on_event('startup')
async def startup() -> None:
    await database.connect()


@app.on_event('shutdown')
async def shutdown() -> None:
    await database.disconnect()
