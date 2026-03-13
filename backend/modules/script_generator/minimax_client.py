"""
MiniMax API客户端 - 文案生成
支持4种风格：专业、幽默、情感、带货
"""
import httpx
from typing import Dict, Optional
from loguru import logger
from config import settings


# 风格Prompt模板
STYLE_PROMPTS = {
    "professional": {
        "name": "专业风格",
        "system": "你是一位资深的知识类视频创作者，擅长用专业但易懂的语言讲解复杂话题。你的文案信息密度高、逻辑清晰、有理有据。",
        "instruction": """要求：
1. 语言专业严谨，但不晦涩
2. 信息密度高，每句话都有价值
3. 逻辑清晰，层层递进
4. 适当使用数据和案例佐证
5. 开头直击主题，结尾有总结升华"""
    },
    "funny": {
        "name": "幽默风格",
        "system": "你是一位搞笑视频博主，擅长用幽默风趣的方式讲述各种话题。你的文案轻松活泼、有梗有料、让人忍不住看完。",
        "instruction": """要求：
1. 语言轻松幽默，适当玩梗
2. 用生动的比喻和夸张手法
3. 节奏明快，不拖沓
4. 在搞笑中传递有价值的信息
5. 开头要有反转或悬念，结尾要有笑点"""
    },
    "emotional": {
        "name": "情感风格",
        "system": "你是一位情感类视频创作者，擅长用真挚的情感打动观众。你的文案有温度、有共鸣、能触动人心。",
        "instruction": """要求：
1. 语言真挚有温度，引发情感共鸣
2. 善用故事化叙述
3. 适当使用修辞手法增强感染力
4. 节奏有起伏，有情绪高潮
5. 开头引发好奇或共情，结尾升华主题"""
    },
    "sales": {
        "name": "带货风格",
        "system": "你是一位顶级带货主播的文案策划，擅长用极具说服力的语言激发购买欲望。你的文案突出卖点、制造紧迫感、引导行动。",
        "instruction": """要求：
1. 突出核心卖点和差异化优势
2. 用场景化描述让观众产生代入感
3. 适当制造紧迫感和稀缺感
4. 用对比和数据增强说服力
5. 开头抛出痛点，结尾强力号召行动"""
    }
}


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
        max_length: int = 500,
        custom_instruction: str = ""
    ) -> Dict:
        """
        基于Markdown内容生成口播文案
        
        参数:
            markdown_content: BiliNote生成的Markdown内容
            style: 文案风格 (professional/funny/emotional/sales)
            max_length: 目标字数
            custom_instruction: 自定义指令（可选）
            
        返回:
            {
                "script": "生成的口播文案",
                "style": "使用的风格",
                "word_count": 实际字数,
                "estimated_duration": 预估朗读时长(秒)
            }
        """
        style_config = STYLE_PROMPTS.get(style, STYLE_PROMPTS["professional"])
        prompt = self._build_prompt(markdown_content, style_config, max_length, custom_instruction)
        
        logger.info(f"开始生成文案: style={style}, max_length={max_length}")
        
        if not self.api_key or self.api_key == "your_minimax_api_key_here":
            logger.warning("MiniMax API Key未配置，使用模拟数据")
            return self._mock_generate(markdown_content, style, max_length)
        
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
                            {"role": "system", "content": style_config["system"]},
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.7,
                        "max_tokens": max_length * 3,
                        "top_p": 0.9
                    }
                )
                response.raise_for_status()
                result = response.json()
                
                script = result["choices"][0]["message"]["content"].strip()
                word_count = len(script)
                # 中文口播约 3-4 字/秒
                estimated_duration = word_count / 3.5
                
                logger.info(f"文案生成完成: {word_count}字, 预估时长: {estimated_duration:.0f}s")
                
                return {
                    "script": script,
                    "style": style,
                    "style_name": style_config["name"],
                    "word_count": word_count,
                    "estimated_duration": round(estimated_duration)
                }
                
            except httpx.HTTPStatusError as e:
                logger.error(f"MiniMax API错误: HTTP {e.response.status_code}")
                raise Exception(f"MiniMax API错误: HTTP {e.response.status_code}")
            except Exception as e:
                logger.error(f"文案生成失败: {str(e)}")
                raise

    async def generate_all_styles(self, markdown_content: str, max_length: int = 500) -> Dict:
        """
        一次性生成所有风格的文案，供用户选择
        
        返回:
            {
                "professional": {...},
                "funny": {...},
                "emotional": {...},
                "sales": {...}
            }
        """
        results = {}
        for style in STYLE_PROMPTS:
            try:
                results[style] = await self.generate_script(markdown_content, style, max_length)
            except Exception as e:
                logger.error(f"生成{style}风格文案失败: {e}")
                results[style] = {"error": str(e)}
        return results

    def _build_prompt(self, content: str, style_config: Dict, max_length: int, custom_instruction: str) -> str:
        """构建Prompt"""
        # 截断过长的内容
        if len(content) > 3000:
            content = content[:3000] + "\n...(内容已截断)"
        
        prompt = f"""请基于以下视频内容，生成一段适合真人出镜口播的视频文案。

{style_config['instruction']}

目标字数：约{max_length}字
格式要求：直接输出文案正文，不要标题、不要分段标记、不要任何说明文字。

"""
        if custom_instruction:
            prompt += f"额外要求：{custom_instruction}\n\n"
        
        prompt += f"原始视频内容：\n{content}"
        
        return prompt

    def _mock_generate(self, content: str, style: str, max_length: int) -> Dict:
        """API Key未配置时的模拟生成"""
        style_config = STYLE_PROMPTS.get(style, STYLE_PROMPTS["professional"])
        
        # 从原始内容提取前几句作为基础
        lines = [l.strip() for l in content.split('\n') if l.strip() and not l.startswith('#')]
        base_text = ' '.join(lines[:5])[:200]
        
        mock_scripts = {
            "professional": f"大家好，今天我们来聊一个非常重要的话题。{base_text}。通过深入分析，我们可以发现其中蕴含的核心逻辑。首先，我们需要理解背景和前因后果。其次，关键数据告诉我们一些不容忽视的事实。最后，让我们总结一下今天的核心要点，希望对大家有所启发。",
            "funny": f"家人们谁懂啊！今天刷到一个视频直接给我整不会了。{base_text}。说实话，看完我整个人都裂开了。但是仔细想想，这里面还真有点东西。你们猜怎么着？最后的结论简直离谱到家了，但偏偏还挺有道理的！",
            "emotional": f"你有没有过这样的时刻，看到一些东西，心里突然被触动了一下？{base_text}。每次想到这些，我都会感慨万千。也许生活就是这样，在不经意间给我们最深的感悟。希望今天的分享，能给你带来一些温暖和力量。",
            "sales": f"等等！先别划走！今天这个内容你一定要看完。{base_text}。我跟你说，了解了这些之后，你的认知会完全不一样。现在知道的人还不多，但趋势已经非常明显了。赶紧点赞收藏，错过真的会后悔！"
        }
        
        script = mock_scripts.get(style, mock_scripts["professional"])
        word_count = len(script)
        
        return {
            "script": script,
            "style": style,
            "style_name": style_config["name"],
            "word_count": word_count,
            "estimated_duration": round(word_count / 3.5),
            "is_mock": True
        }
