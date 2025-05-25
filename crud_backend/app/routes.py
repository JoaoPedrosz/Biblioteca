# app/routes.py

from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo.errors import DuplicateKeyError
from datetime import datetime, timedelta
from bson import ObjectId

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)

api_bp = Blueprint('api', __name__)

@api_bp.before_app_request
def ensure_indexes():
    """
    Reassegura que o índice único em 'email' esteja presente
    antes de atender qualquer requisição.
    """
    current_app.db.usuarios.create_index("email", unique=True)


#
# ROTAS DE AUTENTICAÇÃO / USUÁRIO
#

@api_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    required = ['tipo','nome','sobrenome','data_nascimento','telefone','email','senha']
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({'erro': f"Falta(m) campo(s): {', '.join(missing)}."}), 400

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


@api_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    if not data.get('email') or not data.get('senha'):
        return jsonify({'erro': 'Informe e-mail e senha.'}), 400

    user = current_app.db.usuarios.find_one({'email': data['email']})
    if not user or not check_password_hash(user['senha'], data['senha']):
        return jsonify({'erro': 'Credenciais inválidas.'}), 401

    access_token = create_access_token(
        identity=str(user['_id']),
        additional_claims={'tipo': user['tipo']},
        expires_delta=timedelta(hours=8)
    )
    return jsonify({
        'mensagem': 'Login bem-sucedido.',
        'access_token': access_token,
        'user': {
            'tipo': user['tipo'],
            'nome': user['nome'],
            'sobrenome': user['sobrenome']
        }
    }), 200


@api_bp.route('/perfil', methods=['GET'])
@jwt_required()
def perfil():
    user_id = get_jwt_identity()
    claims = get_jwt()
    user = current_app.db.usuarios.find_one(
        {'_id': ObjectId(user_id)},
        {'senha': 0}
    )
    if not user:
        return jsonify({'erro': 'Usuário não encontrado.'}), 404

    return jsonify({
        'user': {
            'id': user_id,
            'tipo': claims.get('tipo'),
            'nome': user['nome'],
            'sobrenome': user['sobrenome'],
            'email': user['email']
        }
    }), 200


#
# CRUD DE LIVROS
#

@api_bp.route('/livros', methods=['GET'])
@jwt_required()
def listar_livros():
    cursor = current_app.db.livros.find({}, {'_id': 1, 'nome': 1, 'autor': 1, 'isbn': 1})
    livros = []
    for doc in cursor:
        livros.append({
            'id': str(doc['_id']),
            'nome': doc.get('nome', ''),
            'autor': doc.get('autor', ''),
            'isbn': doc.get('isbn', '')
        })
    return jsonify(livros), 200


@api_bp.route('/livros', methods=['POST'])
@jwt_required()
def criar_livro():
    data = request.form.to_dict()
    arquivo = request.files.get('arquivo')
    required = ['nome','paginas','autor','idioma','isbn']
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({'erro': f"Falta(s) campo(s): {', '.join(missing)}"}), 400

    # Salva arquivo
    filename = None
    if arquivo:
        filename = f"{datetime.utcnow().timestamp()}_{arquivo.filename}"
        arquivo.save(f"{current_app.config['UPLOAD_FOLDER']}/{filename}")

    livro_doc = {
        'nome': data['nome'],
        'paginas': int(data['paginas']),
        'autor': data['autor'],
        'idioma': data['idioma'],
        'isbn': data['isbn'],
        'categoria': data.get('categoria', ''),
        'editora': data.get('editora', ''),
        'edicao': data.get('edicao', ''),
        'arquivo_nome': filename,
        'descricao': data.get('descricao', ''),
        'data_criacao': datetime.utcnow(),
        'user_id': ObjectId(get_jwt_identity())    # vincula ao usuário
    }
    current_app.db.livros.insert_one(livro_doc)
    return jsonify({'mensagem': 'Livro cadastrado com sucesso.'}), 201


@api_bp.route('/livros/<id_livro>', methods=['PUT'])
@jwt_required()
def atualizar_livro(id_livro):
    data = request.get_json() or {}
    update = {}
    for campo in ['nome','paginas','autor','idioma','categoria','editora','edicao','descricao']:
        if campo in data:
            update[campo] = data[campo]
    if 'paginas' in update:
        update['paginas'] = int(update['paginas'])
    if not update:
        return jsonify({'erro': 'Nenhum campo para atualizar.'}), 400

    res = current_app.db.livros.update_one(
        {'_id': ObjectId(id_livro)},
        {'$set': update}
    )
    if res.matched_count == 0:
        return jsonify({'erro': 'Livro não encontrado.'}), 404

    return jsonify({'mensagem': 'Livro atualizado com sucesso.'}), 200


@api_bp.route('/livros/<id_livro>', methods=['DELETE'])
@jwt_required()
def remover_livro(id_livro):
    res = current_app.db.livros.delete_one({'_id': ObjectId(id_livro)})
    if res.deleted_count == 0:
        return jsonify({'erro': 'Livro não encontrado.'}), 404
    return jsonify({'mensagem': 'Livro removido com sucesso.'}), 200


@api_bp.route('/livros/isbn/<isbn>', methods=['DELETE'])
@jwt_required()
def remover_livro_por_isbn(isbn):
    res = current_app.db.livros.delete_one({'isbn': isbn})
    if res.deleted_count == 0:
        return jsonify({'erro': 'Livro não encontrado para o ISBN fornecido.'}), 404
    return jsonify({'mensagem': 'Livro removido com sucesso.'}), 200


#
# MINHA ESTANTE / EMPRÉSTIMOS
#

@api_bp.route('/meus-livros', methods=['GET'])
@jwt_required()
def meus_livros():
    """
    Retorna apenas os livros deste usuário, com base na coleção 'emprestimos'.
    """
    user_identity = get_jwt_identity()

    # Encontra todos os empréstimos deste usuário
    emprestimos = current_app.db.emprestimos.find({'id_usuario': user_identity})

    resultados = []
    for emp in emprestimos:
        isbn = str(emp.get('livro_isbn'))
        livro = current_app.db.livros.find_one(
            {'isbn': isbn},
            {'_id': 1, 'nome': 1, 'arquivo_nome': 1}
        )
        if livro:
            resultados.append({
                'id': str(livro['_id']),
                'nome': livro.get('nome', ''),
                'arquivo': livro.get('arquivo_nome', '')
            })

    return jsonify(resultados), 200
