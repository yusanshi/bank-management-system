from flask import Blueprint, jsonify
from bank.models.staff import Staff
from bank.routes import token_required, to_dict

staff_blueprint = Blueprint('staff_blueprint', __name__, url_prefix='/staff')


@staff_blueprint.route('/', methods=['GET'])
@token_required
def handle_all_staff():
    found_staffs = Staff.query.all()
    return jsonify([to_dict(x) for x in found_staffs]), 200
