from pydantic import BaseModel

class AttendeeCreate(BaseModel):
    name: str
    email: str

class AttendeeRead(AttendeeCreate):
    id: int

    class Config:
        orm_mode = True
