from flask import Flask, jsonify, Response, request
from flask_cors import CORS
from db import get_connection
from sqlalchemy import text
import json
import os

app = Flask(__name__)
CORS(app)


@app.route("/commodities", methods=["GET"])
def get_commodities():
    try:
        nome_filtro = request.args.get(
            "nome", "").strip().lower().replace(" ", "")
        with get_connection() as conn:
            result = conn.execute(
                text("SELECT * FROM commodities ORDER BY id, data_hora, nome"))
            rows = result.fetchall()

        if nome_filtro:
            rows = [row for row in rows if nome_filtro in row.nome.replace(
                " ", "").lower()]

        results = []
        for row in rows:
            results.append({
                "idcoleta": row.id,
                "nome": row.nome,
                "data_hora": row.data_hora,
                "valor_atual": row.valor_atual,
                "valor_maximo": row.valor_maximo,
                "valor_minimo": row.valor_minimo,
                "variacao": row.variacao,
                "porcentagem_var": f"{row.porcentagem_var}%"
            })

        return Response(json.dumps(results, ensure_ascii=False), mimetype="application/json")

    except Exception as e:
        return jsonify({"Erro": str(e)}), 500


@app.route("/favicon.ico")
def favicon():
    return "", 204


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
