from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo.errors import DuplicateKeyError
from datetime import datetime

api_bp = Blueprint('api', __name__)

@api_bp.before_app_request
def ensure_indexes():
    """
    Reassegura que o índice único em 'email' esteja presente
    antes de atender qualquer requisição.
    """
    current_app.db.usuarios.create_index("email", unique=True)

@api_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}

    required = [
        'tipo',
        'nome',
        'sobrenome',
        'data_nascimento',  # agora padronizado
        'telefone',
        'email',
        'senha'
    ]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({
            'erro': f"Falta(m) campo(s): {', '.join(missing)}."
        }), 400

    user_doc = {
        'tipo': data['tipo'],
        'nome': data['nome'],
        'sobrenome': data['sobrenome'],
        'data_nascimento': data['data_nascimento'],
        'telefone': data['telefone'],
        'email': data['email'],
        'senha': generate_password_hash(data['senha']),
        'status': 'ativo',
        'data_criacao': datetime.utcnow()
    }

    try:
        current_app.db.usuarios.insert_one(user_doc)
    except DuplicateKeyError:
        return jsonify({'erro': 'E-mail já cadastrado.'}), 409

    return jsonify({'mensagem': 'Conta criada com sucesso.'}), 201

# … suas outras rotas (login, livros, etc.) aqui …
