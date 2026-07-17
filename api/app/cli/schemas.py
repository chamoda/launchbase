from pydantic import EmailStr, Field

from app.schemas import Model


class UserCreate(Model):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
