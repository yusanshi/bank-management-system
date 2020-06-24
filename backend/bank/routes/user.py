from flask import Blueprint, request, jsonify
from bank.models.user import User
from bank.models.token import Token
from bank.routes import token_required
from bank import db
from flask import current_app
from werkzeug.security import generate_password_hash

user_blueprint = Blueprint('user_blueprint', __name__, url_prefix='/user')


@user_blueprint.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']

    found_user = User.query.filter_by(username=username).first()
    if found_user:
        if found_user.check_password(password):
            new_token = Token(user=found_user)
            db.session.add(new_token)
            db.session.commit()
            return jsonify({
                'token': new_token.token,
                'expires': current_app.config['TOKEN_EXPIRE']
            }), 200

    return jsonify({'message': '账号或密码错误'}), 401


@user_blueprint.route('/logout', methods=['POST'])
def logout():
    if 'X-Token' in request.headers:
        x_token = request.headers['X-Token']

        found_token = Token.query.filter_by(token=x_token).first()
        if found_token:
            db.session.delete(found_token)
            db.session.commit()

    return jsonify({}), 200


@user_blueprint.route('/password', methods=['POST'])
@token_required
def change_password():
    found_user = Token.query.filter_by(
        token=request.headers['X-Token']).first().user
    old_password = request.json['old_password']
    new_password = request.json['new_password']

    if found_user.check_password(old_password):
        if old_password == new_password:
            return jsonify({'message': '新旧密码相同'}), 422
        return jsonify({'message': 'DEMO站点，暂不支持修改密码'}), 422
        db.session.query(Token).filter_by(user=found_user).delete()
        found_user.password = generate_password_hash(new_password)
        db.session.add(found_user)
        db.session.commit()
        return jsonify({}), 200

    return jsonify({'message': '旧密码不正确'}), 422
