# 📚 College Library Management System

A production-ready **Library Management System** for colleges, built with Flask, SQLAlchemy, and Bootstrap 5. Features separate portals for **Admin (Librarian)** and **Students** with full CRUD operations, authentication, book issue/return tracking, fine calculation, and notifications.

---

## ✨ Features

### Admin Portal
- **Dashboard** with stats: Total Books, Issued, Overdue, Students
- **Book Management**: Add, Edit, Delete (soft), Search & Filter by category
- **Student Management**: Register, View profiles, Edit, Borrowing history
- **Issue & Return**: Issue books to students, Auto-calculate fines (₹2/day)
- **Transaction Tracking**: Filter by status (Issued/Returned/Overdue)

### Student Portal
- **Dashboard**: Currently borrowed books, pending fines, due-soon warnings
- **Browse Books**: Search/filter library catalog with availability indicators
- **Borrowing History**: Complete record of all transactions
- **Notifications**: Alerts for issued books, due dates, overdue fines

### Security
- Password hashing with **bcrypt**
- Session management with **Flask-Login**
- Role-based access control (admin_required / student_required decorators)
- CSRF protection with **Flask-WTF**

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Seed the database
```bash
python seed.py
```

### 3. Run the application
```bash
python run.py
```

Open **http://localhost:5000** in your browser.

---

## 🔐 Default Credentials

| Role    | Email               | Password    |
|---------|---------------------|-------------|
| Admin   | admin@library.com   | admin123    |
| Student | aarav@college.edu   | student123  |
| Student | priya@college.edu   | student123  |
| Student | rahul@college.edu   | student123  |
| Student | sneha@college.edu   | student123  |
| Student | vikram@college.edu  | student123  |

---

## 🏗️ Tech Stack

- **Backend**: Python 3, Flask
- **Database**: SQLite (SQLAlchemy ORM)
- **Frontend**: Jinja2, Bootstrap 5, Vanilla JS
- **Auth**: Flask-Login + bcrypt
- **Forms**: Flask-WTF / WTForms

---

## 📁 Project Structure

```
library_management/
├── app/
│   ├── __init__.py          # App factory
│   ├── models.py            # Database models
│   ├── auth/                # Auth blueprint (login/logout)
│   ├── admin/               # Admin blueprint (CRUD, issue/return)
│   ├── student/             # Student blueprint (browse, history)
│   ├── templates/           # Jinja2 HTML templates
│   └── static/              # CSS & JS
├── config.py                # Configuration
├── run.py                   # Entry point
├── seed.py                  # Database seeder
└── requirements.txt         # Dependencies
```

---

## 📋 Business Rules

- **Due Date**: 14 days from issue date
- **Fine**: ₹2 per day past due date
- **Max Issues**: 3 active issues per student
- **Soft Delete**: Books are deactivated, not permanently removed
