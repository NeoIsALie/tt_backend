from fastapi import APIRouter

from . import tickers, healthcheck

api_router = APIRouter(
    responses={
        404: {"description": "Page not found"},
    },
)
api_router.include_router(tickers.api_router, prefix='/tickers')
api_router.include_router(healthcheck.api_router, prefix='/healthcheck')
