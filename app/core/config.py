
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    PROJECT_NAME: str
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    DATABASE_URI: Optional[PostgresDsn] = None

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return values.get("DATABASE_URI")
    
    GITHUB_REST_API_KEY: str

    @validator("GITHUB_REST_API_KEY", pre=True)
    def assemble_keys(cls, v: Optional[str]) -> Any:
        if isinstance(v, str):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()