from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Router_api.user import user_router
from Router_api.task import task_router
from Router_api.taskapply   import router_task_apply
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # Nếu đang chạy Live Server ở cổng 5500, nên điền rõ để an toàn
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(task_router, prefix="/tasks", tags=["Task"])
app.include_router(router_task_apply, prefix="/taskapply", tags=["Taskapply"])
