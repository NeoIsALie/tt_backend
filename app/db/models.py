import datetime

from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from . import Base


class Ticker(Base):
    __tablename__ = 'tickers'

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    rates = relationship('rateshs', uselist=True, backref='ticker')


class RateHistory(Base):
    __tablename__ = 'rates'

    id = Column(Integer, primary_key=True)
    ticker_id = Column(Integer, ForeignKey('tickers.id', ondelete='CASCADE'))
    timestamp = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    rate = Column(Numeric(10, 2))
