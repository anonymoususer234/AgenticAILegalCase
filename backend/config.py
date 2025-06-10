import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    pinecone_api_key: str = os.getenv("PINECONE_API_KEY", "")
    pinecone_environment: str = os.getenv("PINECONE_ENVIRONMENT", "us-west1-gcp")
    courtlistener_api_key: str = os.getenv("COURTLISTENER_API_KEY", "")
    vector_dimension: int = 1536
    index_name: str = "legal-research"
    
    class Config:
        env_file = ".env"

settings = Settings() 