from schema import TaskApplyRead  ,TaskReadWithStatus ,TaskApplyWithUser
from connect_database import engine , get_session
from fastapi import APIRouter , Depends , HTTPException
from sqlmodel import Session, select 
from models import TaskApply , User , Task 
from auth import get_current_user
from datetime import datetime
router_task_apply = APIRouter()

@router_task_apply.get('/{task_id}' )
def get_taskapplied (task_id : int , session : Session = Depends(get_session)  ):
    apply_task_id = session.exec(select(TaskApply).where(TaskApply.task_id == task_id)).all()
    return apply_task_id



@router_task_apply.post("/taskapply/{task_id}" , response_model=TaskApplyRead)
def addTaskApply (task_id : int  , current_user : User = Depends(get_current_user) ,session : Session = Depends(get_session)):
    statement = session.exec(select(TaskApply).where(TaskApply.task_id == task_id , TaskApply.user_id ==current_user.id )).first()
    if statement :
        raise HTTPException(status_code=400 , detail="người dùng đã đăng ký task rồi, vui lòng k spam")
    new_apply_task = TaskApply(
        
        user_id= current_user.id,
        task_id= task_id
    )
    
    session.add(new_apply_task)
    session.commit()
    session.refresh(new_apply_task)
    return new_apply_task


@router_task_apply.patch("/approve/{task_id}")
def approve_request(task_id : int ,user_id : int , session : Session = Depends(get_session) , current_user : User = Depends(get_current_user)):
    # chuyển trạng thái task qua doing , thêm cả stared_at
    if current_user.auth != 'admin':
        raise HTTPException(status_code=403, detail="Chỉ Admin mới có quyền duyệt đơn!")
    task_request = session.get(Task,task_id)
   
    if not task_request :
        raise HTTPException (status_code=400 , detail="task này lỗi gòi bạn ơi")
    # chuyển trạng thái của người dùng thành đã được chấp nhận và những người khác = reject
    try :
        accept_apply = session.exec(select(TaskApply).where(TaskApply.task_id == task_id ,TaskApply.user_id ==user_id)).first()
        if not accept_apply:
            raise HTTPException(status_code=404, detail="Không tìm thấy đơn ứng tuyển của người dùng này!")
        other_applies = session.exec(select(TaskApply).where(TaskApply.task_id == task_id ,TaskApply.user_id !=user_id)).all()
        task_request.started_at = datetime.now()
        task_request.status = 'doing'
        task_request.member_id = user_id
        accept_apply.status = 'Accept'
        for user in other_applies:
            user.status = 'Reject'
            session.add(user)
        session.add(accept_apply)
        session.add(task_request)
        session.commit()
        return {"message": "Duyệt thành công!", "task_id": task_id, "approved_user": user_id}
    except Exception as e :
        session.rollback()
        print(f"Lỗi xử lý duyệt đơn: {e}")
        raise HTTPException(status_code=500, detail="Lỗi hệ thống khi phê duyệt đơn")
        

