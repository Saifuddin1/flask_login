from flask import Flask
import secrets
from my_app.auth import auth_bp
from my_app.database import init_db


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secrets.token_hex(16)
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:saif123@localhost/saifuddin"
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
    app.register_blueprint(auth_bp, url_prefix="/")
    init_db(app)
    return app
