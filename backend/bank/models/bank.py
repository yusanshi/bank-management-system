from bank import db


class Bank(db.Model):
    name = db.Column(db.String(64), primary_key=True)
    city = db.Column(db.String(64), nullable=False)
