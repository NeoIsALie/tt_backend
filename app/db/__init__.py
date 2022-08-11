from databases import Database
from sqlalchemy import MetaData, create_engine  # type: ignore
from sqlalchemy.ext.declarative import declarative_base  # type: ignore

from app.config import DATABASE_URL

database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
metadata = MetaData(bind=engine)

Base = declarative_base()
