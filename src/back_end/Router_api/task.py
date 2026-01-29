from fastapi import Depends ,APIRouter , HTTPException
from sqlmodel import Session ,select 
from models import Task , User ,TaskApply
from schema import   TaskCreate , TaskRead  ,TaskReadWithStatus
from auth import get_current_user
from connect_database import get_session

task_router = APIRouter()

@task_router.get("/tasks-with-status" , response_model=list[TaskReadWithStatus])
def get_tasks_with_status ( current_user: User= Depends(get_current_user)  ,session : Session = Depends(get_session)) :
    all_task = session.exec(select(Task)).all()
    applied_task = session.exec(select(TaskApply.task_id).where(TaskApply.user_id == current_user.id))
    applied_set = set(applied_task)
    results = []
    for t in all_task:
        task_data = t.model_dump()
        task_data['is_applied'] = t.id in applied_set
        results.append(task_data)
    return results

@task_router.get("/tasks" , response_model=list[TaskRead])
def read_task (session : Session = Depends(get_session)) :
    tasks = session.exec(select(Task)).all()
    return tasks


@task_router.post("/tasks" , response_model=TaskRead ) 
def post_task (task : TaskCreate , current_user : User = Depends(get_current_user) ,session :Session = Depends(get_session)):
    if current_user.auth == 'admin' :
        task_dict = task.model_dump()
        db_task = Task(
            **task_dict,
            admin_id=current_user.id,
            status = "available"
        )
        
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task
    
    raise HTTPException(
            status_code=403, 
            detail="Bạn không có quyền tạo Task. Chỉ Admin mới được phép!"
        )
    

    
@task_router.patch("/tasks/{task_id}", response_model=TaskRead)
def update_task_status( new_status: str, current_user : User = Depends(get_current_user) ,session: Session = Depends(get_session)):
    if current_user.auth == 'admin' :
        db_task = session.get(Task, current_user.id)
        if not db_task:
             raise HTTPException(status_code=404, detail="Task khong ton tai")
        db_task.status = new_status
        session.add(db_task)
        session.commit()
        session.refresh(db_task)    
        return db_task
    raise HTTPException(
            status_code=403, 
            detail="Bạn không có quyền tạo Task. Chỉ Admin mới được phép!"
        )
   
    
@task_router.delete("/tasks/{task_id}")
def delete_task (task_id : int ,current_user : User = Depends(get_current_user),session : Session = Depends(get_session)):
    if current_user.auth == 'admin' :
        db_task = session.get(Task,task_id)
        if db_task :
            session.delete(db_task)
            session.commit()
            return {"ok": True ,'status' : "thanh cong" , "detail" : "da xoa thanh cong task can xoa"}
        raise HTTPException(status_code=400 , detail="khong tim thay task can xoa")
    raise HTTPException (status_code=403,detail="Bạn không có quyền xóa Task. Chỉ Admin mới được phép!")