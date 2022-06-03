from pydantic import BaseSettings


class Settings(BaseSettings):
    """Load environment variables to python objects using pydantic."""
    development_env: str = "local"
    production_url: str = "docs"

def get_settings():
    settings = Settings()
    return settings
