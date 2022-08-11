from datetime import datetime

from sqlalchemy import insert  # type: ignore

from app.db.models import Ticker, RateHistory


def get_tickers_query() -> str:
    """Запрос списка монет с их текущим курсом.
    """
    return """
        WITH max_rate AS (
            SELECT rh.ticker_id        as ticker_id,
                   max(rh.timestamp) as max_timestamp
            FROM rates rh
            GROUP BY rh.ticker_id
        )
        SELECT c.id    as id,
               c.title as title,
               rh.rate as current_rate
        FROM tickers c
            LEFT JOIN max_rate mr on c.id = mr.ticker_id
            LEFT JOIN rates rh on c.id = rh.ticker_id AND rh.timestamp = mr.max_timestamp;
    """


def get_ticker_query(ticker_id: int, start_time: datetime, end_time: datetime) -> str:
    """Запрос истории курса.

    ticker_id: ID валюты
    start_time: Дата и время начала запрашиваемого периода, включительно
    end_time: Дата и время конца запрашиваемого периода, не включительно
    """
    return f"""
        SELECT c.id              as id,
               c.title           as title,
               rh.timestamp      as timestamp,
               rh.rate           as rate
        FROM tickers c
                 LEFT JOIN rates rh on c.id = rh.ticker_id
        WHERE c.id = {ticker_id}
        AND rh.timestamp >= '{start_time}'
        AND rh.timestamp < '{end_time}';
    """


def set_tickers_query() -> str:
    return insert(Ticker)


def set_rates_query() -> str:
    return insert(RateHistory)
