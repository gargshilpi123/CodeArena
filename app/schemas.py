from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):

    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):

    email: EmailStr
    password: str


class Token(BaseModel):

    access_token: str
    token_type: str


class ProblemCreate(BaseModel):

    title: str
    description: str
    difficulty: str
    topic: str
    constraints: Optional[str] = None


class ProblemResponse(BaseModel):

    id: int
    title: str
    description: str
    difficulty: str
    topic: str
    constraints: Optional[str]

    class Config:
        from_attributes = True


class TestCaseCreate(BaseModel):

    input: str
    expected_output: str


class SubmissionCreate(BaseModel):

    problem_id: int
    language: str
    code: str