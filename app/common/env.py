import os
from typing import Optional
from pydantic_settings import BaseSettings

from app.core.defines import EnvironmentType


class Settings(BaseSettings):
    NAME: str
    PORT: str
    DATABASE_URL: str
    # class Config:
    #     env_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),'.env')


def get_env_type():
    if "ENV_TYPE" in os.environ:
        env_type = os.getenv("ENV_TYPE")
    else:
        env_type = EnvironmentType.PRODUCT
    return env_type