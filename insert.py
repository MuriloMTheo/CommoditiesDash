import psycopg2
import requests
import json
import os
from datetime import datetime
from db import connect

url = os.environ.get('API_URL', 'http://127.0.0.1:5000/commodities')
response = requests.get(url)
dados = response.json()

conn = connect()
cursor = conn.cursor()

for item in dados:

    data_hora = item['DataHoraColeta']

    cursor.execute('''
        SELECT COUNT(*) FROM commodities WHERE nome = %s AND data_hora = %s
    ''', (item['Nome'], data_hora))

    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO commodities (
                nome, data_hora, valor_atual, valor_maximo, valor_minimo,
                variacao, porcentagem_var, json_commodities
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            item['Nome'],
            data_hora,
            float(item['UltimoValor'].replace('.', '').replace(',', '.')),
            float(item['ValorMaximo'].replace('.', '').replace(',', '.')),
            float(item['ValorMinimo'].replace('.', '').replace(',', '.')),
            float(item['Variacao'].replace(',', '.')),
            item['PorcentagemVariacao'],
            json.dumps(item, ensure_ascii=False)
        ))

conn.commit()
cursor.close()
conn.close()
print("Dados inseridos com sucesso no PostgreSQL!")
