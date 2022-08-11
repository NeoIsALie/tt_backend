from fastapi import APIRouter

api_router = APIRouter()


@api_router.get("/")
async def healthcheck() -> dict:
    return {"status": "alive"}
