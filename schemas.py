from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class Package(BaseModel):
    id: UUID
    name: str
    version: str
    last_updated: datetime
    dependencies: list


class Contributor(BaseModel):
    id: UUID
    login: str
    github_id: str
    contributions: list[Package]
