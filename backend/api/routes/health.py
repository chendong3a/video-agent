"""
健康检查路由
"""
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "ok",
        "service": "视频智能体",
        "timestamp": datetime.now().isoformat()
    }


@router.get("/version")
async def version():
    """版本信息"""
    return {
        "version": "1.0.0",
        "api_version": "v1"
    }
