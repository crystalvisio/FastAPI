from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    testdb_url:str
    database_url:str
    secret_key:str
    algorithm:str
    access_token_expire_mins:int

    class Config:
        env_file = ".env"


settings = Settings()
