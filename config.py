from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    MODEL_NAME: str = "gpt-4-turbo-preview"
    TEMPERATURE: float = 0.7
    
    class Config:
        env_file = ".env"