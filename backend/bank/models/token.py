from bank import db
import uuid


class Token(db.Model):
    __tablename__ = 'tokens'
    token = db.Column(db.String, default=uuid.uuid4,
                      primary_key=True, unique=True)
    expiresAt = db.Column(db.DateTime(timezone=True),
                          nullable=False, default=db.func.now())  # TODO shift time by TOKEN_EXPIRE
    user = db.Column(db.String, nullable=False)  # TODO

    def __repr__(self):
        return '<Token for {}>'.format(self.user)
