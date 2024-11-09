from fastapi import FastAPI
from app.api.v1.endpoints import user
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(title="User CRUD API")

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(settings.mongodb_url)
    app.mongodb = app.mongodb_client[settings.database_name]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(user.router, prefix="/api/v1/users", tags=["users"])