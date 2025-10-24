from pydantic import BaseModel, EmailStr


class UserPublicSchema(BaseModel):
    id: int
    name: str
    email: EmailStr


class UserRegisterSchema(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    expires_in: int
    token_type: str = 'bearer'


class UserInfoSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
