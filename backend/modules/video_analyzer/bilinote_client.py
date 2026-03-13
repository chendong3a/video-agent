"""
BiliNote客户端 - 视频分析
支持B站、抖音视频链接分析，返回结构化内容
"""
import re
import httpx
from typing import Dict, List, Optional
from loguru import logger
from config import settings


class BiliNoteClient:
    """BiliNote API客户端"""
    
    def __init__(self):
        self.base_url = settings.BILINOTE_API_URL.rstrip('/')
        self.timeout = 300  # 5分钟超时
    
    def _detect_platform(self, url: str) -> str:
        """检测视频平台"""
        if 'bilibili.com' in url or 'b23.tv' in url:
            return 'bilibili'
        elif 'douyin.com' in url or 'tiktok.com' in url:
            return 'douyin'
        else:
            return 'unknown'
    
    def _extract_video_id(self, url: str, platform: str) -> Optional[str]:
        """提取视频ID"""
        if platform == 'bilibili':
            # 匹配 BV号
            match = re.search(r'(BV[a-zA-Z0-9]+)', url)
            if match:
                return match.group(1)
            # 匹配 av号
            match = re.search(r'av(\d+)', url)
            if match:
                return f'av{match.group(1)}'
        elif platform == 'douyin':
            match = re.search(r'/video/(\d+)', url)
            if match:
                return match.group(1)
        return None

    async def analyze_video(self, video_url: str) -> Dict:
        """
        分析视频内容，返回结构化数据
        
        参数:
            video_url: B站或抖音视频URL
            
        返回:
            {
                "title": "视频标题",
                "platform": "bilibili/douyin",
                "video_id": "BVxxxxx",
                "markdown": "Markdown格式的内容",
                "transcript": "完整转录文本",
                "summary": "内容摘要",
                "key_points": ["要点1", "要点2"],
                "duration": 视频时长(秒)
            }
        """
        platform = self._detect_platform(video_url)
        video_id = self._extract_video_id(video_url, platform)
        
        logger.info(f"开始分析视频: platform={platform}, id={video_id}, url={video_url}")
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                # 调用BiliNote API
                response = await client.post(
                    f"{self.base_url}/api/note",
                    json={
                        "url": video_url,
                        "platform": platform,
                        "quality": "high",
                        "include_transcript": True
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                # 解析返回数据
                markdown = data.get("markdown", data.get("content", ""))
                parsed = self.parse_markdown(markdown)
                
                result = {
                    "title": data.get("title", "未知标题"),
                    "platform": platform,
                    "video_id": video_id,
                    "markdown": markdown,
                    "transcript": data.get("transcript", ""),
                    "summary": parsed["summary"],
                    "key_points": parsed["key_points"],
                    "chapters": parsed["chapters"],
                    "duration": data.get("duration", 0)
                }
                
                logger.info(f"视频分析完成: {result['title']}, 时长: {result['duration']}s")
                return result
                
            except httpx.ConnectError:
                logger.error(f"无法连接BiliNote服务: {self.base_url}")
                raise Exception(f"无法连接BiliNote服务({self.base_url})，请确认服务已启动")
            except httpx.HTTPStatusError as e:
                logger.error(f"BiliNote API返回错误: {e.response.status_code}")
                raise Exception(f"BiliNote API错误: HTTP {e.response.status_code}")
            except Exception as e:
                logger.error(f"视频分析失败: {str(e)}")
                raise

    async def check_health(self) -> bool:
        """检查BiliNote服务是否可用"""
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get(f"{self.base_url}/health")
                return response.status_code == 200
        except Exception:
            return False

    def parse_markdown(self, markdown: str) -> Dict:
        """
        解析Markdown内容，提取关键信息
        
        返回:
            {
                "summary": "内容摘要",
                "key_points": ["要点1", "要点2"],
                "chapters": [{"title": "章节1", "content": "..."}]
            }
        """
        if not markdown:
            return {"summary": "", "key_points": [], "chapters": []}
        
        lines = markdown.strip().split('\n')
        summary = ""
        key_points = []
        chapters = []
        current_chapter = None
        
        for line in lines:
            stripped = line.strip()
            
            # 提取章节标题 (## 或 ###)
            if stripped.startswith('## ') or stripped.startswith('### '):
                if current_chapter:
                    chapters.append(current_chapter)
                title = stripped.lstrip('#').strip()
                current_chapter = {"title": title, "content": ""}
                continue
            
            # 提取要点 (- 或 * 开头的列表项)
            if stripped.startswith('- ') or stripped.startswith('* '):
                point = stripped[2:].strip()
                if point and len(point) > 5:
                    key_points.append(point)
            
            # 累积章节内容
            if current_chapter and stripped:
                current_chapter["content"] += stripped + "\n"
        
        # 添加最后一个章节
        if current_chapter:
            chapters.append(current_chapter)
        
        # 生成摘要：取前200字的纯文本
        plain_text = re.sub(r'[#*\-\[\]()>]', '', markdown)
        plain_text = re.sub(r'\s+', ' ', plain_text).strip()
        summary = plain_text[:200] + "..." if len(plain_text) > 200 else plain_text
        
        # 限制要点数量
        key_points = key_points[:10]
        
        return {
            "summary": summary,
            "key_points": key_points,
            "chapters": chapters
        }
