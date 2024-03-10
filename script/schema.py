import uuid
import re
from pydantic import BaseModel, ValidationError, Field, validator

def is_valid_email(email: str) -> bool:
    email_regex = r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(email_regex, email))

class AdminUser(BaseModel):
    name: str = Field(..., min_length=1)
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)
    email: str
    country: str = Field(..., min_length=1)
    p_key: int = Field(..., gt=0)  # Greater than 0

    @validator('email')
    def validate_email(cls, v):
        if not is_valid_email(v):
            raise ValueError("Email must be a valid email address")
        return v



class User(BaseModel):
    name: str = Field(..., min_length=1)
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)
    email: str
    user_field: str = Field(..., min_length=1)
    years: int = Field(..., gt=0)  # Greater than 0
    country: str = Field(..., min_length=1)

    @validator('email')
    def validate_email(cls, v):
        if not is_valid_email(v):
            raise ValueError("Email must be a valid email address")
        return v


class Book(BaseModel):
    book_name: str
    ISBN10: str
    author: str
    content: str
    field: str

class Paper(BaseModel):
    paper_name: str
    author: str
    content: str
    field: str


class Document(BaseModel):
    name: str
    content: str
    field: str