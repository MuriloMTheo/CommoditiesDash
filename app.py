from flask import Flask, jsonify, Response
from dotenv import load_dotenv
import json
import os
import psycopg2
import psycopg2.extras

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

app = Flask(__name__)


def get_connection():
    return psycopg2.connect(DATABASE_URL)


@app.route("/commodities", methods=["GET"])
def get_commodities():
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cur.execute(
            "SELECT * FROM commodities ORDER BY data_hora, nome")
        rows = cur.fetchall()

        results = []
        for row in rows:
            results.append({
                "idcoleta": row["idcoleta"],
                "nome": row["nome"],
                "data_hora": row["data_hora"],
                "valor_atual": (row["valor_atual"]),
                "valor_maximo": (row["valor_maximo"]),
                "valor_minimo": (row["valor_minimo"]),
                "variacao": (row["variacao"]),
                "porcentagem_var": f"{str(row['porcentagem_var']).replace('%', '')}%",
                "json_completo": row["json_commodities"]
            })

        cur.close()
        conn.close()

        return Response(json.dumps(results, ensure_ascii=False), mimetype="application/json")
    except Exception as e:
        return jsonify({"Erro": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
