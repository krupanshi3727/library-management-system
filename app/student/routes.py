from functools import wraps
from datetime import date, timedelta

from flask import Blueprint, render_template, request, abort
from flask_login import login_required, current_user

from app import db
from app.models import Book, Transaction, Notification, Student

student_bp = Blueprint('student', __name__, template_folder='../templates/student')


def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'student':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


@student_bp.route('/dashboard')
@login_required
@student_required
def dashboard():
    student = current_user.student_profile
    if not student:
        abort(404)

    # Get active transactions
    active_txns = Transaction.query.filter(
        Transaction.student_id == student.id,
        Transaction.status.in_(['issued', 'overdue'])
    ).all()

    # Update overdue statuses
    for t in active_txns:
        if t.status == 'issued' and date.today() > t.due_date:
            t.status = 'overdue'
    db.session.commit()

    # Warning: due in 2 days
    due_soon = [t for t in active_txns
                if t.status == 'issued' and
                (t.due_date - date.today()).days <= 2 and
                (t.due_date - date.today()).days >= 0]

    total_fines = sum(t.calculated_fine for t in active_txns if t.is_overdue)

    unread_count = Notification.query.filter_by(
        user_id=current_user.id, is_read=False).count()

    return render_template('student_dashboard.html',
                           student=student,
                           active_txns=active_txns,
                           due_soon=due_soon,
                           total_fines=total_fines,
                           unread_count=unread_count)


@student_bp.route('/books')
@login_required
@student_required
def browse_books():
    search = request.args.get('search', '', type=str)
    category = request.args.get('category', '', type=str)
    page = request.args.get('page', 1, type=int)

    query = Book.query.filter_by(is_active=True)
    if search:
        query = query.filter(
            db.or_(
                Book.title.ilike(f'%{search}%'),
                Book.author.ilike(f'%{search}%'),
                Book.isbn.ilike(f'%{search}%')
            )
        )
    if category:
        query = query.filter_by(category=category)

    books = query.order_by(Book.title).paginate(page=page, per_page=12, error_out=False)
    categories = db.session.query(Book.category).filter_by(is_active=True).distinct().all()
    categories = [c[0] for c in categories]

    return render_template('student_books.html', books=books, search=search,
                           selected_category=category, categories=categories)


@student_bp.route('/history')
@login_required
@student_required
def history():
    student = current_user.student_profile
    txns = Transaction.query.filter_by(student_id=student.id)\
        .order_by(Transaction.issue_date.desc()).all()
    return render_template('student_history.html', transactions=txns, student=student)


@student_bp.route('/notifications')
@login_required
@student_required
def notifications():
    notifs = Notification.query.filter_by(user_id=current_user.id)\
        .order_by(Notification.created_at.desc()).all()

    # Mark all as read
    for n in notifs:
        n.is_read = True
    db.session.commit()

    return render_template('student_notifications.html', notifications=notifs)
