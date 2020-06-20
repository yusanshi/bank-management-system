from bank import db


class Account(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    balance = db.Column(db.Float, nullable=False)
    open_date = db.Column(db.Integer, nullable=False)
    account_type = db.Column(db.String(64), nullable=False)
    bank_ref = db.Column(db.String(64),
                         db.ForeignKey('bank.name'),
                         nullable=False)
    bank = db.relationship('Bank', backref='accounts')

    __mapper_args__ = {'polymorphic_on': account_type}


class DepositAccount(Account):
    interest_rate = db.Column(db.Float)
    currency_type = db.Column(db.String)
    __mapper_args__ = {'polymorphic_identity': 'deposit'}


class ChequeAccount(Account):
    overdraft = db.Column(db.Float)
    __mapper_args__ = {'polymorphic_identity': 'cheque'}
