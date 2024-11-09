from typing import Generator
from motor.motor_asyncio import AsyncIOMotorClient
from ..core.config import get_settings
from ..services.user import UserService
from fastapi import Depends

settings = get_settings()

async def get_database() -> Generator:
    client = AsyncIOMotorClient(settings.mongodb_url)
    try:
        yield client
    finally:
        client.close()

async def get_user_service(client: AsyncIOMotorClient = Depends(get_database)) -> UserService:
    return UserService(client, settings.database_name)
