"""
App Package
"""
from .blueprints.main import main_bp
from .blueprints.admin import admin_bp
from .db import init_db
from dotenv import load_dotenv
from flask import Flask, current_app, url_for, render_template
from flask_ckeditor import CKEditor
import os
from werkzeug.exceptions import HTTPException

import traceback; traceback.print_stack()

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

    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(main_bp, url_prefix='/')

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['CKEDITOR_PKG_TYPE'] = 'basic'
    app.config['CKEDITOR_ENABLE_CODESNIPPET'] = False
    app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024

    # Database
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['CREATE_TABLES'] = False   # Set to True for local development

    init_db(app)

    from .cli import init_cli


    @app.errorhandler(HTTPException)
    def error_page(error):
        return render_template('main/error-page.html', error=error), error.code


    @app.context_processor
    def inject_logo_url():
        user_logo_path = os.path.join(BASE_DIR, 'static', 'uploads', 'users', 'user-logo.png')

        if os.path.exists(user_logo_path):
            return {
                'logo_url': url_for('static', filename='uploads/users/user-logo.png')
            }
        else:
            return {
                'logo_url': url_for('static', filename='images/default-logo.png')
            }
        

    init_cli(app)


    return app



