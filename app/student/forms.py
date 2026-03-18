from flask_wtf import FlaskForm
from wtforms import SubmitField


class EmptyForm(FlaskForm):
    """Empty form used for CSRF protection on simple actions."""
    submit = SubmitField()
