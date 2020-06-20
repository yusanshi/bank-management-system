from bank import db


class Client(db.Model):
    id_number = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    phone_number = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(64), nullable=False)
    contact_name = db.Column(db.String(64), nullable=False)
    contact_phone_number = db.Column(db.String(64), nullable=False)
    contact_email = db.Column(db.String(64), nullable=False)
    contact_relationship = db.Column(db.String(64), nullable=False)
    staff_ref = db.Column(db.String(64),
                          db.ForeignKey('staff.id_number'),
                          nullable=False)
    staff = db.relationship('Staff', backref='clients')
