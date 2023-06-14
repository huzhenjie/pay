from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    mysql_link: str

    class Config:
        server_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        env_file = ".env.local" if os.path.exists(server_path + '/.env.local') else '.env'
