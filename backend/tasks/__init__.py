"""
Celery任务模块
"""
from .pipeline import (
    analyze_video_task,
    generate_script_task,
    clone_voice_task,
    sync_lip_task,
    compose_final_task,
    create_video_pipeline
)

__all__ = [
    "analyze_video_task",
    "generate_script_task",
    "clone_voice_task",
    "sync_lip_task",
    "compose_final_task",
    "create_video_pipeline"
]
