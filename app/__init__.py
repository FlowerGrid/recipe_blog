"""
App Package
"""
from dotenv import load_dotenv
from flask import Flask
from flask_ckeditor import CKEditor
import os

load_dotenv()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

ckeditor = CKEditor()

def create_app():
    app = Flask(
        __name__,
        static_folder=os.path.join(BASE_DIR, 'static'),
        static_url_path='/static'
        )


    ckeditor.init_app(app)

    from .admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from .main import main_bp
    app.register_blueprint(main_bp, url_prefix='/')

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['CKEDITOR_PKG_TYPE'] = 'basic'
    app.config['CKEDITOR_ENABLE_CODESNIPPET'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, '..', 'static', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024

    print("Registered blueprints:", app.blueprints)

    return app