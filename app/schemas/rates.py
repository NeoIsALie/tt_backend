from datetime import datetime
from decimal import Decimal
from random import random

from pydantic import BaseModel, Field


class BaseRate(BaseModel):
    timestamp: datetime = Field(title='Дата и время')
    rate: Decimal = Field(title='Текущий курс')


class RateDb(BaseRate):
    """Модель курса."""
    class Config:
        orm_mode = True


class Rate(BaseRate):
    """Модель курса с функцией обновления."""
    ticker_id: int = Field(title='ID валюты')

    @staticmethod
    def _generate_movement() -> int:
        """Функция генерации шага изменения курса."""
        movement = -1 if random() < 0.5 else 1
        return movement

    def update_rate(self) -> None:
        """Обновление курса."""
        new_rate = self.rate + Decimal(self._generate_movement())
        self.rate = new_rate if new_rate > Decimal(0) else Decimal(0)
