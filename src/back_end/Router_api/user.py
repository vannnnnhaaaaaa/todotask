from fastapi import Depends  , HTTPException , APIRouter
from sqlmodel import select, Session 
from fastapi.responses import FileResponse
from models import User
from schema import UserCreate , UserRead
from connect_database import get_session
from auth import hash_password , verify_password , create_access_token
user_router = APIRouter()


@user_router.post("/login")
def login (user : UserCreate , session : Session = Depends(get_session)) :
    user_in_db = session.exec(select(User).where(User.user_name == user.user_name)).first()
    if not user_in_db :
        raise HTTPException(status_code= 400 , detail="User not found")
    if not verify_password(user.password, user_in_db.hashed_password) :
        raise HTTPException(status_code=400 , detail="Wrong Password")
    
    access_token = create_access_token({
        "sub" :user_in_db.user_name ,
        "user_id" : user_in_db.id,
        "role" : user_in_db.auth
    })

    return {"access_token": access_token, "token_type": "bearer" , 'auth' :user_in_db.auth }

@user_router.post("/register" , response_model=UserRead)
def register (user : UserCreate  , session : Session = Depends(get_session)):
    exist_user = session.exec(select(User).where(User.user_name == user.user_name)).first()
    if exist_user :
        raise HTTPException(status_code=400 , detail="Username already exist")
    print(f"matkhau da nhap :{user.password} ")
    hashed_string = hash_password(user.password)
    print(f"matkhau da hash :{hashed_string} ")
    new_user = User (
        user_name= user.user_name,
        hashed_password= hashed_string ,
        auth='member'
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

    


