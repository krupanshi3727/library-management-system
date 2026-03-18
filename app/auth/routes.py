from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
import bcrypt

from app.models import User
from app.auth.forms import LoginForm

auth_bp = Blueprint('auth', __name__, template_folder='../templates/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('student.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.checkpw(form.password.data.encode('utf-8'),
                                   user.password_hash.encode('utf-8')):
            login_user(user)
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            if user.role == 'admin':
                return redirect(next_page or url_for('admin.dashboard'))
            return redirect(next_page or url_for('student.dashboard'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
