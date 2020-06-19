from flask import Blueprint

main_blueprint = Blueprint('main_blueprint', __name__)


@main_blueprint.route('/')
def index():
    return 'Backend API is running.'  # TODO
