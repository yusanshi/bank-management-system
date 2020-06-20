from bank import db


class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    money = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(64), nullable=False)
    bank_ref = db.Column(db.String(64),
                         db.ForeignKey('bank.name'),
                         nullable=False)
    bank = db.relationship('Bank', backref='loans')
