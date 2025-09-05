from sqlalchemy import text
from db import get_connection


def create_tables():
    with get_connection() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS commodities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                data_hora TEXT,
                valor_atual REAL,
                valor_maximo REAL,
                valor_minimo REAL,
                variacao REAL,
                porcentagem_var REAL,
                json_commodities TEXT
            )
        """))
        conn.commit()


if __name__ == "__main__":
    create_tables()
    print("Criação com sucesso.")
