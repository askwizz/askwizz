from typing import Annotated, Literal

import dotenv
from fastapi import Depends
from pydantic import BaseModel, BaseSettings, Field


class OAuthConfig(BaseModel):
    client_id: str
    client_secret: str


class AppSettings(BaseSettings):
    oauth_atlassian: OAuthConfig = Field(default=...)
    rwkv_model_path: str = Field(default=...)
    embedder_model_name: str = Field(default=...)
    sqlalchemy_database_url: str = Field(default=...)
    auth_userdata_override_id: str = Field(default=...)
    environment: Literal["prod"] | Literal["dev"] = Field(default=...)

    class Config:
        env_prefix = "api_"
        env_nested_delimiter = "__"


def get_settings() -> AppSettings:
    dotenv.load_dotenv()
    return AppSettings()


def get_is_production(
    settings: Annotated[AppSettings, Depends(get_settings)],
) -> bool:
    return settings.environment == "prod"
