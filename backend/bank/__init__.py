import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from flask_cors import CORS

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)

    # Set default value
    app.config.from_mapping(SQLALCHEMY_DATABASE_URI='sqlite:///' +
                            os.path.join(app.instance_path, 'bank.db'),
                            SQLALCHEMY_TRACK_MODIFICATIONS=False,
                            ADMIN_USERNAME='admin',
                            ADMIN_PASSWORD='admin',
                            TOKEN_EXPIRE=36000,
                            GENERATE_SAMPLE_DATA=True,
                            CONTACT_RELATIONSHIPS=['父子', '母子', '兄弟'],
                            CURRENCY_TYPES=['人民币', '美元', '日元', '津巴布韦币'])

    # Load config file relative to instance folder
    app.config.from_pyfile('config.py')

    db.init_app(app)

    with app.app_context():
        from bank.models.client import Client
        from bank.models.account import DepositAccount, ChequeAccount
        from bank.models.client_account_association import ClientAccountAssociation
        from bank.models.staff import Staff
        from bank.models.department import Department
        from bank.models.bank import Bank
        from bank.models.loan import Loan
        from bank.models.loan_client_association import LoanClientAssociation
        from bank.models.payment import Payment

        from bank.routes.user import user_blueprint
        app.register_blueprint(user_blueprint)
        from bank.routes.client import client_blueprint
        app.register_blueprint(client_blueprint)
        from bank.routes.account import account_blueprint
        app.register_blueprint(account_blueprint)
        from bank.routes.loan import loan_blueprint
        app.register_blueprint(loan_blueprint)
        from bank.routes.bank import bank_blueprint
        app.register_blueprint(bank_blueprint)
        from bank.routes.staff import staff_blueprint
        app.register_blueprint(staff_blueprint)

        db.create_all()

        from bank.models.user import User
        if User.query.all():
            print("Load existing database.")
        else:
            new_user = User(username=app.config['ADMIN_USERNAME'],
                            password=generate_password_hash(
                                app.config['ADMIN_PASSWORD']))
            db.session.add(new_user)
            db.session.commit()
            print(
                f"This is a new database. Create admin user: {app.config['ADMIN_USERNAME']}."
            )

            if app.config['GENERATE_SAMPLE_DATA']:
                from faker import Faker
                fake = Faker('zh_CN')
                import random
                import string
                from datetime import datetime
                current_utc = int(datetime.utcnow().timestamp())

                banks_city = [fake.city() for _ in range(random.randint(4, 8))]
                banks_city = list(set(banks_city))
                banks = [
                    Bank(name=f'{city}第一支行', city=city) for city in banks_city
                ]
                banks_name = [bank.name for bank in banks]

                for x in banks:
                    db.session.add(x)

                departments = [
                    Department(
                        name=
                        f"最{random.choice(['棒','🐮','酷','美'])}{department_kind}",
                        kind=department_kind,
                        staffs=[
                            Staff(id_number=fake.ssn(),
                                  name=fake.name(),
                                  phone_number=fake.phone_number(),
                                  address=fake.address().split()[0],
                                  joined_date=random.randint(
                                      current_utc - 1e8, current_utc - 1e6),
                                  kind='部门经理')
                        ] + [
                            Staff(id_number=fake.ssn(),
                                  name=fake.name(),
                                  phone_number=fake.phone_number(),
                                  address=fake.address().split()[0],
                                  joined_date=random.randint(
                                      current_utc - 1e8, current_utc - 1e6),
                                  kind='普通员工')
                            for _ in range(random.randint(8, 16))
                        ]) for department_kind in ['技术部', '财务部', '业务部', '后勤部']
                ]

                for x in departments:
                    db.session.add(x)

                staffs_id_number = [
                    staff.id_number for department in departments
                    for staff in department.staffs
                ]

                clients = [
                    Client(id_number=fake.ssn(),
                           name=fake.name(),
                           phone_number=fake.phone_number(),
                           address=fake.address().split()[0],
                           contact_name=fake.name(),
                           contact_phone_number=fake.phone_number(),
                           contact_email=fake.free_email(),
                           contact_relationship=random.choice(
                               app.config['CONTACT_RELATIONSHIPS']),
                           staff_ref=random.choice(staffs_id_number))
                    for _ in range(random.randint(32, 64))
                ]

                for x in clients:
                    db.session.add(x)

                clients_id_number = [client.id_number for client in clients]

                accounts = [
                    DepositAccount(id=''.join(
                        random.choices(string.digits, k=16)),
                                   balance=random.uniform(1e2, 1e8),
                                   open_date=random.randint(
                                       current_utc - 1e8, current_utc - 1e6),
                                   account_type='deposit',
                                   bank_ref=random.choice(banks_name),
                                   interest_rate=random.uniform(1e-3, 1e-1),
                                   currency_type=random.choice(
                                       app.config['CURRENCY_TYPES']))
                    for _ in range(random.randint(16, 32))
                ] + [
                    ChequeAccount(id=''.join(
                        random.choices(string.digits, k=16)),
                                  balance=random.uniform(1e2, 1e8),
                                  open_date=random.randint(
                                      current_utc - 1e8, current_utc - 1e6),
                                  account_type='cheque',
                                  bank_ref=random.choice(banks_name),
                                  overdraft=random.uniform(1e2, 1e8))
                    for _ in range(random.randint(16, 32))
                ]

                for x in accounts:
                    db.session.add(x)

                accounts_id = [account.id for account in accounts]

                client_account_associations = []

                for account_id in accounts_id:
                    # make sure each account has at least one client
                    client_account_associations.append(
                        (random.choice(clients_id_number), account_id))

                for _ in range(
                        int(len(clients_id_number) * len(accounts_id) * 0.02)):
                    client_id_nubmer = random.choice(clients_id_number)
                    account_id = random.choice(accounts_id)
                    if (client_id_nubmer,
                            account_id) not in client_account_associations:
                        client_account_associations.append(
                            (client_id_nubmer, account_id))

                for client_id_nubmer, account_id in client_account_associations:
                    db.session.add(
                        ClientAccountAssociation(
                            client_ref=client_id_nubmer,
                            account_ref=account_id,
                            last_visit_date=random.randint(
                                current_utc - 1e8, current_utc - 1e3)))

                def split_randomly(target, parts):
                    assert target > 0
                    assert parts >= 1
                    ret = [random.uniform(0, 1) for _ in range(parts)]
                    ret = list(map(lambda x: x * target / sum(ret), ret))
                    return ret

                loans = []
                for _ in range(random.randint(16, 32)):
                    choice = random.choice(range(3))
                    target_money = random.uniform(1e2, 1e8)
                    if choice == 0:
                        loans.append(
                            Loan(money=target_money,
                                 status='未开始发放',
                                 bank_ref=random.choice(banks_name),
                                 payments=[]))
                    elif choice == 1:
                        loans.append(
                            Loan(money=target_money,
                                 status='发放中',
                                 bank_ref=random.choice(banks_name),
                                 payments=[
                                     Payment(pay_date=random.randint(
                                         current_utc - 1e8, current_utc - 1e3),
                                             money=x)
                                     for x in split_randomly(
                                         random.uniform(0, target_money),
                                         random.randint(1, 3))
                                 ]))
                    elif choice == 2:
                        loans.append(
                            Loan(money=target_money,
                                 status='已全部发放',
                                 bank_ref=random.choice(banks_name),
                                 payments=[
                                     Payment(pay_date=random.randint(
                                         current_utc - 1e8, current_utc - 1e3),
                                             money=x)
                                     for x in split_randomly(
                                         target_money, random.randint(1, 5))
                                 ]))
                for x in loans:
                    db.session.add(x)

                # commit it now in order to get access to loan.id
                db.session.commit()

                loans_id = [loan.id for loan in loans]
                loan_client_associations = []

                for loan_id in loans_id:
                    # make sure each loan has at least one client
                    loan_client_associations.append(
                        (loan_id, random.choice(clients_id_number)))

                for _ in range(
                        int(len(loans_id) * len(clients_id_number) * 0.02)):
                    loan_id = random.choice(loans_id)
                    client_id_number = random.choice(clients_id_number)
                    if (loan_id,
                            client_id_number) not in loan_client_associations:
                        loan_client_associations.append(
                            (loan_id, client_id_number))

                for loan_id, client_id_number in loan_client_associations:
                    db.session.add(
                        LoanClientAssociation(loan_ref=loan_id,
                                              client_ref=client_id_number))

                db.session.commit()

    return app
