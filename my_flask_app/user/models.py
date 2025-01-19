# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property

from my_flask_app.database import Column, PkModel, db, reference_col, relationship
from my_flask_app.extensions import bcrypt


class Role(PkModel):
    """A role for a user."""

    __tablename__ = "roles"
    name = Column(db.String(80), unique=True, nullable=False)
    user_id = reference_col("users", nullable=True)
    user = relationship("User", backref="roles")

    def __init__(self, name, **kwargs):
        """Create instance."""
        super().__init__(name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Role({self.name})>"


class User(UserMixin, PkModel):
    """A user of the app."""

    __tablename__ = "users"
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    _password = Column("password", db.LargeBinary(128), nullable=True)
    created_at = Column(
        db.DateTime, nullable=False, default=dt.datetime.now(dt.timezone.utc)
    )
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)

    @hybrid_property
    def password(self):
        """Hashed password."""
        return self._password

    @password.setter
    def password(self, value):
        """Set password."""
        self._password = bcrypt.generate_password_hash(value)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self._password, value)

    @property
    def full_name(self):
        """Full user name."""
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<User({self.username!r})>"

    def to_dict(self):
        """Convert User object to dictionary."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "active": self.active,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class Course(PkModel):
    """A course offered in the system."""

    __tablename__ = "course"

    id = Column(db.Integer, primary_key=True, autoincrement=True)
    course_name = Column(db.String(255), nullable=False)
    course_description = Column(db.String(25500), nullable=True)
    course_code = Column(db.String(255), unique=True, nullable=False)
    course_link = Column(db.String(2550), nullable=True)
    semester = Column(db.String(255), nullable=False)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Course({self.id!r}, {self.course_name!r})>"

    def to_dict(self):
        """Convert Course object to dictionary."""
        return {
            "id": self.id,
            "course_name": self.course_name,
            "course_description": self.course_description,
            "course_code": self.course_code,
            "course_link": self.course_link,
            "semester": self.semester
        }

class Feedback(PkModel):
    """A course offered in the system."""

    __tablename__ = "feedback"

    id = Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = Column(db.Integer, nullable=False)
    feedback = Column(db.String(25500), nullable=True)
    user_id = Column(db.Integer, unique=True, nullable=False)
    course_name = Column(db.String(255))
    username = Column(db.String(255))
    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Course({self.id!r}, {self.course_name!r})>"

    def to_dict(self):
        """Convert Course object to dictionary."""
        return {
            "id": self.id,
            "course_id": self.course_id,
            "feedback": self.feedback,
            "user_id": self.user_id,
            "course_name": self.course_name,
            "username": self.username
        }

