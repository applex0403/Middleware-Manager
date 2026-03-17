from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from api import middleware, config

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(title="中间件管理平台")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(middleware.router, prefix="/api/middleware", tags=["middleware"])
app.include_router(config.router, prefix="/api/config", tags=["config"])

@app.get("/")
def read_root():
    return {"message": "中间件管理平台 API"}
