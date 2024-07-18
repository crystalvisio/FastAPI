from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_name: str
    db_host: str
    db_port:str
    secret_key:str
    algorithm:str
    access_token_expire_mins:int

    class Config:
        env_file = ".env"

settings = Settings()
