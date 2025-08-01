import psycopg2
import requests
import json
import os
from db import connect

url = os.environ.get(
    'API_URL', 'https://web-production-38e46.up.railway.app/commodities')
response = requests.get(url)
dados = response.json()

conn = connect()
cursor = conn.cursor()

if isinstance(dados, list) and all(isinstance(item, dict) for item in dados):
    for item in dados:
        data_hora = item.get('DataHoraColeta')
        if not data_hora:
            continue

        cursor.execute(
            'SELECT COUNT(*) FROM commodities WHERE nome = %s AND data_hora = %s',
            (item.get('Nome'), data_hora)
        )
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                'INSERT INTO commodities (nome, data_hora, valor_atual, valor_maximo, valor_minimo, variacao, porcentagem_var, json_commodities) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                (
                    item.get('Nome'),
                    data_hora,
                    float(item.get('UltimoValor', '0').replace(
                        '.', '').replace(',', '.')),
                    float(item.get('ValorMaximo', '0').replace(
                        '.', '').replace(',', '.')),
                    float(item.get('ValorMinimo', '0').replace(
                        '.', '').replace(',', '.')),
                    float(item.get('Variacao', '0').replace(',', '.')),
                    item.get('PorcentagemVariacao', ''),
                    json.dumps(item, ensure_ascii=False)
                )
            )
else:
    print("Erro: resposta da API não é uma lista de dicionários ou está vazia.")
    print(dados)

conn.commit()
cursor.close()
conn.close()
