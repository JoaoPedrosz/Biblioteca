# config.py
import os

class Config(object):
    # Secret key (só se você usar sessões ou algo parecido)
    SECRET_KEY = os.environ.get('SECRET_KEY') or "my_secret_key"

    # URI do seu MongoDB Atlas
    MONGO_URI = os.environ.get(
        "MONGO_URI",
        "mongodb+srv://joaosilva:abc123456@com759.d8vet.mongodb.net/"
        "trabalho_COM759?retryWrites=true&w=majority&appName=COM759"
    )

    # Caminho absoluto para salvar uploads
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASEDIR, "static", "uploads")

    # Extensões permitidas para upload
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
