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
    """Garante índice único em 'email'."""
    current_app.db.usuarios.create_index("email", unique=True)


#
# AUTENTICAÇÃO E USUÁRIOS
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
    cursor = current_app.db.livros.find(
        {},
        {'_id': 1, 'nome': 1, 'autor': 1, 'isbn': 1, 'arquivo_nome': 1, 'disponivel': 1}
    )
    livros = []
    for doc in cursor:
        livros.append({
            'id': str(doc['_id']),
            'nome': doc.get('nome', ''),
            'autor': doc.get('autor', ''),
            'isbn': doc.get('isbn', ''),
            'arquivo': doc.get('arquivo_nome', ''),
            'disponivel': doc.get('disponivel', True)
        })
    return jsonify(livros), 200


@api_bp.route('/livros', methods=['POST'])
@jwt_required()
def criar_livro():
    data = request.form.to_dict()
    arquivo = request.files.get('arquivo')

    # Campos obrigatórios
    required = ['nome','paginas','autor','idioma','isbn']
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({'erro': f"Falta(s) campo(s): {', '.join(missing)}"}), 400

    # Salva arquivo (se houver)
    filename = None
    if arquivo:
        filename = f"{datetime.utcnow().timestamp()}_{arquivo.filename}"
        arquivo.save(f"{current_app.config['UPLOAD_FOLDER']}/{filename}")

    # Converte dispoível (string) para booleano
    disponivel = data.get('disponivel', 'true').lower() == 'true'

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
        'disponivel': disponivel
    }

    current_app.db.livros.insert_one(livro_doc)
    return jsonify({'mensagem': 'Livro cadastrado com sucesso.'}), 201


@api_bp.route('/livros/<id_livro>', methods=['PUT'])
@jwt_required()
def atualizar_livro(id_livro):
    data = request.get_json() or {}
    update = {}

    for campo in [
        'nome','paginas','autor','idioma','categoria',
        'editora','edicao','descricao','disponivel'
    ]:
        if campo in data:
            if campo == 'paginas':
                update['paginas'] = int(data['paginas'])
            elif campo == 'disponivel':
                update['disponivel'] = bool(data['disponivel'])
            else:
                update[campo] = data[campo]

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


@api_bp.route('/livros/isbn/<isbn>', methods=['GET'])
@jwt_required()
def get_livro_por_isbn(isbn):
    doc = current_app.db.livros.find_one({'isbn': isbn})
    if not doc:
        return jsonify({'erro': 'Livro não encontrado.'}), 404

    livro = {
        'id': str(doc['_id']),
        'nome': doc.get('nome', ''),
        'autor': doc.get('autor', ''),
        'paginas': doc.get('paginas', 0),
        'idioma': doc.get('idioma', ''),
        'isbn': doc.get('isbn', ''),
        'categoria': doc.get('categoria', ''),
        'editora': doc.get('editora', ''),
        'edicao': doc.get('edicao', ''),
        'descricao': doc.get('descricao', ''),
        'disponivel': doc.get('disponivel', True),
        'arquivo': doc.get('arquivo_nome', '')
    }
    return jsonify(livro), 200


#
# EMPRÉSTIMOS (MINHA ESTANTE)
#

@api_bp.route('/meus-livros', methods=['GET'])
@jwt_required()
def meus_livros():
    user_id = get_jwt_identity()
    emprestimos = current_app.db.emprestimos.find({
        'id_usuario': user_id,
        'data_devolucao_real': None
    })

    resultados = []
    for emp in emprestimos:
        isbn = emp.get('livro_isbn')
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


#
# RESERVAS / QR CODE
#

@api_bp.route('/reservar/<isbn>', methods=['POST'])
@jwt_required()
def reservar_livro(isbn):
    user_id = get_jwt_identity()

    livro = current_app.db.livros.find_one({'isbn': isbn})
    if not livro:
        return jsonify({'erro': 'Livro não encontrado.'}), 404
    if not livro.get('disponivel', True):
        return jsonify({'erro': 'Livro indisponível para reserva.'}), 400

    ativos = current_app.db.emprestimos.count_documents({
        'id_usuario': user_id,
        'data_devolucao_real': None
    })
    if ativos >= 2:
        return jsonify({'erro': 'Você já possui 2 livros emprestados.'}), 400

    agora = datetime.utcnow()
    validade = agora + timedelta(days=5)

    emprestimo = {
        'id_usuario': user_id,
        'livro_isbn': isbn,
        'data_emprestimo': agora,
        'data_devolucao_prevista': validade,
        'data_devolucao_real': None
    }
    current_app.db.emprestimos.insert_one(emprestimo)

    current_app.db.livros.update_one(
        {'_id': livro['_id']},
        {'$set': {'disponivel': False}}
    )

    qr_text = f"Livro: {livro['nome']}\nISBN: {isbn}\nValidade: {validade.date().isoformat()}"
    return jsonify({
        'mensagem': 'Reserva realizada com sucesso.',
        'qr_text': qr_text
    }), 201
