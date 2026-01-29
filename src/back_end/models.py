from datetime import datetime 
from sqlmodel import Field , SQLModel , Relationship  
from typing import Optional, List

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_name: str = Field(index=True, unique=True)
    hashed_password: str
    auth: str = Field(default='member')
    # Cầu nối quản lý Task (Admin tạo)
    created_tasks: List["Task"] = Relationship(
        back_populates="admin_user",
        sa_relationship_kwargs={"foreign_keys": "Task.admin_id"} 
    )
    # Cầu nối nhận Task (Member làm)
    tasks_to_do: List["Task"] = Relationship(
        back_populates="assigned_member",
        sa_relationship_kwargs={"foreign_keys": "Task.member_id"}
    )
    # QUAN TRỌNG: Thêm cầu nối tới đơn ứng tuyển
    applies: List["TaskApply"] = Relationship(back_populates="member_user")

class Task(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(default="")
    status: str = Field(default="available") 
    deadline: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    admin_id: int = Field(foreign_key="user.id") 
    admin_user: "User" = Relationship(
        back_populates="created_tasks",
        sa_relationship_kwargs={"foreign_keys": "Task.admin_id"}
    )

    member_id: Optional[int] = Field(default=None, foreign_key="user.id") 
    assigned_member: Optional["User"] = Relationship(
        back_populates="tasks_to_do",
        sa_relationship_kwargs={"foreign_keys": "Task.member_id"}
    )
    # QUAN TRỌNG: Thêm cầu nối để Admin xem ai ứng tuyển Task này
    applies: List["TaskApply"] = Relationship(back_populates="target_task")

class TaskApply(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)

    status: str = Field(default='pending')
    applied_at: datetime = Field(default_factory=datetime.now)

    user_id: int = Field(foreign_key='user.id')
    task_id: int = Field(foreign_key='task.id')
    
    member_user: "User" = Relationship(back_populates="applies")
    target_task: "Task" = Relationship(back_populates="applies")

