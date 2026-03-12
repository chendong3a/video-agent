"""
视频合成器 - 最终合成
"""
import os
from typing import Optional
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
from PIL import Image, ImageDraw, ImageFont


class VideoComposer:
    """视频合成器"""
    
    def __init__(self):
        pass
    
    def add_subtitle(
        self,
        video_path: str,
        srt_path: str,
        output_path: str,
        font_size: int = 24,
        font_color: str = "white"
    ) -> str:
        """
        添加字幕到视频
        
        参数:
            video_path: 视频路径
            srt_path: SRT字幕文件路径
            output_path: 输出视频路径
            font_size: 字体大小
            font_color: 字体颜色
            
        返回:
            输出视频路径
        """
        # TODO: 使用FFmpeg烧录字幕
        # ffmpeg -i video.mp4 -vf subtitles=subtitle.srt output.mp4
        
        import subprocess
        cmd = [
            'ffmpeg', '-i', video_path,
            '-vf', f"subtitles={srt_path}:force_style='FontSize={font_size},PrimaryColour=&H{font_color}'",
            '-c:a', 'copy',
            output_path
        ]
        subprocess.run(cmd, check=True)
        
        return output_path
    
    def add_title(
        self,
        video_path: str,
        title: str,
        output_path: str,
        duration: float = 3.0,
        position: str = "top"
    ) -> str:
        """
        添加标题到视频
        
        参数:
            video_path: 视频路径
            title: 标题文字
            output_path: 输出视频路径
            duration: 标题显示时长（秒）
            position: 位置 (top/center/bottom)
            
        返回:
            输出视频路径
        """
        video = VideoFileClip(video_path)
        
        # 创建标题文字
        txt_clip = TextClip(
            title,
            fontsize=48,
            color='white',
            font='Arial',
            stroke_color='black',
            stroke_width=2
        ).set_duration(duration)
        
        # 设置位置
        if position == "top":
            txt_clip = txt_clip.set_position(('center', 50))
        elif position == "center":
            txt_clip = txt_clip.set_position('center')
        else:  # bottom
            txt_clip = txt_clip.set_position(('center', video.h - 100))
        
        # 合成
        final = CompositeVideoClip([video, txt_clip])
        final.write_videofile(output_path, codec='libx264', audio_codec='aac')
        
        return output_path
    
    def add_bgm(
        self,
        video_path: str,
        bgm_path: str,
        output_path: str,
        bgm_volume: float = 0.3
    ) -> str:
        """
        添加背景音乐
        
        参数:
            video_path: 视频路径
            bgm_path: BGM音频路径
            output_path: 输出视频路径
            bgm_volume: BGM音量 (0.0-1.0)
            
        返回:
            输出视频路径
        """
        # TODO: 使用FFmpeg混音
        # ffmpeg -i video.mp4 -i bgm.mp3 -filter_complex 
        # "[1:a]volume=0.3[a1];[0:a][a1]amix=inputs=2:duration=first[aout]" 
        # -map 0:v -map "[aout]" output.mp4
        
        import subprocess
        cmd = [
            'ffmpeg', '-i', video_path, '-i', bgm_path,
            '-filter_complex',
            f'[1:a]volume={bgm_volume}[a1];[0:a][a1]amix=inputs=2:duration=first[aout]',
            '-map', '0:v', '-map', '[aout]',
            '-c:v', 'copy',
            output_path
        ]
        subprocess.run(cmd, check=True)
        
        return output_path
    
    def compose_final(
        self,
        video_path: str,
        audio_path: str,
        srt_path: Optional[str],
        bgm_path: Optional[str],
        title: Optional[str],
        output_path: str
    ) -> str:
        """
        最终合成
        
        参数:
            video_path: 口型对齐后的视频
            audio_path: 克隆的音频
            srt_path: 字幕文件（可选）
            bgm_path: BGM文件（可选）
            title: 标题（可选）
            output_path: 输出路径
            
        返回:
            最终视频路径
        """
        temp_path = output_path.replace('.mp4', '_temp.mp4')
        
        # 1. 替换音频
        video = VideoFileClip(video_path)
        audio = AudioFileClip(audio_path)
        video_with_audio = video.set_audio(audio)
        video_with_audio.write_videofile(temp_path, codec='libx264', audio_codec='aac')
        
        current_video = temp_path
        
        # 2. 添加字幕
        if srt_path:
            temp_subtitle = output_path.replace('.mp4', '_subtitle.mp4')
            self.add_subtitle(current_video, srt_path, temp_subtitle)
            current_video = temp_subtitle
        
        # 3. 添加BGM
        if bgm_path:
            temp_bgm = output_path.replace('.mp4', '_bgm.mp4')
            self.add_bgm(current_video, bgm_path, temp_bgm)
            current_video = temp_bgm
        
        # 4. 添加标题
        if title:
            self.add_title(current_video, title, output_path)
        else:
            os.rename(current_video, output_path)
        
        # 清理临时文件
        for temp in [temp_path, temp_path.replace('_temp', '_subtitle'), 
                     temp_path.replace('_temp', '_bgm')]:
            if os.path.exists(temp) and temp != output_path:
                os.remove(temp)
        
        return output_path
