from dotenv import load_dotenv
import os

# Carrega automaticamente as variáveis do arquivo .env
load_dotenv()

class Config:
    @staticmethod
    def get(key: str):
        return os.getenv(key)
