from utils import Config
from openai import AsyncOpenAI, OpenAI
from logger import logger
config = Config()


class LLM:
    def __init__(self, use_async: bool = True):
        self.use_async = use_async
        if use_async:
            self.chat_client = AsyncOpenAI(
                api_key=config.model_api_key,
                base_url=config.model_base_url
            )
        else:
            self.chat_client = OpenAI(
                api_key=config.model_api_key,
                base_url=config.model_base_url
            )
        
    
        