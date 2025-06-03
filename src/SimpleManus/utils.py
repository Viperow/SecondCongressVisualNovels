import yaml
from logger import logger
class Config:
    def __init__(self, config_path="config.yaml"):
        config = self.load_config(config_path)
        
        for key, value in config.items():
            for k, v in value.items():
                setattr(self, f"{key}_{k}", v)
                    
    
    def load_config(self, config_path):
        with open(config_path, "r", encoding='utf8') as f:
            config = yaml.safe_load(f)
        return config

    def __str__(self):
        attrs = vars(self)  # 等同于 self.__dict__
        return '\n'.join(f"{k}: {v}" for k, v in attrs.items())
    
class Memory:
    def __init__(self):
        self.messages = []
    
    def add_message(self, role, content, **kwargs):
        message = {"role": role,
                   "content": content,
                   **kwargs}
        self.messages.append(message)
         
    
if __name__ == "__main__":
    config = Config()
    print(config)
    logger.info("ok")
