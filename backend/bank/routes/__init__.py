from flask import request, jsonify
from bank.models.token import Token
from datetime import datetime
from functools import wraps
from bank import db


def token_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if 'X-Token' in request.headers:
            x_token = request.headers['X-Token']
            found_token = Token.query.filter_by(token=x_token).first()
            if found_token:
                if found_token.expiresAt > int(datetime.utcnow().timestamp()):
                    return f(*args, **kwargs)
                db.session.delete(found_token)
                db.session.commit()
                return jsonify({'message': 'token 已过期，删除之'}), 401

            return jsonify({'message':
                            '找不到 token，可能是因为 token 已过期，您可以尝试重新登录'}), 401

        return jsonify({'message': '无 token'}), 401

    return wrapped


def to_dict(x, extra_fields=[]):
    return {
        c.name: getattr(x, c.name)
        for c in x.__table__.columns if hasattr(x, c.name)
    }
