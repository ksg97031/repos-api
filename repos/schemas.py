from datetime import datetime, timezone
from pydantic import BaseModel, Json

class OrgBase(BaseModel):
    name: str
    repos: Json
    created_at: datetime
    updated_at: datetime

class OrgCreate(BaseModel):
    name: str
    repos: Json
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)

class Org(OrgBase):
    name: str
    repos: Json

    class Config:
        orm_mode = True