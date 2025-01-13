import math
import copy
import json
from datetime import *
from bson.objectid import ObjectId
from config.configer import Configer
from db.mongodb_management import MongoDBConnection
from models.authorizations.frontend.sections import *

myConf = Configer()


class Permissions:
    def __init__(self):
        self.monogodb_management_obj = MongoDBConnection()
        self.groups_collection = self.monogodb_management_obj.db["groups"]
        self.permissions_collection = self.monogodb_management_obj.db["permissions"]
        self.base_permissions_collection = self.monogodb_management_obj.db["base_permissions"]
    def create_permission(self,name: str, description: str, url: str,config: dict):
        if config.get("authorizations_type") == "frontend":
            if config.get("permission_type") == "section":
                for doc in self.permissions_collection.find({"is_deleted": False, "name":name,"authorizations_type":config.get("authorizations_type")}):
                    return {
                        "status": 400,
                        "message":"قبلا بخشی با این نام ایجاد شده است",
                    }
                result = self.permissions_collection.insert_one({
                    "name": name,
                    "description": description,
                    "url": url,
                    "authorizations_type": config.get("authorizations_type"),
                    "permission_type": config.get("permission_type"),
                    "created_at": int(datetime.now(timezone.utc).timestamp()*1000),
                    "updated_at": int(datetime.now(timezone.utc).timestamp()*1000),
                    "is_deleted": False
                })
                if result.inserted_id:
                    list_of_group_ids = [str(doc["_id"]) for doc in self.groups_collection.find({"is_deleted": False}, {"_id": 1})]
                    for group_id in list_of_group_ids:
                        new_permission_doc = {
                            "group_id": group_id,
                            "base_permission_id": str(result.inserted_id),
                            "is_deleted": False,
                            "created_at": int(datetime.now(timezone.utc).timestamp()*1000),
                            "updated_at": int(datetime.now(timezone.utc).timestamp()*1000),
                            "is_active": True
                        }
                        self.permissions_collection.insert_one(new_permission_doc)
                        return {
                            "status":201,
                            "message": "دسترسی با موفقیت ایجاد شد",
                            "id": str(result.inserted_id)
                        }
                else:
                    return {
                        "status": 400,
                        "message": "ایجاد دسترسی با خطا مواجه شد"
                    }
            elif config.get("permission_type") == "page":
                section = self.base_permissions_collection.find_one({"_id": ObjectId(config.get("section_id")), "is_deleted": False, "permission_type": "section"})
                if not section:
                    return {
                        "status": 404,
                        "message": "بخشی بااین شناسه یافت نشد"
                    }
                existing_page = self.base_permissions_collection.find_one({                    "is_deleted": False,
                    "name": name,
                    "section_id": config.get("section_id"),
                    "authorizations_type": config.get("authorizations_type"),
                    "permission_type": "page"
                })
                if existing_page:
                    return {
                        "status": 400,
                        "message": "صفحه ای با این نام قبلا ساخته شده است"
                    }
                new_page_data = {
                    "name": name,
                    "descriptioon": description,
                    "url": url,
                    "section_id": config.get("section_id"),
                    "authorizations_type": config.get("authorizations_type"),
                    "permission_type": config.get("permission_type"),
                    "created_at": int(datetime.now(timezone.utc).timestamp()*1000),
                    "updated_at": int(datetime.now(timezone.utc).timestamp()*1000),
                    "is_active": True
                }
                new_page = self.base_permissions_collection.insert_one(
                    new_page_data)
                if new_page.inserted_id:
                    list_of_group_ids = [str(doc["_id"]) for doc in self.groups_collection.find(
                        {"is_deleted": False}, {"_id": 1})]
                    for group_id in list_of_group_ids:
                        new_permission_doc = {
                            "group_id": group_id,
                            "base_permission_id": str(new_page.inserted_id),
                            "is_deleted": False,
                            "created_at": int(datetime.now(timezone.utc).timestamp()*1000),
                            "updated_at": int(datetime.now(timezone.utc).timestamp()*1000),
                            "is_active": True
                        }
                        self.permissions_collection.insert_one(
                            new_permission_doc)
                    return {
                        "status": 201,
                        "message": "صفحه با موفقیت ایجاد شد",
                        "id": str(new_page.inserted_id)
                    }
                else:
                    return {
                        "status": 400,
                        "message": "ایجاد صفحه با خطا مواجه شد"
                    }

                    