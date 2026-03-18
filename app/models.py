from datetime import datetime, date
from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(10), nullable=False, default='student')  # admin / student
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    student_profile = db.relationship('Student', backref='user', uselist=False, lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True,
                                    order_by='Notification.created_at.desc()')

    def __repr__(self):
        return f'<User {self.name} ({self.role})>'


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)  # college roll number
    department = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String(15), nullable=False)

    transactions = db.relationship('Transaction', backref='student', lazy=True,
                                   order_by='Transaction.issue_date.desc()')

    def __repr__(self):
        return f'<Student {self.student_id}>'


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    total_copies = db.Column(db.Integer, nullable=False, default=1)
    available_copies = db.Column(db.Integer, nullable=False, default=1)
    publisher = db.Column(db.String(100), default='')
    year = db.Column(db.Integer)
    description = db.Column(db.Text, default='')
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)  # for soft delete

    transactions = db.relationship('Transaction', backref='book', lazy=True)

    @property
    def is_available(self):
        return self.available_copies > 0

    def __repr__(self):
        return f'<Book {self.title}>'


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    issue_date = db.Column(db.Date, nullable=False, default=date.today)
    due_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=True)
    fine_amount = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(10), nullable=False, default='issued')  # issued / returned / overdue

    @property
    def is_overdue(self):
        if self.status == 'returned':
            return False
        return date.today() > self.due_date

    @property
    def calculated_fine(self):
        if self.status == 'returned' and self.return_date and self.return_date > self.due_date:
            days = (self.return_date - self.due_date).days
            return days * 2.0
        if self.status != 'returned' and date.today() > self.due_date:
            days = (date.today() - self.due_date).days
            return days * 2.0
        return 0.0

    def __repr__(self):
        return f'<Transaction {self.id} - {self.status}>'


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Notification {self.id}>'
