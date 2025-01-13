from bson.objectid import ObjectId
from db.mongodb_management import MongoDBConnection
from tools.users_management import UsersManagement
import models.user



class Users:
    def __init__(self):
        self.mongodb_management_obj = MongoDBConnection()
        self.users_collection = self.mongodb_management_obj.db["users"]
        self.users_management_obj = UsersManagement
    def create_user_db(self, UserModel: models.user.Human,creator):
        if self.users_collection.find_one({"email": UserModel.email}) != None:
            return {
                "data":{
                    "message": "این ایمیل قبلا استفاده شده است",
                },
                "status": 400
            }
        dicModel = {
            "name": UserModel.name,
            "family": UserModel.family,
            "age": UserModel.age,
            "email": UserModel.email,
            "gender": UserModel.gender,
            "password":UserModel.password,
            "creator": creator
        }
        dicModel["password"] = self.users_management_obj.encrypt_password(self.users_management_obj,UserModel.password)
        result = self.users_collection.insert_one(dicModel)
        return {
            "data" : {
                "access_token":self.users_management_obj.generate_jwt(self.users_management_obj,result.inserted_id),
                "message": "کاربر با موفقیت ثبت شد"
            },
            "status": 200
        }
    
    def get_user_db(self, Id: str):
        result = self.users_collection.find_one({"_id": ObjectId(Id)})
        if not result:
            return {
                "status": 404,
                "message": "کاربر با این شناسه وجود ندارد",
                "data": {}
            }
        return {
            "data":{
                "name": result["name"],
                "family": result["family"],
                "age": result["age"],
                "sex": result["gender"],
                "email": result["email"],
            },
            "status":200
        }

    def get_all_db(self):
        result = list(self.users_collection.find())
        if not result:
            return {
                "data":{},
                "status": 404,
                "message": "کاربری وجود ندارد"
            }
        data = []
        for r in result:
            userdata = {
                "name" : r.get("name"),
                "family" : r.get("family"),
                "age" : r.get("age"),
                "sex" : r.get("gender"),
                "email": r.get("email")
            }
            data.append(userdata)
        return {
            "data":data,
            "message":"درخواست با موفقیت انجام شد",
            "status":200
        }
        
    def update_user_db(self, UserModel: models.user.Human,userId: str):
        if self.users_collection.find_one({"email": UserModel.email}) != None:
            return {
                "data":{
                    "message": "این ایمیل قبلا استفاده شده است",
                },
                "status": 400
            }
        self.users_collection.update_one({"_id": ObjectId(userId)},{ "$set": {"name": UserModel.name,"family":UserModel.family,"age":UserModel.age,"email":UserModel.email,"gender":UserModel.gender}})
        result = self.get_user_db(userId)
        return result
    
    def delete_user_db(self,user_id:str):
        result = self.users_collection.delete_one({"_id": ObjectId(user_id)})
        return {
            "data": result.acknowledged,
            "status":200
        }
    