import os
from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config

# Cria a aplicação Flask
app = Flask(
    __name__,
    static_folder="../static",
    static_url_path="/static"
)
app.config.from_object(Config)

# Garante que a pasta de uploads exista
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Libera CORS para todas as origens
CORS(app, resources={r"/*": {"origins": "*"}})

# Inicializa o JWT
jwt = JWTManager(app)

# Inicializa o cliente do MongoDB
mongodb_client = PyMongo(
    app,
    uri=(
        "mongodb+srv://joaosilva:abc123456@com759.d8vet.mongodb.net/"
        "biblioteca?retryWrites=true&w=majority&appName=COM759"
    )
)
app.db = mongodb_client.db

# Cria índice único em 'email'
app.db.usuarios.create_index("email", unique=True)

# Importa e registra as rotas
from app.routes import api_bp
app.register_blueprint(api_bp)
