from bank import db
from werkzeug.security import check_password_hash


class User(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(64), primary_key=True, unique=True)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
