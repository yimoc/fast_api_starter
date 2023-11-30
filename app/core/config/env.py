import os
from typing import Optional
from pydantic_settings import BaseSettings

from app.core.defines import EnvironmentType


class Settings(BaseSettings):
    NAME: str
    PORT: str
    DATABASE_URL: str
    MODEL_CLIENT_SERVER_URL: str
    MODEL_SERVER_WITH_LOCAL: str        # Model service 와 같은 서버에 구동하는지 여부 : True 인 경우 이미지을 path로 전달
    WORKSPACE_PATH: str
    # class Config:
    #     env_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),'.env')


def get_env_type():
    if "ENV_TYPE" in os.environ:
        env_type = os.getenv("ENV_TYPE")
    else:
        env_type = EnvironmentType.PRODUCT
    return env_type