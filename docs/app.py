from flask import Flask
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from Flask_doc.docs.views.users import users_app
from Flask_doc.docs.views.documents import documents_app
from Flask_doc.docs.views.top import top_app
from Flask_doc.docs.models.database import db
from Flask_doc.docs.views.auth import auth_app, login_manager
from Flask_doc.docs.admin.admin import admin
#from api import init_api


def create_app() -> Flask:
    app = Flask(__name__)

    app.config.from_object('Flask_doc.docs.config')
    db.init_app(app)
    migrate = Migrate(app, db, compare_type=True)

    register_blueprints(app)

    login_manager.init_app(app)
    admin.init_app(app)
    csrf = CSRFProtect()
    #api = init_api(app)

    return app


def register_blueprints(app: Flask):
    app.register_blueprint(users_app)
    app.register_blueprint(documents_app)
    app.register_blueprint(top_app)
    app.register_blueprint(auth_app)
