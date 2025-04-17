from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = {
        "from_attributes": True  # For Pydantic v2
    }


class Token(BaseModel):
    access_token: str
    token_type: str



class UserLogin(BaseModel):
    username: str
    password: str