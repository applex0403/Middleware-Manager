from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import datetime

Base = declarative_base()

# 中间件组模型
class MiddlewareGroup(Base):
    __tablename__ = "middleware_group"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # 关联中间件
    middlewares = relationship("Middleware", back_populates="group")

# 中间件模型
class Middleware(Base):
    __tablename__ = "middleware"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    type = Column(String(100))
    version = Column(String(50))
    status = Column(String(50))
    description = Column(Text)
    host_ip = Column(String(100))  # 主机IP
    password = Column(String(255))  # 密码
    group_id = Column(Integer, ForeignKey("middleware_group.id"))  # 组ID
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # 关联配置文件
    configs = relationship("Config", back_populates="middleware")
    # 关联拓扑关系
    source_relationships = relationship("MiddlewareRelation", foreign_keys="MiddlewareRelation.source_id", back_populates="source")
    target_relationships = relationship("MiddlewareRelation", foreign_keys="MiddlewareRelation.target_id", back_populates="target")
    # 关联组
    group = relationship("MiddlewareGroup", back_populates="middlewares")

# 配置文件模型
class Config(Base):
    __tablename__ = "config"
    id = Column(Integer, primary_key=True, index=True)
    middleware_id = Column(Integer, ForeignKey("middleware.id"))
    name = Column(String(255))
    content = Column(Text)
    version = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # 关联中间件
    middleware = relationship("Middleware", back_populates="configs")

# 中间件关系模型
class MiddlewareRelation(Base):
    __tablename__ = "middleware_relation"
    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("middleware.id"))
    target_id = Column(Integer, ForeignKey("middleware.id"))
    relation_type = Column(String(100))  # 例如：依赖、调用等
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # 关联源中间件和目标中间件
    source = relationship("Middleware", foreign_keys=[source_id], back_populates="source_relationships")
    target = relationship("Middleware", foreign_keys=[target_id], back_populates="target_relationships")

# 创建数据库引擎
engine = create_engine("sqlite:///middleware.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 依赖项，用于获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
