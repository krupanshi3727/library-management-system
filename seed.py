"""
Seed script for Library Management System.
Populates the database with sample data:
  - 1 admin user
  - 5 student users with profiles
  - 20 books across 4+ categories
  - 5 sample transactions (issued, returned, overdue)
"""

import os
import sys
from datetime import date, timedelta, datetime

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Student, Book, Transaction, Notification
import bcrypt


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def seed():
    app = create_app()
    with app.app_context():
        # Drop and recreate all tables
        db.drop_all()
        db.create_all()
        print('[OK] Database tables created.')

        # ── Admin User ──
        admin = User(
            name='Library Admin',
            email='admin@library.com',
            password_hash=hash_password('admin123'),
            role='admin'
        )
        db.session.add(admin)
        print('[OK] Admin user created (admin@library.com / admin123)')

        # ── Students ──
        students_data = [
            {'name': 'Aarav Sharma', 'email': 'aarav@college.edu', 'password': 'student123',
             'student_id': 'CS2024001', 'department': 'Computer Science', 'year': 2, 'phone': '9876543210'},
            {'name': 'Priya Patel', 'email': 'priya@college.edu', 'password': 'student123',
             'student_id': 'EE2024002', 'department': 'Electrical Engineering', 'year': 3, 'phone': '9876543211'},
            {'name': 'Rahul Kumar', 'email': 'rahul@college.edu', 'password': 'student123',
             'student_id': 'ME2024003', 'department': 'Mechanical Engineering', 'year': 1, 'phone': '9876543212'},
            {'name': 'Sneha Gupta', 'email': 'sneha@college.edu', 'password': 'student123',
             'student_id': 'MA2024004', 'department': 'Mathematics', 'year': 4, 'phone': '9876543213'},
            {'name': 'Vikram Singh', 'email': 'vikram@college.edu', 'password': 'student123',
             'student_id': 'PH2024005', 'department': 'Physics', 'year': 2, 'phone': '9876543214'},
        ]

        student_objects = []
        for s in students_data:
            user = User(
                name=s['name'], email=s['email'],
                password_hash=hash_password(s['password']),
                role='student'
            )
            db.session.add(user)
            db.session.flush()
            student = Student(
                user_id=user.id, student_id=s['student_id'],
                department=s['department'], year=s['year'], phone=s['phone']
            )
            db.session.add(student)
            db.session.flush()
            student_objects.append(student)

        print(f'[OK] {len(students_data)} students created.')

        # ── Books ──
        books_data = [
            # Science (5)
            {'title': 'A Brief History of Time', 'author': 'Stephen Hawking', 'isbn': '978-0553380163',
             'category': 'Science', 'total_copies': 3, 'publisher': 'Bantam', 'year': 1988,
             'description': 'A landmark volume in science writing by one of the great minds of our time.'},
            {'title': 'The Selfish Gene', 'author': 'Richard Dawkins', 'isbn': '978-0198788607',
             'category': 'Science', 'total_copies': 2, 'publisher': 'Oxford University Press', 'year': 1976,
             'description': 'The classic study of how organisms evolve through genes.'},
            {'title': 'Cosmos', 'author': 'Carl Sagan', 'isbn': '978-0345539434',
             'category': 'Science', 'total_copies': 4, 'publisher': 'Ballantine Books', 'year': 1980,
             'description': 'A comprehensive exploration of the universe.'},
            {'title': 'The Origin of Species', 'author': 'Charles Darwin', 'isbn': '978-0451529060',
             'category': 'Science', 'total_copies': 2, 'publisher': 'Signet Classics', 'year': 1859,
             'description': 'Darwin\'s groundbreaking work on evolution.'},
            {'title': 'Sapiens: A Brief History of Humankind', 'author': 'Yuval Noah Harari', 'isbn': '978-0062316097',
             'category': 'Science', 'total_copies': 5, 'publisher': 'Harper', 'year': 2015,
             'description': 'A narrative of humanity from the Stone Age to the Silicon Age.'},

            # Literature (5)
            {'title': 'To Kill a Mockingbird', 'author': 'Harper Lee', 'isbn': '978-0061120084',
             'category': 'Literature', 'total_copies': 4, 'publisher': 'Harper Perennial', 'year': 1960,
             'description': 'A Pulitzer Prize-winning novel about racial injustice in the American South.'},
            {'title': '1984', 'author': 'George Orwell', 'isbn': '978-0451524935',
             'category': 'Literature', 'total_copies': 3, 'publisher': 'Signet Classics', 'year': 1949,
             'description': 'A dystopian social science fiction novel and cautionary tale.'},
            {'title': 'Pride and Prejudice', 'author': 'Jane Austen', 'isbn': '978-0141439518',
             'category': 'Literature', 'total_copies': 2, 'publisher': 'Penguin Classics', 'year': 1813,
             'description': 'A timeless story of love, class, and social manners in Regency-era England.'},
            {'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald', 'isbn': '978-0743273565',
             'category': 'Literature', 'total_copies': 3, 'publisher': 'Scribner', 'year': 1925,
             'description': 'A commentary on the American Dream set in the Jazz Age.'},
            {'title': 'Hamlet', 'author': 'William Shakespeare', 'isbn': '978-0743477123',
             'category': 'Literature', 'total_copies': 2, 'publisher': 'Simon & Schuster', 'year': 1603,
             'description': 'Shakespeare\'s famous tragedy of the Prince of Denmark.'},

            # Engineering (5)
            {'title': 'Introduction to Algorithms', 'author': 'Thomas H. Cormen', 'isbn': '978-0262033848',
             'category': 'Engineering', 'total_copies': 5, 'publisher': 'MIT Press', 'year': 2009,
             'description': 'A comprehensive textbook on the modern study of algorithms.'},
            {'title': 'Clean Code', 'author': 'Robert C. Martin', 'isbn': '978-0132350884',
             'category': 'Engineering', 'total_copies': 3, 'publisher': 'Prentice Hall', 'year': 2008,
             'description': 'A handbook of agile software craftsmanship.'},
            {'title': 'Design Patterns', 'author': 'Erich Gamma et al.', 'isbn': '978-0201633610',
             'category': 'Engineering', 'total_copies': 2, 'publisher': 'Addison-Wesley', 'year': 1994,
             'description': 'Elements of reusable object-oriented software design.'},
            {'title': 'The Pragmatic Programmer', 'author': 'David Thomas & Andrew Hunt', 'isbn': '978-0135957059',
             'category': 'Engineering', 'total_copies': 4, 'publisher': 'Addison-Wesley', 'year': 2019,
             'description': 'Your journey to mastery in software development.'},
            {'title': 'Computer Networks', 'author': 'Andrew S. Tanenbaum', 'isbn': '978-0132126953',
             'category': 'Engineering', 'total_copies': 3, 'publisher': 'Pearson', 'year': 2010,
             'description': 'A comprehensive guide to computer networking.'},

            # Mathematics (5)
            {'title': 'Calculus', 'author': 'James Stewart', 'isbn': '978-1285740621',
             'category': 'Mathematics', 'total_copies': 6, 'publisher': 'Cengage Learning', 'year': 2015,
             'description': 'A popular textbook for introductory calculus courses.'},
            {'title': 'Linear Algebra Done Right', 'author': 'Sheldon Axler', 'isbn': '978-3319110806',
             'category': 'Mathematics', 'total_copies': 3, 'publisher': 'Springer', 'year': 2015,
             'description': 'A unique approach to linear algebra focusing on proofs and concepts.'},
            {'title': 'Discrete Mathematics', 'author': 'Kenneth H. Rosen', 'isbn': '978-0073383095',
             'category': 'Mathematics', 'total_copies': 4, 'publisher': 'McGraw-Hill', 'year': 2011,
             'description': 'A comprehensive textbook on discrete mathematical structures.'},
            {'title': 'Probability and Statistics', 'author': 'Morris H. DeGroot', 'isbn': '978-0321500465',
             'category': 'Mathematics', 'total_copies': 3, 'publisher': 'Pearson', 'year': 2012,
             'description': 'A rigorous treatment of probability and statistical theory.'},
            {'title': 'Topology', 'author': 'James Munkres', 'isbn': '978-0131816299',
             'category': 'Mathematics', 'total_copies': 2, 'publisher': 'Pearson', 'year': 2000,
             'description': 'An introduction to the fundamental concepts of topology.'},
        ]

        book_objects = []
        for b in books_data:
            book = Book(
                title=b['title'], author=b['author'], isbn=b['isbn'],
                category=b['category'], total_copies=b['total_copies'],
                available_copies=b['total_copies'],
                publisher=b.get('publisher', ''), year=b.get('year'),
                description=b.get('description', '')
            )
            db.session.add(book)
            db.session.flush()
            book_objects.append(book)

        print(f'[OK] {len(books_data)} books created.')

        # ── Transactions ──
        today = date.today()

        # 1. Issued (active, not overdue) – Aarav borrowed "Introduction to Algorithms"
        txn1 = Transaction(
            student_id=student_objects[0].id,
            book_id=book_objects[10].id,  # Intro to Algorithms
            issue_date=today - timedelta(days=5),
            due_date=today + timedelta(days=9),
            status='issued'
        )
        book_objects[10].available_copies -= 1

        # 2. Returned – Priya returned "1984"
        txn2 = Transaction(
            student_id=student_objects[1].id,
            book_id=book_objects[6].id,  # 1984
            issue_date=today - timedelta(days=20),
            due_date=today - timedelta(days=6),
            return_date=today - timedelta(days=7),
            fine_amount=0.0,
            status='returned'
        )

        # 3. Overdue – Rahul has "Clean Code" overdue
        txn3 = Transaction(
            student_id=student_objects[2].id,
            book_id=book_objects[11].id,  # Clean Code
            issue_date=today - timedelta(days=21),
            due_date=today - timedelta(days=7),
            status='overdue'
        )
        book_objects[11].available_copies -= 1

        # 4. Issued – Sneha borrowed "Calculus"
        txn4 = Transaction(
            student_id=student_objects[3].id,
            book_id=book_objects[15].id,  # Calculus
            issue_date=today - timedelta(days=3),
            due_date=today + timedelta(days=11),
            status='issued'
        )
        book_objects[15].available_copies -= 1

        # 5. Returned with fine – Vikram returned "Cosmos" late
        txn5 = Transaction(
            student_id=student_objects[4].id,
            book_id=book_objects[2].id,  # Cosmos
            issue_date=today - timedelta(days=25),
            due_date=today - timedelta(days=11),
            return_date=today - timedelta(days=5),
            fine_amount=12.0,  # 6 days late × ₹2
            status='returned'
        )

        db.session.add_all([txn1, txn2, txn3, txn4, txn5])
        db.session.flush()

        # ── Notifications ──
        notifs = [
            Notification(user_id=student_objects[0].user_id,
                         message=f"Book 'Introduction to Algorithms' issued to you. Due by {txn1.due_date.strftime('%d %b %Y')}."),
            Notification(user_id=student_objects[2].user_id,
                         message=f"OVERDUE: Book 'Clean Code' was due on {txn3.due_date.strftime('%d %b %Y')}. Fine: Rs.{txn3.calculated_fine:.0f}"),
            Notification(user_id=student_objects[3].user_id,
                         message=f"Book 'Calculus' issued to you. Due by {txn4.due_date.strftime('%d %b %Y')}."),
            Notification(user_id=student_objects[4].user_id,
                         message=f"Book 'Cosmos' returned with a fine of Rs.12 (6 days overdue)."),
            Notification(user_id=student_objects[1].user_id,
                         message=f"Book '1984' returned successfully. No fine."),
        ]
        db.session.add_all(notifs)

        db.session.commit()
        print('[OK] 5 transactions created (2 issued, 2 returned, 1 overdue).')
        print('[OK] Notifications created.')
        print('\n==========================================')
        print('  Database seeded successfully!')
        print('  Admin login: admin@library.com / admin123')
        print('  Students:    <name>@college.edu / student123')
        print('  Run: python run.py')
        print('==========================================')


if __name__ == '__main__':
    seed()
