from flask import Blueprint, jsonify
from bank.models.bank import Bank
from bank.routes import token_required, to_dict

bank_blueprint = Blueprint('bank_blueprint', __name__, url_prefix='/bank')


@bank_blueprint.route('/', methods=['GET'])
@token_required
def handle_all_bank():
    found_banks = Bank.query.all()
    return jsonify([to_dict(x) for x in found_banks]), 200
