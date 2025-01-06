from pydantic import BaseModel
from typing import Union

class Human(BaseModel):
    name: str
    family: str
    age: int
    email: str
    password: str
    gender: Union[bool,None] = False