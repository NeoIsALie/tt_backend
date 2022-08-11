import asyncio
import sys
from datetime import datetime
from decimal import Decimal
from time import sleep

sys.path = ['', '..'] + sys.path[1:]

from app.db import database
from app.db.queries import get_tickers_query, set_tickers_query, set_rates_query
from app.schemas import TickerDb, Rate


async def generate_tickers() -> None:
    """Генерация искусственных монет."""
    db_tickers = await database.fetch_all(get_tickers_query())
    if not db_tickers:
        await database.execute_many(query=set_tickers_query(), values=[{'title': f'ticker_{i:02}'} for i in range(100)])


async def start_tickers() -> None:
    """Генерация курсов."""
    while True:
        start_time = datetime.now()

        db_tickers = await database.fetch_all(get_tickers_query())
        for db_ticker in db_tickers:
            ticker = TickerDb.parse_obj(db_ticker)
            if ticker.current_rate is None:
                ticker.current_rate = Decimal(0)

            rate = Rate(
                ticker_id=ticker.id,
                timestamp=datetime.utcnow(),
                rate=ticker.current_rate,
            )
            rate.update_rate()
            await database.execute(query=set_rates_query(), values=rate.dict())

        run_time = (datetime.now() - start_time).total_seconds()
        sleep(1 - run_time if run_time < 1 else 0)


async def main() -> None:
    await database.connect()
    await generate_tickers()
    await start_tickers()


if __name__ == '__main__':
    asyncio.run(main())
