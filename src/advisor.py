import os
import sqlite3
from openai import OpenAI

# ==========================================
# 极其关键的底层补丁 (Monkey Patch)
# 解决 MacOS Python3.9 下由于 Mem0 的多线程并发导致 Qdrant 本地 SQLite 报错的问题
# ==========================================
original_connect = sqlite3.connect
def patched_connect(*args, **kwargs):
    kwargs['check_same_thread'] = False
    return original_connect(*args, **kwargs)
sqlite3.connect = patched_connect

from mem0 import Memory

class FinancialAdvisor:
    def __init__(self):
        # 从环境变量获取智谱 API Key
        ZHIPU_API_KEY = os.environ.get("ZHIPU_API_KEY")
        if not ZHIPU_API_KEY:
            raise ValueError("未找到 ZHIPU_API_KEY，请确保在运行时输入了正确的 Key！")

        ZHIPU_BASE_URL = "https://open.bigmodel.cn/api/paas/v4/"
        
        config = {
            "vector_store": {
                "provider": "qdrant",
                "config": {
                    "collection_name": "mem0_zhipu_v2",
                    "embedding_model_dims": 1024 
                }
            },
            "llm": {
                "provider": "openai",
                "config": {
                    "model": "glm-4-flash", 
                    "api_key": ZHIPU_API_KEY,
                    "openai_base_url": ZHIPU_BASE_URL
                }
            },
            "embedder": {
                "provider": "openai",
                "config": {
                    "model": "embedding-2", 
                    "api_key": ZHIPU_API_KEY,
                    "openai_base_url": ZHIPU_BASE_URL
                }
            }
        }
        # 初始化 Mem0 记忆层
        self.memory = Memory.from_config(config)
        
        # 初始化用于最终对话生成的客户端
        self.client = OpenAI(
            api_key=ZHIPU_API_KEY,
            base_url=ZHIPU_BASE_URL
        )
        
    def chat_and_remember(self, user_id: str, message: str):
        """
        接收用户的日常沟通，利用 Mem0 自动提取并长久保存金融偏好/状况
        """
        print(f"[系统日志] 正在分析并提取用户 '{user_id}' 的特征记忆...")
        self.memory.add(message, user_id=user_id)
        print("[系统日志] 记忆已成功更新！")

    def get_personalized_advice(self, user_id: str, query: str) -> str:
        """
        根据用户当前提问，召回相关记忆，利用 LLM 生成个性化投资建议
        """
        print(f"\n[系统日志] 正在检索用户 '{user_id}' 的专属金融记忆...")
        # 1. 记忆召回 (RAG)
        raw_memories = self.memory.search(query, user_id=user_id)
        
        # 【关键修复】Mem0 1.0 版本 search 返回的是字典结构 {"results": [...]}
        relevant_memories = []
        if isinstance(raw_memories, dict) and "results" in raw_memories:
            relevant_memories = raw_memories["results"]
        elif isinstance(raw_memories, list):
            relevant_memories = raw_memories

        # 将记忆拼接为字符串
        memory_context = ""
        if relevant_memories:
            memories_list = [mem.get("memory", "") for mem in relevant_memories if isinstance(mem, dict)]
            memory_context = "\n".join(memories_list)
            print(f"[系统日志] 成功召回以下记忆特征：\n{memory_context}\n")
        else:
            print("[系统日志] 未检索到相关的历史偏好记忆，将进行通用回复。\n")

        # 2. 构建 Prompt
        system_prompt = f"""你是一位专业的私人财富管理顾问。
以下是系统从记忆库中提取到的关于该用户的核心特征/历史偏好：
<user_memory>
{memory_context}
</user_memory>

请务必将上述特征融入你的回答中。针对用户的提问给出极其专业、严谨且符合其个人特征的投资建议。
"""
        print("[系统日志] 正在生成个性化投资方案...")
        response = self.client.chat.completions.create(
            model="glm-4-flash",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ]
        )
        
        return response.choices[0].message.content