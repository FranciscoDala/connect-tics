from pydantic import BaseModel, Field, field_validator
import re

USERNAME_REGEX = re.compile(r"^[a-zA-Z0-9_.-]{3,50}$")

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not USERNAME_REGEX.match(v):
            raise ValueError('Use apenas a-z, 0-9,. _ -')
        return v.lower().strip()

class UserUpdate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str | None = Field(None, min_length=6)

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not USERNAME_REGEX.match(v):
            raise ValueError('Use apenas a-z, 0-9,. _ -')
        return v.lower().strip()

class UserOut(BaseModel):
    id: int
    username: str
    model_config = {"from_attributes": True}