from pydantic import BaseModel


class StudentNoID(BaseModel):
    name: str
    surname: str
    classes: str
    points: int


class Student(StudentNoID):
    id: int

    class Config:
        orm_mode = True
