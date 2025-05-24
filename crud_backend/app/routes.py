import os
import json
from flask import request, jsonify, url_for
from werkzeug.utils import secure_filename
from bson import json_util, ObjectId

from app import app, db

# -------------------
# Helpers
# -------------------

def allowed_file(filename):
    """Verifica se a extensão do arquivo está na lista ALLOWED_EXTENSIONS."""
    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )

def process_uploaded_image(field_name="imagem"):
    """
    Se houver arquivo em request.files[field_name], salva e retorna a URL pública.
    Caso contrário, retorna None.
    """
    file = request.files.get(field_name)
    if not file or file.filename == "":
        return None

    if not allowed_file(file.filename):
        return None

    filename = secure_filename(file.filename)
    destino = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(destino)

    public_url = url_for("static", filename=f"uploads/{filename}", _external=True)
    return public_url

# -------------------
# Rotas de Carros
# -------------------

@app.route("/carros", methods=["GET"])
def listar_carros():
    """Retorna lista de todos os carros."""
    cursor = db.carros.find().sort("_id", 1)
    carros = json.loads(json_util.dumps(cursor))
    return jsonify(carros), 200

@app.route("/carros/<string:carro_id>", methods=["GET"])
def get_carro(carro_id):
    """Retorna um único carro pelo ID."""
    try:
        obj_id = ObjectId(carro_id)
    except:
        return jsonify({"erro": "ID inválido"}), 400

    carro = db.carros.find_one({"_id": obj_id})
    if not carro:
        return jsonify({"erro": "Carro não encontrado"}), 404

    return jsonify(json.loads(json_util.dumps(carro))), 200

@app.route("/carros", methods=["POST"])
def criar_carro():
    """Cria um novo carro com multipart/form-data (incluindo imagem)."""
    data = {
        "modelo":       request.form.get("modelo", ""),
        "cidade":       request.form.get("cidade", ""),
        "ano":          request.form.get("ano", ""),
        "km":           request.form.get("km", ""),
        "preco":        request.form.get("preco", ""),  # <-- CORRETO AQUI
        "cambio":       request.form.get("cambio", ""),
        "carroceria":   request.form.get("carroceria", ""),
        "cor":          request.form.get("cor", ""),
        "combustivel":  request.form.get("combustivel", "")
    }

    data["imagem"] = process_uploaded_image("imagem")

    try: data["ano"] = int(data["ano"])
    except: pass
    try: data["km"] = int(data["km"])
    except: pass
    try: data["preco"] = float(data["preco"])  # <-- CORRETO AQUI
    except: pass

    res = db.carros.insert_one(data)
    return jsonify({ "mensagem": "Carro criado com sucesso", "id": str(res.inserted_id) }), 201

@app.route("/carros/<string:carro_id>", methods=["PUT"])
def atualizar_carro(carro_id):
    """Atualiza um carro existente (formato multipart/form-data)."""
    try:
        obj_id = ObjectId(carro_id)
    except:
        return jsonify({"erro": "ID inválido"}), 400

    dados = {
        "modelo":       request.form.get("modelo", ""),
        "cidade":       request.form.get("cidade", ""),
        "ano":          request.form.get("ano", ""),
        "km":           request.form.get("km", ""),
        "preco":        request.form.get("preco", ""),  # <-- CORRETO AQUI
        "cambio":       request.form.get("cambio", ""),
        "carroceria":   request.form.get("carroceria", ""),
        "cor":          request.form.get("cor", ""),
        "combustivel":  request.form.get("combustivel", "")
    }

    nova_imagem = process_uploaded_image("imagem")
    if nova_imagem:
        dados["imagem"] = nova_imagem

    try: dados["ano"] = int(dados["ano"])
    except: pass
    try: dados["km"] = int(dados["km"])
    except: pass
    try: dados["preco"] = float(dados["preco"])  # <-- CORRETO AQUI
    except: pass

    res = db.carros.update_one({"_id": obj_id}, {"$set": dados})
    if res.matched_count == 0:
        return jsonify({"erro": "Carro não encontrado"}), 404

    return jsonify({"mensagem": "Carro atualizado com sucesso"}), 200

@app.route("/carros/<string:carro_id>", methods=["DELETE"])
def deletar_carro(carro_id):
    """Exclui um carro pelo ID."""
    try:
        obj_id = ObjectId(carro_id)
    except:
        return jsonify({"erro": "ID inválido"}), 400

    res = db.carros.delete_one({"_id": obj_id})
    if res.deleted_count == 0:
        return jsonify({"erro": "Carro não encontrado"}), 404

    return jsonify({"mensagem": "Carro removido com sucesso"}), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    print(f"[LOGIN] E-mail recebido: {email}")
    print(f"[LOGIN] Senha recebida: {password}")

    user = db.usuario.find_one({ "email": email })

    if not user or user.get('password') != password:
        print("[LOGIN] Falha: usuário ou senha inválidos.")
        return jsonify({ "erro": "Usuário ou senha inválidos" }), 401

    print("[LOGIN] Sucesso!")
    return jsonify({
        "access_token": "fake-token",
        "user": {
            "email": user["email"],
            "tipo": user["tipo"]
        }
    }), 200

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    required_fields = ['nome', 'email', 'cpf', 'telefone', 'data_nascimento', 'password', 'tipo']

    # Verifica se todos os campos obrigatórios estão presentes
    for field in required_fields:
        if not data.get(field):
            return jsonify({'erro': f'Campo {field} é obrigatório'}), 400

    # Verifica se email já está cadastrado
    if db.usuario.find_one({ "email": data['email'] }):
        return jsonify({'erro': 'E-mail já cadastrado'}), 409

    # Salva o novo usuário
    db.usuario.insert_one({
        "nome": data['nome'],
        "email": data['email'],
        "cpf": data['cpf'],
        "telefone": data['telefone'],
        "data_nascimento": data['data_nascimento'],
        "password": data['password'],
        "tipo": data.get('tipo', 'usuario')
    })

    return jsonify({'mensagem': 'Usuário cadastrado com sucesso'}), 201







