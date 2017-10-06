# app/__init__.py

# third-party imports
from flask import Flask, render_template, abort

from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

# local imports
from config import app_config

# db variable initialization
db = SQLAlchemy()
# Flask database migration management

# Flask Login Manager initialization
login_manager = LoginManager()



def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    # initialize the flask objects
    Bootstrap(app)
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"

    migrate = Migrate(app, db)

    from notesApp import models

    # Register the Blueprints
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint)


    # Custom Error Handling
    # existing code remains

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html', title='Forbidden'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        logError(True)
        return render_template('errors/404.html', title='Page Not Found'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        logError(True)
        return render_template('errors/500.html', title='Server Error'), 500

    @app.route('/500')
    def error():
        logError(True)
        abort(500)

    def logError(start):
        #   Explicitely Prints error to the errorlog. @/var/log/apache2/error.log
        assert start
        import traceback, sys, StringIO
        err = sys.stderr
        buffer = sys.stderr = StringIO.StringIO()
        traceback.print_exc()
        sys.stderr = err
        print buffer.getvalue()


    return app

