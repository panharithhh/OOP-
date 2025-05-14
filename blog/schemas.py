from pydantic import BaseModel
from . import schemas

class Blog(BaseModel):
    title: str
    body : str