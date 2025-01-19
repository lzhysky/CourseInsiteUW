# -*- coding: utf-8 -*-
"""User forms."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from .models import User


class RegisterForm(FlaskForm):
    """Register form."""

    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=25)]
    )
    email = StringField(
        "Email", validators=[DataRequired(), Email(), Length(min=6, max=40)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        "Verify password",
        [DataRequired(), EqualTo("password", message="Passwords must match")],
    )

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, **kwargs):
        """Validate the form."""
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append("Username already registered")
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        return True

class FeedbackForm(FlaskForm):
    """Register form."""

    course_name = StringField(
        "course_name"
    )
    feedback = StringField(
        "feedback"
    )
    username = PasswordField(
        "username"
    )

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, **kwargs):
        """Validate the form."""
        return True


class RegisterFormUW(FlaskForm):
    """Register form."""

    username = StringField(
        "username"
    )

    firstName = StringField(
        "FirstName", validators=[DataRequired(), Length(min=3, max=25)]
    )
    lastName = StringField(
        "LastName", validators=[DataRequired(), Length(min=3, max=25)]
    )
    email = StringField(
        "Email", validators=[DataRequired(), Email(), Length(min=6, max=40)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        "Verify password",
        [DataRequired(), EqualTo("password", message="Passwords must match")],
    )

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(RegisterFormUW, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, **kwargs):
        """Validate the form."""
        initial_validation = super(RegisterFormUW, self).validate()
        if not initial_validation:
            return False
        # user = User.query.filter_by(username=self.username.data).first()
        # if user:
        #     self.username.errors.append("Username already registered")
        #     return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        return True