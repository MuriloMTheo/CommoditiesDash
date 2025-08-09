import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


def connect():
    dsn = os.getenv("DATABASE_URL")
    return psycopg2.connect(dsn)
