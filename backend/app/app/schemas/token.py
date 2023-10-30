from typing import Optional
from pydantic import BaseModel
from typing_extensions import Annotated
from fastapi.param_functions import Form
from typing import Any, Dict, List, Optional, Union, cast


class Token(BaseModel):
    access_token: str
    token_type: str
    user_name: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    organization: Optional[str] = None


class UserLogin(BaseModel):
    grant_type: Union[str, None] = None
    username: str
    password: str
    scope: str = ""
    client_id: Union[str, None] = None
    client_secret: Union[str, None] = None


class TokenPayload(BaseModel):
    sub: Optional[int] = None
