from datetime import *
from pydantic import BaseModel
from typing import Optional


class FrontPermissionModel(BaseModel):
    url: str = None
    name: str = None
    permission_type: Optional[str] = None
    page_id: Optional[str] = None
    section_id: Optional[str] = None
    description: Optional[str] = None


class FrontUpdatePermissionModel(BaseModel):
    url: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
