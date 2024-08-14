from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_name: str
    db_password: str
    db_user: str
    db_port: str
    db_host: str
    testdb_url:str
    secret_key: str
    algorithm: str
    access_token_expire_mins: int

    class Config:
        env_file = ".env"


settings = Settings()
