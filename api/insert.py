from scraping import coleta_dado
from db import get_connection
from sqlalchemy import text
import json
import datetime


def insere_dado(dados):
    with get_connection() as conn:
        for item in dados:
            conn.execute(text("""
                INSERT INTO commodities 
                (nome, data_hora, valor_atual, valor_maximo, valor_minimo, variacao, porcentagem_var, json_commodities)
                VALUES (:nome, :data_hora, :valor_atual, :valor_maximo, :valor_minimo, :variacao, :porcentagem_var, :json_commodities)
            """), {
                "nome": item["Nome"],
                "data_hora": item["DataHoraColeta"],
                "valor_atual": float(item["UltimoValor"].replace(".", "").replace(",", ".")),
                "valor_maximo": float(item["ValorMaximo"].replace(".", "").replace(",", ".")),
                "valor_minimo": float(item["ValorMinimo"].replace(".", "").replace(",", ".")),
                "variacao": float(item["Variacao"].replace(".", "").replace(",", ".")),
                "porcentagem_var": float(item["PorcentagemVariacao"].replace(".", "").replace(",", ".")),
                "json_commodities": json.dumps(item)
            })
        conn.commit()
    print("Dados inseridos com sucesso!")


if __name__ == "__main__":
    dados = coleta_dado()
    insere_dado(dados)

with open("log_execucao.txt", "a", encoding="utf-8") as f:
    f.write(f"Script executado em {datetime.datetime.now()}\n")
    print("Log de execução atualizado.")
