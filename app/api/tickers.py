from datetime import datetime, timedelta
from typing import Any, Mapping

from fastapi import APIRouter, HTTPException, status

from app.db import database
from app.db.queries import get_ticker_query, get_tickers_query
from app.schemas.tickers import *

api_router = APIRouter()


@api_router.get('/', response_model=list[TickerDb])
async def get_tickers() -> list[Mapping[Any, Any]]:
    """Возвращает все существующие валюты."""
    res = await database.fetch_all(
        query=get_tickers_query(),
    )
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Tickers not found')

    return res


@api_router.get('/{ticker_id}', response_model=TickerWithRate)
async def get_ticker(
        ticker_id: int, 
        start: datetime = None, 
        end: datetime = None
) -> TickerWithRate:
    """Возвращает валюту по ее ID."""
    if end is None:
        end = datetime.now()

    if start  is None:
        start  = end - timedelta(days=1)

    if start  > end:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='"start " is upper "end"')

    db_rates = await database.fetch_all(
        query=get_ticker_query(ticker_id=ticker_id, start_time=start , end_time=end),
    )
    if not db_rates:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Tickerd with id `{ticker_id}` not found')

    ticker_with_rate = TickerWithRate.parse_obj(db_rates[0])
    for db_rate in db_rates:
        ticker_with_rate.rates.append(RateDb.parse_obj(db_rate))

    return ticker_with_rate
