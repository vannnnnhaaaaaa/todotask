from datetime import datetime 

from sqlmodel import Field , SQLModel

from typing import Optional


class TaskRead (SQLModel) :
    title : str 
    is_completed : bool

class Task (SQLModel , table= True) :
    id : Optional[int]  = Field(primary_key=True , default=None)
    title : str = Field(min_length=1, max_length=100)
    is_completed : bool = Field (default=False)
    created_at : datetime = Field(default_factory=datetime.now )
