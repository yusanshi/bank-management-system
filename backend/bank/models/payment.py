from bank import db


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pay_date = db.Column(db.Integer, nullable=False)
    money = db.Column(db.Float, nullable=False)
    loan_ref = db.Column(db.Integer, db.ForeignKey('loan.id'), nullable=False)
    loan = db.relationship('Loan', backref='payments')
