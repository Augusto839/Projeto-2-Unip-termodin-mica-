
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from pathlib import Path
from datetime import datetime
import math

app = Flask(__name__)
CORS(app)

# Caminho do banco de dados
BANCO = Path(__file__).resolve().parent / "estacao.db"


def conectar():
    conn = sqlite3.connect(BANCO)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# Receber dados do ESP32
@app.route("/dados", methods=["POST"])
def receber_dados():

    dados = request.get_json(silent=True)

    campos_numericos = [
        "temperatura",
        "umidade",
        "pressao",
        "qualidade_ar",
        "luminosidade",
        "pluviometria"
    ]

    if not isinstance(dados, dict):
        return jsonify({"erro": "Dados inválidos"}), 400

    for campo in campos_numericos:
        valor = dados.get(campo)

        if (
            not isinstance(valor, (int, float))
            or isinstance(valor, bool)
            or not math.isfinite(valor)
        ):
            return jsonify({
                "erro": f"Valor inválido: {campo}"
            }), 400

    # Qualidade do ar e luminosidade são inteiros
    for campo in ["qualidade_ar", "luminosidade"]:
        if not isinstance(dados[campo], int) or isinstance(dados[campo], bool):
            return jsonify({
                "erro": f"{campo} deve ser um número inteiro"
            }), 400

    with conectar() as conn:

        # Buscar a estação cadastrada
        estacao = conn.execute("""
            SELECT id_estacao
            FROM estacao
            ORDER BY id_estacao
            LIMIT 1
        """).fetchone()

        if estacao is None:
            return jsonify({
                "erro": "Nenhuma estação cadastrada"
            }), 400

        # Armazenar medição
        conn.execute("""
            INSERT INTO leitura (
                id_estacao,
                temperatura,
                umidade,
                pressao,
                qualidade_ar,
                luminosidade,
                pluviometria,
                data_hora
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            estacao["id_estacao"],
            dados["temperatura"],
            dados["umidade"],
            dados["pressao"],
            dados["qualidade_ar"],
            dados["luminosidade"],
            dados["pluviometria"],
            datetime.now().isoformat(timespec="seconds")
        ))

    return jsonify({
        "mensagem": "Medição armazenada com sucesso!"
    }), 201


# Buscar última medição
@app.route("/dados", methods=["GET"])
def consultar_dados():

    with conectar() as conn:
        dado = conn.execute("""
            SELECT * FROM leitura
            ORDER BY id_leitura DESC
            LIMIT 1
        """).fetchone()

    return jsonify(dict(dado) if dado else {})


# Buscar histórico
@app.route("/historico", methods=["GET"])
def historico():

    with conectar() as conn:
        dados = conn.execute("""
            SELECT * FROM leitura
            ORDER BY id_leitura DESC
            LIMIT 100
        """).fetchall()

    return jsonify([dict(d) for d in dados])


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
