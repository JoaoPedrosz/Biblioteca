# app/__init__.py

import os
from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from config import Config

# Cria a aplicação Flask, servindo arquivos estáticos de ../static
app = Flask(__name__, static_folder="../static", static_url_path="/static")
# Carrega as configurações de Config
app.config.from_object(Config)

# Garante que a pasta de uploads exista
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Libera CORS para todas as origens
CORS(app, resources={r"/*": {"origins": "*"}})

# Inicializa o cliente do MongoDB com a URI já presente aqui
mongodb_client = PyMongo(
    app,
    uri="mongodb+srv://joaosilva:abc123456@com759.d8vet.mongodb.net/"
        "biblioteca?retryWrites=true&w=majority&appName=COM759"
)
db = mongodb_client.db

# Importa as rotas para registrá-las na aplicação
from app import routes  
