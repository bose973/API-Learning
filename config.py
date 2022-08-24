from pydantic import BaseSettings

#this class is created to perform the required validations that the env variables are set
class Settings(BaseSettings):
        database_port : str
        database_hostname : str
        database_password : str
        database_name : str
        database_username : str
        secret_key : str
        algorithm : str
        access_token_expire_minutes : int
        
        class Config:
                env_file = ".env"
        

settings = Settings()
