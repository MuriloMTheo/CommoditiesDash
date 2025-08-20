from scraping import coleta_dado
from db import connect
import psycopg2
import json
import os


def insere_dado(dados):
    conn = psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"]
    )

    cursor = conn.cursor()

    for item in dados:
        cursor.execute("""
            INSERT INTO commodities 
            (nome, data_hora, valor_atual, valor_maximo, valor_minimo, variacao, porcentagem_var, json_commodities)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            item["Nome"],
            item["DataHoraColeta"],
            float(item["UltimoValor"].replace('.', '').replace(',', '.')),
            float(item["ValorMaximo"].replace('.', '').replace(',', '.')),
            float(item["ValorMinimo"].replace('.', '').replace(',', '.')),
            float(item["Variacao"]),
            float(item["PorcentagemVariacao"].replace('%', '')),
            json.dumps(item)
        ))

    conn.commit()
    cursor.close()
    conn.close()
    print("Sucesso")


if __name__ == "__main__":
    dados = coleta_dado()
    insere_dado(dados)
