from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db, Config, Middleware
from pydantic import BaseModel
from typing import List, Optional
import datetime
import json

router = APIRouter()

# 配置文件基础模型
class ConfigBase(BaseModel):
    middleware_id: int
    name: str
    content: str

# 配置文件响应模型
class ConfigResponse(ConfigBase):
    id: int
    version: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    
    class Config:
        from_attributes = True

# 策略选择模型
class UpdateStrategy(BaseModel):
    strategy: str  # immediate, scheduled, rolling
    scheduled_time: Optional[datetime.datetime] = None

# 获取中间件的所有配置文件
@router.get("/middleware/{middleware_id}", response_model=List[ConfigResponse])
def get_middleware_configs(middleware_id: int, db: Session = Depends(get_db)):
    # 检查中间件是否存在
    middleware = db.query(Middleware).filter(Middleware.id == middleware_id).first()
    if not middleware:
        raise HTTPException(status_code=404, detail="中间件不存在")
    
    return db.query(Config).filter(Config.middleware_id == middleware_id).all()

# 获取单个配置文件
@router.get("/{config_id}", response_model=ConfigResponse)
def get_config(config_id: int, db: Session = Depends(get_db)):
    config = db.query(Config).filter(Config.id == config_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="配置文件不存在")
    return config

# 创建配置文件
@router.post("/", response_model=ConfigResponse)
def create_config(config: ConfigBase, db: Session = Depends(get_db)):
    # 检查中间件是否存在
    middleware = db.query(Middleware).filter(Middleware.id == config.middleware_id).first()
    if not middleware:
        raise HTTPException(status_code=404, detail="中间件不存在")
    
    # 检查配置文件名称是否已存在
    existing = db.query(Config).filter(
        Config.middleware_id == config.middleware_id,
        Config.name == config.name
    ).first()
    
    if existing:
        # 更新现有配置文件，版本号+1
        existing.content = config.content
        existing.version += 1
        db.commit()
        db.refresh(existing)
        return existing
    else:
        # 创建新配置文件
        db_config = Config(**config.model_dump())
        db.add(db_config)
        db.commit()
        db.refresh(db_config)
        return db_config

# 上传配置文件
@router.post("/upload/{middleware_id}", response_model=ConfigResponse)
async def upload_config(middleware_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    # 检查中间件是否存在
    middleware = db.query(Middleware).filter(Middleware.id == middleware_id).first()
    if not middleware:
        raise HTTPException(status_code=404, detail="中间件不存在")
    
    # 读取文件内容
    content = await file.read()
    content_str = content.decode("utf-8")
    
    # 检查配置文件名称是否已存在
    existing = db.query(Config).filter(
        Config.middleware_id == middleware_id,
        Config.name == file.filename
    ).first()
    
    if existing:
        # 更新现有配置文件，版本号+1
        existing.content = content_str
        existing.version += 1
        db.commit()
        db.refresh(existing)
        return existing
    else:
        # 创建新配置文件
        db_config = Config(
            middleware_id=middleware_id,
            name=file.filename,
            content=content_str
        )
        db.add(db_config)
        db.commit()
        db.refresh(db_config)
        return db_config

# 下载配置文件
@router.get("/{config_id}/download")
def download_config(config_id: int, db: Session = Depends(get_db)):
    config = db.query(Config).filter(Config.id == config_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="配置文件不存在")
    
    from fastapi.responses import PlainTextResponse
    return PlainTextResponse(config.content, media_type="text/plain", headers={
        "Content-Disposition": f"attachment; filename={config.name}"
    })

# 更新配置文件
@router.put("/{config_id}", response_model=ConfigResponse)
def update_config(config_id: int, config: ConfigBase, db: Session = Depends(get_db)):
    db_config = db.query(Config).filter(Config.id == config_id).first()
    if not db_config:
        raise HTTPException(status_code=404, detail="配置文件不存在")
    
    # 更新配置文件，版本号+1
    for key, value in config.model_dump().items():
        setattr(db_config, key, value)
    db_config.version += 1
    db.commit()
    db.refresh(db_config)
    return db_config

# 删除配置文件
@router.delete("/{config_id}")
def delete_config(config_id: int, db: Session = Depends(get_db)):
    db_config = db.query(Config).filter(Config.id == config_id).first()
    if not db_config:
        raise HTTPException(status_code=404, detail="配置文件不存在")
    
    db.delete(db_config)
    db.commit()
    return {"message": "配置文件删除成功"}

# 应用配置更新策略
@router.post("/{config_id}/apply-strategy")
def apply_strategy(config_id: int, strategy: UpdateStrategy, db: Session = Depends(get_db)):
    config = db.query(Config).filter(Config.id == config_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="配置文件不存在")
    
    # 这里可以根据策略类型执行不同的更新逻辑
    # 例如：立即更新、定时更新、滚动更新等
    
    return {
        "message": f"配置更新策略已应用: {strategy.strategy}",
        "config_id": config_id,
        "scheduled_time": strategy.scheduled_time
    }
