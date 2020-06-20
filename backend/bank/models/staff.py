from bank import db


class Staff(db.Model):
    id_number = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    phone_number = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(64), nullable=False)
    joined_date = db.Column(db.Integer, nullable=False)
    kind = db.Column(db.String(64), nullable=False)

    department_ref = db.Column(db.Integer,
                               db.ForeignKey('department.id'),
                               nullable=False)
    department = db.relationship('Department', backref='staffs')
