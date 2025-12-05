"""
App Package
"""
from dotenv import load_dotenv
from flask import Flask
from flask_ckeditor import CKEditor
import os

load_dotenv()

ckeditor = CKEditor()

def create_app():
    app = Flask(__name__)
    # app.config.from_object('config.Config')

    ckeditor.init_app(app)

    from .admin import admin_bp
    app.register_blueprint(admin_bp)

    from .main import main_bp
    app.register_blueprint(main_bp)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['CKEDITOR_PKG_TYPE'] = 'basic'
    app.config['CKEDITOR_ENABLE_CODESNIPPET'] = False
    app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024

    return app