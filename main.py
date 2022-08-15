import celery as celery
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request

from api.api_v1.routers.auth import auth_router
from api.api_v1.routers.users import users_router
from core import config
from core.auth import get_current_active_user
from db.session import SessionLocal, engine, Base
import tasks

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=config.PROJECT_NAME,docs_url="/api/docs",openapi_url="/api"
)

# 跨域配置
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 使用拦截器，在每个请求前，创建数据库连接,并将连接写到request中
@app.middleware("http")
def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal() # 动态的给request 添加一个state属性，state 为字典类型，为state 动态添加一个 value属性，其值为右边
    response = call_next(request)
    return response

# 添加任务消息队列
@app.get('/api/v1/task')
def example_task():
    # 生产者：发送消息，调用任务
    # todo
    tasks.example_task.delay("hello world")

    return {"message":"success"}


@app.get("/api/v1")
def root():
    return {"message": "Hello World"}


app.include_router(
    users_router,
    prefix="/api/v1",
    tags=["users"],
    dependencies=[Depends(get_current_active_user)],
)
app.include_router(
    auth_router,
    prefix="/api",
    tags=["auth"],
)

# import uvicorn
# if  __name__ == "__main__":
#    with engine.begin() as conn:
#        conn
