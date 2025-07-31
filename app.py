import json
import requests
import os
from flask import Flask, Response, request
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)


def coleta_dados():
    url = "https://br.investing.com/commodities/softs"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.content, "html.parser")

    rows = soup.select("table tbody tr")
    result = []

    for row in rows:
        columns = row.find_all("td")
        if len(columns) >= 8:
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


@app.route("/commodities")
def commodities():
    filtro = request.args.get("nome")
    print(f"Filtro recebido: {filtro}")

    dados = coleta_dados()

    if filtro:
        filtro = filtro.lower().replace(" ", "")
        dados = [
            item for item in dados if filtro in item["Nome"].lower().replace(" ", "")
        ]
    else:
        print("Nenhum filtro aplicado")

    json_str = json.dumps(dados, ensure_ascii=False)
    return Response(json_str, mimetype='application/json; charset=utf-8')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
