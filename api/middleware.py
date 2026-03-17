from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, Middleware, MiddlewareRelation
from pydantic import BaseModel
from typing import List, Optional
import datetime

router = APIRouter()

# 中间件基础模型
class MiddlewareBase(BaseModel):
    name: str
    type: str
    version: str
    status: str
    description: Optional[str] = None

# 中间件响应模型
class MiddlewareResponse(MiddlewareBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    
    class Config:
        from_attributes = True

# 中间件关系基础模型
class MiddlewareRelationBase(BaseModel):
    source_id: int
    target_id: int
    relation_type: str

# 中间件关系响应模型
class MiddlewareRelationResponse(MiddlewareRelationBase):
    id: int
    created_at: datetime.datetime
    
    class Config:
        from_attributes = True

# 获取所有中间件
@router.get("/", response_model=List[MiddlewareResponse])
def get_middlewares(db: Session = Depends(get_db)):
    return db.query(Middleware).all()

# 获取单个中间件
@router.get("/{middleware_id}", response_model=MiddlewareResponse)
def get_middleware(middleware_id: int, db: Session = Depends(get_db)):
    middleware = db.query(Middleware).filter(Middleware.id == middleware_id).first()
    if not middleware:
        raise HTTPException(status_code=404, detail="中间件不存在")
    return middleware

# 创建中间件
@router.post("/", response_model=MiddlewareResponse)
def create_middleware(middleware: MiddlewareBase, db: Session = Depends(get_db)):
    # 检查名称是否已存在
    existing = db.query(Middleware).filter(Middleware.name == middleware.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="中间件名称已存在")
    
    db_middleware = Middleware(**middleware.model_dump())
    db.add(db_middleware)
    db.commit()
    db.refresh(db_middleware)
    return db_middleware

# 更新中间件
@router.put("/{middleware_id}", response_model=MiddlewareResponse)
def update_middleware(middleware_id: int, middleware: MiddlewareBase, db: Session = Depends(get_db)):
    db_middleware = db.query(Middleware).filter(Middleware.id == middleware_id).first()
    if not db_middleware:
        raise HTTPException(status_code=404, detail="中间件不存在")
    
    # 检查名称是否与其他中间件冲突
    if middleware.name != db_middleware.name:
        existing = db.query(Middleware).filter(Middleware.name == middleware.name).first()
        if existing:
            raise HTTPException(status_code=400, detail="中间件名称已存在")
    
    for key, value in middleware.model_dump().items():
        setattr(db_middleware, key, value)
    db.commit()
    db.refresh(db_middleware)
    return db_middleware

# 删除中间件
@router.delete("/{middleware_id}")
def delete_middleware(middleware_id: int, db: Session = Depends(get_db)):
    db_middleware = db.query(Middleware).filter(Middleware.id == middleware_id).first()
    if not db_middleware:
        raise HTTPException(status_code=404, detail="中间件不存在")
    
    db.delete(db_middleware)
    db.commit()
    return {"message": "中间件删除成功"}

# 获取中间件关系
@router.get("/relations/all", response_model=List[MiddlewareRelationResponse])
def get_relations(db: Session = Depends(get_db)):
    return db.query(MiddlewareRelation).all()

# 创建中间件关系
@router.post("/relations", response_model=MiddlewareRelationResponse)
def create_relation(relation: MiddlewareRelationBase, db: Session = Depends(get_db)):
    # 检查源中间件和目标中间件是否存在
    source = db.query(Middleware).filter(Middleware.id == relation.source_id).first()
    target = db.query(Middleware).filter(Middleware.id == relation.target_id).first()
    if not source or not target:
        raise HTTPException(status_code=404, detail="源中间件或目标中间件不存在")
    
    # 检查关系是否已存在
    existing = db.query(MiddlewareRelation).filter(
        MiddlewareRelation.source_id == relation.source_id,
        MiddlewareRelation.target_id == relation.target_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="关系已存在")
    
    db_relation = MiddlewareRelation(**relation.model_dump())
    db.add(db_relation)
    db.commit()
    db.refresh(db_relation)
    return db_relation

# 删除中间件关系
@router.delete("/relations/{relation_id}")
def delete_relation(relation_id: int, db: Session = Depends(get_db)):
    db_relation = db.query(MiddlewareRelation).filter(MiddlewareRelation.id == relation_id).first()
    if not db_relation:
        raise HTTPException(status_code=404, detail="关系不存在")
    
    db.delete(db_relation)
    db.commit()
    return {"message": "关系删除成功"}
