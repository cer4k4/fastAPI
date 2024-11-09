from typing import Optional, Annotated
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema, **kwargs):
        field_schema.update(type="string")
        return field_schema

class UserInDB(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)
    
    id: Annotated[PyObjectId, Field(default_factory=PyObjectId, alias="_id")]
    email: str
    username: str
    hashed_password: str
    full_name: Optional[str] = None
    disabled: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    def dict(self, *args, **kwargs):
        """Converts the model to a dictionary and handles ObjectId conversion"""
        dict_data = super().model_dump(*args, **kwargs)
        if "_id" in dict_data:
            dict_data["id"] = str(dict_data.pop("_id"))
        return dict_data