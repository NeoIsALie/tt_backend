from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field

from .rates import RateDb


class TickerBase(BaseModel):
    """Валюта."""
    title: str = Field(title='Наименование валюты')


class TickerDb(TickerBase):
    id: int = Field(title='ID валюты')
    current_rate: Optional[Decimal] = Field(title='Текущий курс')

    class Config:
        orm_mode = True


class TickerWithRate(TickerBase):
    rates: list[RateDb] = Field(title='Изменение курса', default_factory=list)
