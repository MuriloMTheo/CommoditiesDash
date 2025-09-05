import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

DEFAULT_SQLITE = "sqlite:///./data/commodities.db"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_SQLITE)

engine = create_engine(DATABASE_URL, future=True)


def get_connection():
    return engine.connect()
