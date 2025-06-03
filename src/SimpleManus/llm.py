from utils import Config
from openai import AsyncOpenAI
from logger import logger
config = Config()


class LLM:
    def __init__(self):
        self.chat_client = AsyncOpenAI(
            api_key=config.model_api_key,
            base_url=config.model_base_url
        )
        
    
        