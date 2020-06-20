from bank import db


class LoanClientAssociation(db.Model):
    loan_ref = db.Column(db.String(64),
                         db.ForeignKey('loan.id'),
                         primary_key=True)
    loan = db.relationship('Loan', backref='loan_client_associations')
    client_ref = db.Column(db.String(64),
                           db.ForeignKey('client.id_number'),
                           primary_key=True)
    client = db.relationship('Client', backref='loan_client_associations')
