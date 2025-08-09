import psycopg2
import os


def connect():
    dsn = os.getenv("DATABASE_URL")
    return psycopg2.connect(dsn)
