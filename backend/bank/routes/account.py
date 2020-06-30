from flask import Blueprint, request, jsonify
from bank.models.account import Account, DepositAccount, ChequeAccount
from bank.models.client import Client
from bank.models.client_account_association import ClientAccountAssociation
from bank.routes import token_required, to_dict
from bank import db

account_blueprint = Blueprint('account_blueprint',
                              __name__,
                              url_prefix='/account')


@account_blueprint.route('/', methods=['GET', 'POST'])
@token_required
def handle_all_account():
    if request.method == 'GET':
        found_accounts = Account.query.all()
        return jsonify([{
            **to_dict(account), 'client_account_associations':
            [to_dict(x) for x in account.client_account_associations]
        } for account in found_accounts]), 200
    elif request.method == 'POST':
        if Account.query.filter_by(id=request.json['id']).first():
            return jsonify({'message': '账户已存在'}), 422
        client_account_associations = request.json.pop(
            'client_account_associations')
        for x in client_account_associations:
            for y in Client.query.get(
                    x['client_ref']).client_account_associations:
                if y.account.account_type == request.json[
                        'account_type'] and y.account.bank_ref == request.json[
                            'bank_ref']:
                    return jsonify({
                        'message':
                        f"客户{x['client_ref']}在{request.json['bank_ref']}已经有一个{request.json['account_type']}账户"
                    }), 422
        for k, v in request.json.items():
            if isinstance(v, str):
                if v.strip() == '':
                    return jsonify({'message': f'{k} 值不能为空'}), 422
        if request.json['account_type'] == 'deposit':
            account = DepositAccount(**request.json)
        elif request.json['account_type'] == 'cheque':
            account = ChequeAccount(**request.json)
        else:
            return jsonify({'message': '未知账户类型'}), 422
        account.client_account_associations = [
            ClientAccountAssociation(**association)
            for association in client_account_associations
        ]
        db.session.add(account)
        db.session.commit()
        return jsonify({}), 200


@account_blueprint.route('/<string:id>', methods=['PUT', 'DELETE'])
@token_required
def handle_single_account(id):
    found_account = Account.query.filter_by(id=id).first()
    if not found_account:
        return jsonify({'message': '找不到该账户'}), 422

    if request.method == 'PUT':
        if request.json['id'] != id:
            return jsonify({'message': '不允许修改账户号'}), 422
        client_account_associations = request.json.pop(
            'client_account_associations')
        for x in client_account_associations:
            for y in Client.query.get(
                    x['client_ref']).client_account_associations:
                if y.account.id != request.json[
                        'id'] and y.account.account_type == request.json[
                            'account_type'] and y.account.bank_ref == request.json[
                                'bank_ref']:
                    return jsonify({
                        'message':
                        f"客户{x['client_ref']}在{request.json['bank_ref']}已经有一个{request.json['account_type']}账户"
                    }), 422
        for k, v in request.json.items():
            if isinstance(v, str):
                if v.strip() == '':
                    return jsonify({'message': f'{k} 值不能为空'}), 422
        if request.json['account_type'] == 'deposit':
            DepositAccount.query.filter_by(id=id).update(request.json)
        elif request.json['account_type'] == 'cheque':
            ChequeAccount.query.filter_by(id=id).update(request.json)
        else:
            return jsonify({'message': '未知账户类型'}), 422
        for association in found_account.client_account_associations:
            db.session.delete(association)
        for x in [
                ClientAccountAssociation(**association)
                for association in client_account_associations
        ]:
            db.session.add(x)

    elif request.method == 'DELETE':
        for x in found_account.client_account_associations:
            db.session.delete(x)
        db.session.delete(found_account)

    db.session.commit()
    return jsonify({}), 200
