from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class EventCreate(BaseModel):
    title: str
    description: str
    slots: int


class EventUpdate(BaseModel):
    title: str
    description: str
    slots: int

class AnnouncementCreate(BaseModel) :
    message : str