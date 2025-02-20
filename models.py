from pydantic import BaseModel
from sqlmodel import SQLModel, Field

class Employee(SQLModel, table=True):
    id: int = Field(default = None,primary_key = True)
    name: str
    age: int
    department: str
    salary: float

