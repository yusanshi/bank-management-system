from flask import Blueprint, request, jsonify
from bank.models.user import User
from bank import db
import uuid
import datetime

user_blueprint = Blueprint(
    'user_blueprint', __name__, url_prefix='/user')


@user_blueprint.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    if username and password:
        found_user = User.query.filter(User.username == username).first()
        if found_user:
            if found_user.check_password(password):
                token = uuid.uuid4().hex
                expire = datetime.datetime.now() + datetime.timedelta(hours=2)
                found_user.tokens = found_user.tokens.copy()
                found_user.tokens[token] = expire
                db.session.commit()
                return jsonify({
                    'status': 'success',
                    'token': token,
                    'expire': expire
                })
            return jsonify({
                'status': 'failure',
                'error': 'Username or password error.'
            })
        return jsonify({
            'status': 'failure',
            'error': 'User not found.'
        })
    return jsonify({
        'status': 'failure',
        'error': 'Empty username or password.'
    })
