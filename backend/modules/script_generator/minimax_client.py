"""
MiniMax API客户端 - 文案生成
"""
import httpx
from typing import Dict, Optional
from config import settings


class MinimaxClient:
    """MiniMax API客户端"""
    
    def __init__(self):
        self.api_key = settings.MINIMAX_API_KEY
        self.group_id = settings.MINIMAX_GROUP_ID
        self.base_url = "https://api.minimax.chat/v1"
    
    async def generate_script(
        self,
        markdown_content: str,
        style: str = "professional",
        max_length: int = 500
    ) -> str:
        """
        基于Markdown内容生成口播文案
        
        参数:
            markdown_content: BiliNote生成的Markdown内容
            style: 文案风格 (professional/funny/emotional/sales)
            max_length: 最大字数
            
        返回:
            生成的口播文案
        """
        prompt = self._build_prompt(markdown_content, style, max_length)
        
        async with httpx.AsyncClient(timeout=60) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/text/chatcompletion_v2",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "abab6.5-chat",
                        "messages": [
                            {
                                "role": "system",
                                "content": "你是一个专业的视频文案创作者，擅长将内容改写成适合口播的文案。"
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        "temperature": 0.7,
                        "max_tokens": max_length * 2
                    }
                )
                response.raise_for_status()
                result = response.json()
                return result["choices"][0]["message"]["content"]
            except httpx.HTTPError as e:
                raise Exception(f"MiniMax API调用失败: {str(e)}")
    
    def _build_prompt(self, content: str, style: str, max_length: int) -> str:
        """构建Prompt"""
        style_prompts = {
            "professional": "专业、严谨、信息密度高",
            "funny": "幽默风趣、轻松活泼、有梗",
            "emotional": "情感丰富、有感染力、引发共鸣",
            "sales": "带货风格、突出卖点、引导购买"
        }
        
        style_desc = style_prompts.get(style, "专业")
        
        return f"""
请基于以下视频内容，生成一段适合口播的视频文案。

要求：
1. 风格：{style_desc}
2. 字数：约{max_length}字
3. 适合真人出镜口播，语言自然流畅
4. 保留核心信息，但用更生动的表达方式
5. 开头要吸引人，结尾要有总结或呼吁

原始内容：
{content}

请直接输出文案，不要有其他说明文字。
"""
