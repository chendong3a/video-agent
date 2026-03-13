"""
任务管理路由
"""
import os
import uuid
import json
from datetime import datetime
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import Optional
from pydantic import BaseModel
from loguru import logger

from config import settings
from modules.video_analyzer.bilinote_client import BiliNoteClient
from modules.script_generator.minimax_client import MinimaxClient

router = APIRouter()

# 内存任务存储（后续可替换为数据库）
tasks_store = {}


class TaskResponse(BaseModel):
    task_id: str
    status: str
    message: str


def _ensure_dirs():
    """确保存储目录存在"""
    for d in [settings.UPLOAD_DIR, settings.OUTPUT_DIR, settings.TEMP_DIR]:
        os.makedirs(d, exist_ok=True)


@router.post("/create", response_model=TaskResponse)
async def create_task(
    video_url: str = Form(...),
    script_style: str = Form("professional"),
    bgm_style: str = Form("auto")
):
    """创建视频生成任务"""
    _ensure_dirs()
    task_id = f"task_{uuid.uuid4().hex[:12]}"
    
    tasks_store[task_id] = {
        "task_id": task_id,
        "video_url": video_url,
        "script_style": script_style,
        "bgm_style": bgm_style,
        "status": "pending",
        "progress": 0,
        "current_step": "等待处理",
        "created_at": datetime.now().isoformat(),
        "steps": [
            {"name": "视频分析", "status": "pending"},
            {"name": "文案生成", "status": "pending"},
            {"name": "声音克隆", "status": "pending"},
            {"name": "口型对齐", "status": "pending"},
            {"name": "后期合成", "status": "pending"}
        ],
        "result": None
    }
    
    logger.info(f"任务创建: {task_id}, url={video_url}, style={script_style}")
    
    return {
        "task_id": task_id,
        "status": "pending",
        "message": "任务创建成功，正在处理中..."
    }


@router.post("/analyze")
async def analyze_video(video_url: str = Form(...)):
    """
    单独调用视频分析接口（用于预览）
    """
    client = BiliNoteClient()
    
    try:
        result = await client.analyze_video(video_url)
        return {
            "status": "ok",
            "data": result
        }
    except Exception as e:
        logger.error(f"视频分析失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-script")
async def generate_script(
    content: str = Form(...),
    style: str = Form("professional"),
    max_length: int = Form(500)
):
    """
    单独调用文案生成接口（用于预览和调整）
    """
    client = MinimaxClient()
    
    try:
        result = await client.generate_script(content, style=style, max_length=max_length)
        return {
            "status": "ok",
            "data": result
        }
    except Exception as e:
        logger.error(f"文案生成失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-all-scripts")
async def generate_all_scripts(
    content: str = Form(...),
    max_length: int = Form(500)
):
    """
    生成所有风格的文案，供用户选择
    """
    client = MinimaxClient()
    
    try:
        results = await client.generate_all_styles(content, max_length=max_length)
        return {
            "status": "ok",
            "data": results
        }
    except Exception as e:
        logger.error(f"批量文案生成失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload/voice")
async def upload_voice(file: UploadFile = File(...)):
    """上传声音样本"""
    _ensure_dirs()
    file_id = f"voice_{uuid.uuid4().hex[:8]}"
    ext = os.path.splitext(file.filename)[1] or '.wav'
    save_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}{ext}")
    
    content = await file.read()
    with open(save_path, 'wb') as f:
        f.write(content)
    
    logger.info(f"声音样本上传: {file_id}, size={len(content)}, file={file.filename}")
    
    return {
        "file_id": file_id,
        "filename": file.filename,
        "path": save_path,
        "size": len(content),
        "message": "声音样本上传成功"
    }


@router.post("/upload/video")
async def upload_video(file: UploadFile = File(...)):
    """上传底片视频"""
    _ensure_dirs()
    file_id = f"video_{uuid.uuid4().hex[:8]}"
    ext = os.path.splitext(file.filename)[1] or '.mp4'
    save_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}{ext}")
    
    content = await file.read()
    with open(save_path, 'wb') as f:
        f.write(content)
    
    logger.info(f"底片视频上传: {file_id}, size={len(content)}, file={file.filename}")
    
    return {
        "file_id": file_id,
        "filename": file.filename,
        "path": save_path,
        "size": len(content),
        "message": "底片视频上传成功"
    }


@router.get("/list")
async def list_tasks():
    """获取所有任务列表"""
    task_list = sorted(
        tasks_store.values(),
        key=lambda x: x.get("created_at", ""),
        reverse=True
    )
    return {
        "status": "ok",
        "total": len(task_list),
        "tasks": task_list
    }


@router.get("/{task_id}/status")
async def get_task_status(task_id: str):
    """查询任务状态"""
    task = tasks_store.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    return {
        "task_id": task_id,
        "status": task["status"],
        "progress": task["progress"],
        "current_step": task["current_step"],
        "steps": task["steps"],
        "created_at": task["created_at"]
    }


@router.get("/{task_id}/result")
async def get_task_result(task_id: str):
    """获取任务结果"""
    task = tasks_store.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    if task["status"] != "completed":
        return {
            "task_id": task_id,
            "status": task["status"],
            "message": "任务尚未完成"
        }
    
    return {
        "task_id": task_id,
        "status": "completed",
        "result": task.get("result", {}),
        "output_video_url": f"/api/file/download/{task_id}.mp4"
    }


@router.delete("/{task_id}")
async def cancel_task(task_id: str):
    """取消任务"""
    task = tasks_store.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    task["status"] = "cancelled"
    task["current_step"] = "已取消"
    logger.info(f"任务取消: {task_id}")
    
    return {
        "task_id": task_id,
        "message": "任务已取消"
    }
