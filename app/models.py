from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship

from datetime import datetime

from .database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String(50),
        unique=True,
        nullable=False
    )

    email = Column(
        String(100),
        unique=True,
        nullable=False
    )

    password = Column(
        String(255),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    submissions = relationship(
        "Submission",
        back_populates="user"
    )


class Problem(Base):

    __tablename__ = "problems"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String(200),
        nullable=False
    )

    description = Column(
        Text,
        nullable=False
    )

    difficulty = Column(
        String(20),
        nullable=False
    )

    topic = Column(
        String(100),
        nullable=False
    )

    constraints = Column(
        Text
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    test_cases = relationship(
        "TestCase",
        back_populates="problem",
        cascade="all, delete-orphan"
    )

    submissions = relationship(
        "Submission",
        back_populates="problem"
    )


class TestCase(Base):

    __tablename__ = "test_cases"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    problem_id = Column(
        Integer,
        ForeignKey("problems.id"),
        nullable=False
    )

    input = Column(
        Text,
        nullable=False
    )

    expected_output = Column(
        Text,
        nullable=False
    )

    problem = relationship(
        "Problem",
        back_populates="test_cases"
    )


class Submission(Base):

    __tablename__ = "submissions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    problem_id = Column(
        Integer,
        ForeignKey("problems.id"),
        nullable=False
    )

    code = Column(
        Text,
        nullable=False
    )

    language = Column(
        String(20),
        nullable=False
    )

    status = Column(
        String(50),
        nullable=False
    )

    passed = Column(
        Integer,
        default=0
    )

    total = Column(
        Integer,
        default=0
    )

    runtime = Column(
        String(50)
    )

    submitted_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    user = relationship(
        "User",
        back_populates="submissions"
    )

    review = relationship(
        "CodeReview",
        back_populates="submission",
        uselist=False,
        cascade="all, delete-orphan"
    )


class CodeReview(Base):

    __tablename__ = "code_reviews"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    submission_id = Column(
        Integer,
        ForeignKey("submissions.id"),
        nullable=False,
        unique=True
    )

    correctness = Column(
        Text,
        nullable=False
    )

    time_complexity = Column(
        String(100),
        nullable=False
    )

    space_complexity = Column(
        String(100),
        nullable=False
    )

    bugs = Column(
        Text,
        nullable=False
    )

    code_quality = Column(
        Text,
        nullable=False
    )

    edge_cases = Column(
        Text,
        nullable=False
    )

    suggestions = Column(
        Text,
        nullable=False
    )

    overall_feedback = Column(
        Text,
        nullable=False
    )

    submission = relationship(
        "Submission",
        back_populates="review"
    )