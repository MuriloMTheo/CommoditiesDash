import requests
from bs4 import BeautifulSoup
from datetime import datetime
import psycopg2
import json
import os
from dotenv import load_dotenv

load_dotenv()


def coleta_dado():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    url = "https://br.investing.com/commodities/softs"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    tabela = soup.find("table")
    linhas = tabela.find_all("tr")

    results = []

    for linha in linhas:
        columns = linha.find_all("td")
        if len(columns) < 9:
            continue

        try:
            nome = columns[1].find("a").text.strip()
            mes = columns[2].text.strip()
            valor_ultimo = columns[3].text.strip().replace(",", ".")
            valor_max = columns[4].text.strip().replace(",", ".")
            valor_min = columns[5].text.strip().replace(",", ".")
            variacao = columns[6].text.strip().replace(",", ".")
            variacao_porc = columns[7].text.strip().replace(
                ",", ".").replace("%", "")
            hora = columns[8].find("time").text.strip()

            data_atual = datetime.now().strftime("%Y-%m-%d")
            data_hora_coleta = f"{data_atual} {hora}"

            resultado = {
                "Nome": nome,
                "DataHoraColeta": data_hora_coleta,
                "Mes": mes,
                "UltimoValor": valor_ultimo,
                "ValorMaximo": valor_max,
                "ValorMinimo": valor_min,
                "Variacao": variacao,
                "PorcentagemVariacao": variacao_porc
            }

            results.append(resultado)

        except Exception as e:
            print(f"Erro ao processar linha: {e}")
            continue

    return results


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
