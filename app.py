import json
import requests
import os
from flask import Flask, Response, request
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)


def coleta_dados():
    url = "https://br.investing.com/commodities/softs"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        rows = soup.select("table tbody tr")
        result = []

        for row in rows:
            columns = row.find_all("td")

            if len(columns) >= 9:
                nome = columns[1].text.strip()
                mes = columns[2].text.strip()
                valorultimo = columns[3].text.strip()
                valormax = columns[4].text.strip()
                valormin = columns[5].text.strip()
                variacao = columns[6].text.strip()
                variacaoporcetagem = columns[7].text.strip()
                hora = columns[8].text.strip()

                data_atual = datetime.now().strftime("%Y-%m-%d")
                data_hora_coleta = f"{data_atual} {hora}"

                result.append({
                    "Nome": nome,
                    "DataHoraColeta": data_hora_coleta,
                    "Mes": mes,
                    "UltimoValor": valorultimo,
                    "ValorMaximo": valormax,
                    "ValorMinimo": valormin,
                    "Variacao": variacao,
                    "PorcentagemVariacao": variacaoporcetagem
                })
        return result
    except Exception as e:
        print(f"Erro ao coletar dados: {e}")
        return []


@app.route("/commodities")
def commodities():
    exemplo = [
        {"Nome": "Teste", "DataHoraColeta": "2025-08-01 12:00", "Mes": "Ago",
         "UltimoValor": "100", "ValorMaximo": "110", "ValorMinimo": "90",
         "Variacao": "+1", "PorcentagemVariacao": "+1%"}
    ]
    json_str = json.dumps(exemplo, ensure_ascii=False)
    return Response(json_str, mimetype='application/json; charset=utf-8')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
