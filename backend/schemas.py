from datetime import date, datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserBase(BaseModel):
    """Fields shared by every user schema."""

    model_config = ConfigDict(str_strip_whitespace=True)

    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(default=None, pattern=r"^\+?\d{10,15}$")
    gender: Optional[Literal["Male", "Female", "Other"]] = None
    date_of_birth: Optional[date] = None
    department: Optional[str] = Field(default=None, max_length=100)
    designation: Optional[str] = Field(default=None, max_length=100)
    status: Literal["Active", "Inactive"] = "Active"

    @field_validator(
        "phone", "gender", "date_of_birth", "department", "designation",
        mode="before",
    )
    @classmethod
    def empty_string_to_none(cls, value):
        """An empty form box arrives as "", so store it as NULL instead."""
        if isinstance(value, str) and value.strip() == "":
            return None
        return value

    @field_validator("date_of_birth")
    @classmethod
    def dob_not_in_future(cls, value):
        if value is not None and value > date.today():
            raise ValueError("Date of birth cannot be in the future")
        return value


class UserCreate(UserBase):
    """Data accepted by POST /api/users."""


class UserUpdate(UserBase):
    """Data accepted by PUT /api/users/{user_id}."""


class UserResponse(UserBase):
    """Data we send back: the user's fields plus what MySQL generated."""

    user_id: int
    created_at: datetime
    updated_at: datetime