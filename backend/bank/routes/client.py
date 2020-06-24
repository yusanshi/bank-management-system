from flask import Blueprint, request, jsonify
from bank.models.client import Client
from bank.models.client_account_association import ClientAccountAssociation
from bank.routes import token_required, to_dict
from bank import db

client_blueprint = Blueprint('client_blueprint',
                             __name__,
                             url_prefix='/client')


@client_blueprint.route('/', methods=['GET', 'POST'])
@token_required
def handle_all_client():
    if request.method == 'GET':
        found_clients = Client.query.all()
        return jsonify([{
            **to_dict(client), 'client_account_associations':
            [to_dict(x) for x in client.client_account_associations]
        } for client in found_clients]), 200
    elif request.method == 'POST':
        if Client.query.filter_by(id_number=request.json['id_number']).first():
            return jsonify({'message': '客户已存在'}), 422
        client_account_associations = request.json.pop(
            'client_account_associations')
        for k, v in request.json.items():
            if isinstance(v, str):
                if v.strip() == '':
                    return jsonify({'message': f'{k} 值不能为空'}), 422
        client = Client(**request.json)
        client.client_account_associations = [
            ClientAccountAssociation(**association)
            for association in client_account_associations
        ]
        db.session.add(client)
        db.session.commit()
        return jsonify({}), 200


@client_blueprint.route('/<string:id_number>', methods=['PUT', 'DELETE'])
@token_required
def handle_single_client(id_number):
    query = Client.query.filter_by(id_number=id_number)
    found_client = query.first()
    if not found_client:
        return jsonify({'message': '找不到该客户'}), 422

    if request.method == 'PUT':
        if request.json['id_number'] != id_number and Client.query.filter_by(
                id_number=request.json['id_number']).first():
            return jsonify({'message': '客户的新身份证号已存在'}), 422

        client_account_associations = request.json.pop(
            'client_account_associations')
        for k, v in request.json.items():
            if isinstance(v, str):
                if v.strip() == '':
                    return jsonify({'message': f'{k} 值不能为空'}), 422
        query.update(request.json)
        for association in found_client.client_account_associations:
            db.session.delete(association)
        for x in [
                ClientAccountAssociation(**association)
                for association in client_account_associations
        ]:
            db.session.add(x)

    elif request.method == 'DELETE':
        if len(found_client.client_account_associations) != 0:
            return jsonify({'message': '客户还有关联的账户，不允许删除'}), 422
        if len(found_client.loan_client_associations) != 0:
            return jsonify({'message': '客户还有关联的贷款记录，不允许删除'}), 422

        query.delete()

    db.session.commit()
    return jsonify({}), 200
