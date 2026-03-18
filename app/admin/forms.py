from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional


class AddBookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    author = StringField('Author', validators=[DataRequired(), Length(max=100)])
    isbn = StringField('ISBN', validators=[DataRequired(), Length(max=20)])
    category = SelectField('Category', choices=[
        ('Science', 'Science'),
        ('Literature', 'Literature'),
        ('Engineering', 'Engineering'),
        ('Mathematics', 'Mathematics'),
        ('Computer Science', 'Computer Science'),
        ('History', 'History'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    total_copies = IntegerField('Total Copies', validators=[DataRequired(), NumberRange(min=1)])
    publisher = StringField('Publisher', validators=[Optional(), Length(max=100)])
    year = IntegerField('Publication Year', validators=[Optional(), NumberRange(min=1800, max=2030)])
    description = TextAreaField('Description', validators=[Optional()])
    submit = SubmitField('Save Book')


class EditBookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    author = StringField('Author', validators=[DataRequired(), Length(max=100)])
    isbn = StringField('ISBN', validators=[DataRequired(), Length(max=20)])
    category = SelectField('Category', choices=[
        ('Science', 'Science'),
        ('Literature', 'Literature'),
        ('Engineering', 'Engineering'),
        ('Mathematics', 'Mathematics'),
        ('Computer Science', 'Computer Science'),
        ('History', 'History'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    total_copies = IntegerField('Total Copies', validators=[DataRequired(), NumberRange(min=1)])
    publisher = StringField('Publisher', validators=[Optional(), Length(max=100)])
    year = IntegerField('Publication Year', validators=[Optional(), NumberRange(min=1800, max=2030)])
    description = TextAreaField('Description', validators=[Optional()])
    submit = SubmitField('Update Book')


class AddStudentForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    student_id = StringField('Roll Number', validators=[DataRequired(), Length(max=20)])
    department = SelectField('Department', choices=[
        ('Computer Science', 'Computer Science'),
        ('Electrical Engineering', 'Electrical Engineering'),
        ('Mechanical Engineering', 'Mechanical Engineering'),
        ('Civil Engineering', 'Civil Engineering'),
        ('Mathematics', 'Mathematics'),
        ('Physics', 'Physics'),
        ('Chemistry', 'Chemistry'),
        ('Literature', 'Literature'),
    ], validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired(), NumberRange(min=1, max=6)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(max=15)])
    submit = SubmitField('Register Student')


class EditStudentForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    student_id = StringField('Roll Number', validators=[DataRequired(), Length(max=20)])
    department = SelectField('Department', choices=[
        ('Computer Science', 'Computer Science'),
        ('Electrical Engineering', 'Electrical Engineering'),
        ('Mechanical Engineering', 'Mechanical Engineering'),
        ('Civil Engineering', 'Civil Engineering'),
        ('Mathematics', 'Mathematics'),
        ('Physics', 'Physics'),
        ('Chemistry', 'Chemistry'),
        ('Literature', 'Literature'),
    ], validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired(), NumberRange(min=1, max=6)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(max=15)])
    submit = SubmitField('Update Student')


class IssueBookForm(FlaskForm):
    student_roll = StringField('Student Roll Number', validators=[DataRequired()])
    book_isbn = StringField('Book ISBN or Title', validators=[DataRequired()])
    submit = SubmitField('Issue Book')
