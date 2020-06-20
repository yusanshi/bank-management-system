from bank import db


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    kind = db.Column(db.String(64), nullable=False)
