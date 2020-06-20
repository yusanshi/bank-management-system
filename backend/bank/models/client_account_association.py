from bank import db


class ClientAccountAssociation(db.Model):
    client_ref = db.Column(db.String(64),
                           db.ForeignKey('client.id_number'),
                           primary_key=True)
    client = db.relationship('Client', backref='client_account_associations')
    account_ref = db.Column(db.String(64),
                            db.ForeignKey('account.id'),
                            primary_key=True)
    account = db.relationship('Account', backref='client_account_associations')
    last_visit_date = db.Column(db.Integer, nullable=False, default=0)
