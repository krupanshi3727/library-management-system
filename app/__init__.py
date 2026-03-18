from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
csrf = CSRFProtect()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    from app.auth.routes import auth_bp
    from app.admin.routes import admin_bp
    from app.student.routes import student_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(student_bp, url_prefix='/student')

    # Root route redirects to login
    @app.route('/')
    def index():
        from flask import redirect, url_for
        return redirect(url_for('auth.login'))

    with app.app_context():
        db.create_all()

    return app
