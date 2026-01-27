from fastapi import FastAPI , Depends 
from sqlmodel import Session , select 
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .models import Task , TaskRead
from .connect_database import engine 

app =  FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Cho phép tất cả các nguồn truy cập
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_session ():
    with Session(engine) as session :
        yield session

@app.get("/")
async def read_index():
    return FileResponse('src/front-end/fontend.html')

@app.get("/tasks" , response_model=list[TaskRead])
def read_task (session : Session = Depends(get_session)) :
    tasks = session.exec(select(Task)).all()
    return tasks


@app.post("/tasks" , response_model=TaskRead)
def post_task (task : Task ,session :Session = Depends(get_session)):
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

    

@app.patch("/tasks/{task_id}" , response_model=Task)
def update_task (task_id : int , session : Session = Depends(get_session)) :
    db_task = session.get(Task , task_id)
    if db_task :
        db_task.is_completed = not db_task.is_completed
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
    return db_task