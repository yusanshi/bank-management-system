from flask import Blueprint, request, jsonify
from bank.models.loan import Loan
from bank.models.loan_client_association import LoanClientAssociation
from bank.models.payment import Payment
from bank.routes import token_required, to_dict
from bank import db

loan_blueprint = Blueprint('loan_blueprint', __name__, url_prefix='/loan')


@loan_blueprint.route('/', methods=['GET', 'POST'])
@token_required
def handle_all_loan():
    if request.method == 'GET':
        found_loans = Loan.query.all()
        return jsonify([{
            **to_dict(loan), 'payments': [to_dict(x) for x in loan.payments],
            'clients':
            [to_dict(x.client) for x in loan.loan_client_associations]
        } for loan in found_loans]), 200
    elif request.method == 'POST':
        clients = request.json.pop('clients')
        del request.json['id']
        loan = Loan(**request.json)
        db.session.add(loan)
        db.session.commit()
        for client_ref in clients:
            db.session.add(
                LoanClientAssociation(loan_ref=loan.id, client_ref=client_ref))
        db.session.commit()
        return jsonify({
            **to_dict(loan), 'payments': [to_dict(x) for x in loan.payments],
            'clients':
            [to_dict(x.client) for x in loan.loan_client_associations]
        }), 200


@loan_blueprint.route('/<int:id>/payment', methods=['POST'])
@token_required
def handle_single_loan_add_payment(id):
    query = Loan.query.filter_by(id=id)
    found_loan = query.first()
    if not found_loan:
        return jsonify({'message': '找不到这笔贷款'}), 422
    if found_loan.status == '已全部发放':
        return jsonify({'message': '已全部发放，不允许添加支付'}), 422
    request.json['money'] = float(request.json['money'])
    found_loan.payments.append(Payment(**request.json))
    if sum([x.money for x in found_loan.payments]) > found_loan.money:
        return jsonify({'message': '付款总金额超过贷款金额'}), 422
    elif sum([x.money for x in found_loan.payments]) == found_loan.money:
        found_loan.status = '已全部发放'
    elif found_loan.status == '未开始发放':
        found_loan.status = '发放中'
    db.session.commit()
    return jsonify({
        **to_dict(found_loan), 'payments':
        [to_dict(x) for x in found_loan.payments],
        'clients':
        [to_dict(x.client) for x in found_loan.loan_client_associations]
    }), 200


@loan_blueprint.route('/<int:id>', methods=['DELETE'])
@token_required
def handle_single_loan(id):
    found_loan = Loan.query.filter_by(id=id).first()
    if not found_loan:
        return jsonify({'message': '找不到这笔贷款'}), 422
    if found_loan.status == '发放中':
        return jsonify({'message': '发放中的贷款不允许删除'}), 422
    # TODO how to delete better
    for x in found_loan.payments:
        db.session.delete(x)
    for x in found_loan.loan_client_associations:
        db.session.delete(x)
    db.session.delete(found_loan)
    db.session.commit()
    return jsonify({}), 200
