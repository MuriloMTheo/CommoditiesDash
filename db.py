import psycopg2
import os


def connect():
    dsn = os.getenv("DATABASE_URL")
    print(f"DEBUG DATABASE_URL: {dsn}")
    if not dsn:
        raise Exception("DATABASE_URL não está definida no ambiente")
    return psycopg2.connect(dsn)
