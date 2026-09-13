import re

from pydantic import BaseModel, ConfigDict, field_validator

EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


class CustomerCreate(BaseModel):
    name: str
    phone: str
    email: str
    address: str

    @field_validator("name", "phone", "email", "address")
    @classmethod
    def required_trimmed_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Field must not be blank")
        return value

    @field_validator("email")
    @classmethod
    def valid_email(cls, value: str) -> str:
        if not EMAIL_PATTERN.match(value):
            raise ValueError("Email must be valid")
        return value


class CustomerRead(CustomerCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
