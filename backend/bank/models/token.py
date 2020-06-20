from bank import db
import uuid
from datetime import datetime
from flask import current_app


class Token(db.Model):
    token = db.Column(db.String(64),
                      default=lambda: str(uuid.uuid4()),
                      primary_key=True)
    expiresAt = db.Column(db.Integer,
                          nullable=False,
                          default=lambda: int(datetime.utcnow().timestamp()) +
                          current_app.config['TOKEN_EXPIRE'])
    user_ref = db.Column(db.String(64),
                         db.ForeignKey('user.username'),
                         nullable=False)
    user = db.relationship('User', backref='tokens')
