import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Set default value
    app.config.from_mapping(
        SECRET_KEY='WhosYourDaddy',
        SQLALCHEMY_DATABASE_URI='sqlite:///' +
        os.path.join(app.instance_path, 'bank.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,

        ADMIN_USERNAME='admin',
        ADMIN_PASSWORD='admin',
        TOKEN_EXPIRE=3600
    )

    # Load config file relative to instance folder
    app.config.from_pyfile('config.py')

    db.init_app(app)

    from bank.routes.user import user_blueprint
    app.register_blueprint(user_blueprint)
    from bank.routes.main import main_blueprint
    app.register_blueprint(main_blueprint)

    with app.app_context():
        db.create_all()

        from bank.models.user import User
        if User.query.all():
            print("Load existing database.")
        else:
            new_user = User(username=app.config['ADMIN_USERNAME'], password=generate_password_hash(
                app.config['ADMIN_PASSWORD']))
            db.session.add(new_user)
            db.session.commit()
            print(
                f"This is a new database. Create admin user: {app.config['ADMIN_USERNAME']}.")

    return app
