import os
from openai import OpenAI
from typing import List
from loguru import logger
from src.models.schemas import Signal

class Summarizer:
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.client = None
        if self.api_key:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url="https://api.deepseek.com"
            )

    def generate_digest(self, signals: List[Signal]) -> str:
        """
        Use DeepSeek to summarize a list of signals into a digest.
        """
        if not self.client:
            logger.warning("🚫 DeepSeek API Key missing. Returning simple list.")
            return self._fallback_summary(signals)

        if not signals:
            return "📭 过去 24 小时无信号。"

        # Prepare context for LLM
        context_text = ""
        for s in signals:
            context_text += f"- [{s.source_name}] ({s.timestamp.strftime('%H:%M')}): {s.raw_text[:300]}\n"

        prompt = (
            "你是一个专业的金融情报分析师。请阅读以下来自不同博主的推文/新闻片段，为我生成一份简明扼要的【情报日报】。\n\n"
            "要求：\n"
            "1. 按话题分类（如 AI, Crypto, Macro, Tech 等）。\n"
            "2. 重点标注明确的观点（看多/看空/新发布/吐槽）。\n"
            "3. 去除重复和无关废话（如打招呼、广告）。\n"
            "4. 使用中文，风格专业干练，使用 emoji 增加可读性。\n"
            "5. 只要摘要，不要废话开头。\n\n"
            f"情报列表：\n{context_text}"
        )

        try:
            logger.info("🧠 Calling DeepSeek for digest...")
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                stream=False
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"❌ DeepSeek API Failed: {e}")
            return self._fallback_summary(signals)

    def _fallback_summary(self, signals: List[Signal]) -> str:
        """Simple text concatenation if LLM fails"""
        msg = f"📅 *情报日报 (Fallback)*\n---------------------\n"
        grouped = {}
        for sig in signals:
            if sig.source_name not in grouped:
                grouped[sig.source_name] = []
            grouped[sig.source_name].append(sig)
            
        for source, sigs in grouped.items():
            msg += f"👤 *{source}*\n"
            for s in sigs[:2]:
                msg += f"  • {s.raw_text[:50]}...\n"
            msg += "\n"
        return msg
