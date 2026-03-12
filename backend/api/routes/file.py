"""
文件管理路由
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

router = APIRouter()


@router.get("/download/{filename}")
async def download_file(filename: str):
    """下载生成的视频文件"""
    # TODO: 实现文件下载
    file_path = f"./storage/outputs/{filename}"
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="文件不存在")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="video/mp4"
    )


@router.get("/preview/{task_id}")
async def preview_video(task_id: str):
    """预览视频"""
    # TODO: 实现视频预览
    return {
        "task_id": task_id,
        "preview_url": f"/api/file/download/{task_id}_preview.mp4"
    }
