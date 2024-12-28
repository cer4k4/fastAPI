from starlette.responses import JSONResponse
from fastapi import APIRouter
from routes.classes.User import Users
from models import user


router = APIRouter(tags=["user"])

# Create User
@router.post("/user")
async def create_user(user: user.Human):
    user_obj = Users()
    result = user_obj.create_user_db(UserModel=user,creator="Ali karimi")
    return JSONResponse(status_code=result.get("status"),content=result.get("data"))

# Get All User
@router.get("/users")
async def get_all():
    user_obj_db = Users()
    userList = user_obj_db.get_all_db()
    return JSONResponse(status_code=userList.get("status"),content=userList.get("data"))

# Get Single User
@router.get("/user/{user_id}")
async def get_by_user_id(user_id: str):
    user_obj = Users()
    result = user_obj.get_user_db(user_id)
    return JSONResponse(status_code=result.get("status"),content=result.get("data"))

# Update User
@router.put("/user/{user_id}")
async def update_user(user: user.Human,user_id:str):
    user_obj = Users()
    result = user_obj.update_user_db(user,user_id)
    return JSONResponse(status_code=result.get("status"),content=result.get("data"))

# Delete User
@router.delete("/user/{user_id}")
async def delete_user(user_id: str):
    user_obj = Users()
    result = user_obj.delete_user_db(user_id)
    return JSONResponse(status_code=result.get("status"),content=result.get("data"))