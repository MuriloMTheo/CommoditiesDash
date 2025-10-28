from flask import Flask, jsonify, Response, request
from flask_cors import CORS
from db import get_connection
from sqlalchemy import text
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)


@app.route("/commodities", methods=["GET"])
def get_commodities():
    dias = request.args.get("dias", default=0, type=int)
    try:
        nome_filtro = request.args.get(
            "nome", "").strip().lower().replace(" ", "")

        with get_connection() as conn:
            if dias == 0:
                query = text(
                    "SELECT * FROM commodities ORDER BY id, data_hora, nome;")
                result = conn.execute(query)
            else:
                data_min = (datetime.now() - timedelta(days=dias)
                            ).strftime("%Y-%m-%d")
                query = text("""
                    SELECT *
                    FROM commodities
                    WHERE substr(data_hora, 1, 10) >= :data_min
                    ORDER BY id, data_hora, nome;
                """)
                result = conn.execute(query, {"data_min": data_min})

            rows = result.fetchall()

        if nome_filtro:
            rows = [row for row in rows if nome_filtro in row._mapping["nome"].replace(
                " ", "").lower()]

        results = []
        for row in rows:
            results.append({
                "idcoleta": row._mapping["id"],
                "nome": row._mapping["nome"],
                "data_hora": row._mapping["data_hora"],
                "valor_atual": row._mapping["valor_atual"],
                "valor_maximo": row._mapping["valor_maximo"],
                "valor_minimo": row._mapping["valor_minimo"],
                "variacao": row._mapping["variacao"],
                "porcentagem_var": f"{row._mapping['porcentagem_var']}%"
            })

        return Response(json.dumps(results, ensure_ascii=False), mimetype="application/json")

    except Exception as e:
        print(e)
        return jsonify({"Erro": str(e)}), 500


@app.route("/favicon.ico")
def favicon():
    return "", 204


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
