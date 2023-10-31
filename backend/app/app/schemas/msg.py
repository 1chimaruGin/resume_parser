from pydantic import BaseModel, EmailStr


class Msg(BaseModel):
    subject: str
    name: str
    email: EmailStr
    msg: str
