from datetime import *
from fastapi import Depends
from bson.objectid import ObjectId
from config.loader import Configer
from fastapi.security import HTTPBearer
from tools.users_management import UsersManagement
from db.mongodb_management import MongoDBConnection
from routes.classes.User import Users
users_management_obj = UsersManagement()
security = HTTPBearer()
myConf = Configer()

def get_current_active_user(token: str = Depends(security)):
    try:
        token = dict(token).get("credentials", "")
        payload = users_management_obj.decode_jwt(token=token)
        if payload.get("type") != "normal_token":
            return {
                "message": "توکن صحیح نیست",
                "status": 400,
                "success": False
            }
        if not payload.get("success", True):
            return {
                "message": "توکن صحیح نیست",
                "status": 400,
                "success": False
            }
        if payload.get("expire_at", "") < int(datetime.now(timezone.utc).timestamp()*1000):
            return {
                "message": "توکن منقضی شده است",
                "status": 400,
                "success": False
            }
        print("userID",payload)
        user_db_object = Users()
        user = user_db_object.get_user_db(payload.get("user_id"))
        print("User",user)
        return {**user, "status": 200, "success": True}
        #user_db_connection = MongoDBConnection()
        # users_collection = user_db_connection.db["users"]
        # user_info = users_collection.find_one(
        #     {"_id": ObjectId(payload.get("user_id", "")), "is_deleted": False})
        # if user_info == None:
        #     return {
        #         "message": "کاربری با این شناسه وجود ندارد",
        #         "status": 400,
        #         "success": False
        #     }
        # if not user_info.get("is_active", True):
        #     return {
        #         "message": "کاربر مورد نظر غیر فعال است",
        #         "status": 400,
        #         "success": False
        #     }
        # user_info["id"] = str(user_info["_id"])
        # user_info["group_id"] = user_info.get("group_id")
        # del user_info["_id"]
        # return {**user_info, "status": 200, "success": True}
    except:
        return {
            "message": "توکن صحیح نیست",
            "status": 400,
            "success": False
        }
