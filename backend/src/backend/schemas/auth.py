from pydantic import BaseModel, EmailStr


class UserPublicSchema(BaseModel):
    id: int
    name: str
    email: EmailStr


class UserRegisterSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
