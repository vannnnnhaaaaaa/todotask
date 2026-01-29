from sqlmodel import SQLModel , Field 
from typing import Optional
from datetime import datetime

# -- --- SCHEMA FOR USER --- -- #
class UserCreate  (SQLModel ) :
    user_name : str = Field(index=True , unique=True)
    password : str = Field(min_length=1, max_length=72)

class UserRead(SQLModel):
    id: int
    user_name: str
    auth: str

# -- --- SCHEMA FOR TASK --- -- #
class TaskCreate (SQLModel) :
    title : str 
    description : str
    deadline : datetime

class TaskRead (SQLModel) :
    id : int 
    title : str
    description : str
    status : str 
    deadline : datetime 
    started_at : Optional[datetime]
    completed_at : Optional[datetime]
    delay_info : Optional[str] = None

# -- --- SCHEMA FOR APPLY --- -- #
class TaskApplyRead(SQLModel) :
    id : int
    user_id : int
    task_id : int
    status : str
    applied_at : datetime

class TaskApplyWithUser (SQLModel) :
    id: int
    task_id: int
    user_id: int
    status: str
    applied_at: datetime
    username: str
    
class TaskReadWithStatus(SQLModel):
    id: int
    title: str
    description: str | None = None
    deadline: datetime
    status: str
    is_applied: bool 