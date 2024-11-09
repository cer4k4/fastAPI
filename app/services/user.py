from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from app.models.user import UserInDB
from app.core.security import get_password_hash
from datetime import datetime

class UserService:
    def __init__(self, client: AsyncIOMotorClient, database_name: str):
        self.db = client[database_name]
        self.collection = self.db.users

    async def create_user(self, user_data: dict) -> UserInDB:
        # Hash the password before storing
        user_data["hashed_password"] = get_password_hash(user_data.pop("password"))
        # Add creation timestamp
        user_data["created_at"] = datetime.utcnow()
        user_data["updated_at"] = user_data["created_at"]
        
        # Create user instance
        user = UserInDB(**user_data)
        
        # Insert into database
        result = await self.collection.insert_one(user.model_dump(by_alias=True))
        
        # Fetch and return the created user
        created_user = await self.collection.find_one({"_id": result.inserted_id})
        return UserInDB.model_validate(created_user)

    async def get_users(self, skip: int = 0, limit: int = 10) -> List[UserInDB]:
        users = await self.collection.find().skip(skip).limit(limit).to_list(length=limit)
        return [UserInDB.model_validate(user) for user in users]

    async def get_user_by_email(self,email: str) -> UserInDB:
        if email == "":
            return UserInDB
        result = await self.collection.find_one_and_update(
            {"_id": ObjectId(user_id)},
            return_document=True
        )
        if result:
            return UserInDB.model_validate(result)
        return None

    async def update_user(self, user_id: str, update_data: dict) -> Optional[UserInDB]:
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        update_data["updated_at"] = datetime.utcnow()
        
        result = await self.collection.find_one_and_update(
            {"_id": ObjectId(user_id)},
            {"$set": update_data},
            return_document=True
        )
        if result:
            return UserInDB.model_validate(result)
        return None
