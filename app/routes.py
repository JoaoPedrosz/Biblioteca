from flask import render_template, request, jsonify
from app import app, db
from bson import ObjectId
from flask import redirect, url_for

@app.route("/ping")
def ping():
    return jsonify({"status": "ok", "livros": db.livros.count_documents({})})

@app.route('/livros/create', methods=["POST"])
def cadastrar_livro():
    data = request.json
    if not data:
        return jsonify({"erro": "Dados inválidos"}), 400

    data['disponivel'] = True  # todos os livros começam como disponíveis
    db.livros.insert_one(data)
    return jsonify({"mensagem": "Livro cadastrado com sucesso!"})


