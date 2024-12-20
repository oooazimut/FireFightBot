from sqlalchemy import create_engine, text
from config import settings


engine = create_engine(settings.sqlite_dsn, echo=True)
