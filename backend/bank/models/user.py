from bank import db
from werkzeug.security import check_password_hash


class User(db.Model):
    username = db.Column(db.String(64), primary_key=True)
    password = db.Column(db.String(64), nullable=False)

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
