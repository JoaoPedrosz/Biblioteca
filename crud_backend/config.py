# config.py
import os

class Config(object):
    # Chave secreta para Flask (sessions, CSRF etc)
    SECRET_KEY = os.environ.get('SECRET_KEY') or "my_secret_key"

    # Chave usada pelo Flask-JWT-Extended para assinar/verificar tokens
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or "uma-chave-muito-secreta-aqui"

    # URI de conexão com o MongoDB Atlas
    MONGO_URI = os.environ.get(
        "MONGO_URI",
        "mongodb+srv://joaosilva:abc123456@com759.d8vet.mongodb.net/"
        "trabalho_COM759?retryWrites=true&w=majority&appName=COM759"
    )

    # Caminho base do projeto (útil para formar paths relativos)
    BASEDIR = os.path.abspath(os.path.dirname(__file__))

    # Pasta onde os arquivos enviados pelo usuário vão ser salvos
    UPLOAD_FOLDER = os.path.join(BASEDIR, "static", "uploads")

    # Quais extensões de arquivos são permitidas no upload
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
