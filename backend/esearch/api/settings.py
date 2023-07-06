from pydantic import BaseModel, BaseSettings, Field


class OAuthConfig(BaseModel):
    client_id: str
    client_secret: str


class AppSettings(BaseSettings):
    oauth_atlassian: OAuthConfig = Field(default=...)
    rwkv_model_path: str = Field(default=...)
    embedder_model_name: str = Field(default=...)
    sqlalchemy_database_url: str = Field(default=...)

    class Config:
        env_prefix = "api_"
        env_nested_delimiter = "__"
