from cryptography.fernet import Fernet
from config.loader import Configer
from datetime import *
import re
import jwt
import random

myConf = Configer()

class UsersManagement:
    def encrypt_password(self, password: str):
        key = myConf.get("user", "secret_key").encode('utf-8')
        fernet_obj = Fernet(key)
        encrypted_password = fernet_obj.encrypt(password.encode())
        return encrypted_password

    def decrypted_password(self, encrypted_password: str):
        key = myConf.get("user", "secret_key").encode('utf-8')
        fernet_obj = Fernet(key)
        decrypted_password = fernet_obj.decrypt(encrypted_password).decode()
        return decrypted_password

    def check_password(self, password, encrypted_password):
        decrypted_password = self.decrypted_password(encrypted_password)
        if password == decrypted_password:
            return True
        else:
            return False

    def generate_secret_key(self):
        key = Fernet.generate_key()
        try:
            key = myConf.get("user", "secret_key") != None
        except:
            key = str(key.decode('utf-8'))
            config.set("user", "secret_key", key)
            config.write(myfile.open("w"))
        return key

    def validate_email(self, email):
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        if re.fullmatch(regex, email):
            return True
        else:
            return False

    def validate_phone_number(self, phone):
        regex = r'^\d{10}$'
        if re.fullmatch(regex, phone):
            return True
        else:
            return False

    def generate_jwt(self, user_id):
        try:
            secret_key = myConf.get("user", "secret_key").encode('utf-8')
            # generate normal_token
            expiration_time = int(datetime.timestamp(datetime.now(
                timezone.utc) + timedelta(minutes=int(myConf.get("user", "token_lifetime"))))*1000)
            payload = {
                "type": "normal_token",
                "user_id": user_id,
                "expire_at": expiration_time
            }
            token = jwt.encode(payload, secret_key, algorithm="HS256")
            # generate refresh_token
            expiration_time = int(datetime.timestamp(datetime.now(
                timezone.utc) + timedelta(minutes=int(myConf.get("user", "refresh_token_lifetime"))))*1000)
            payload = {
                "type": "refresh_token",
                "user_id": user_id,
                "expire_at": expiration_time
            }
            refresh_token = jwt.encode(payload, secret_key, algorithm="HS256")
            return {"token": token, "refresh_token": refresh_token, "expire_at": payload.get("expire_at"), "success": True}
        except:
            return {"token": "", "refresh_token": "", "expire_at": 1, "success": False}

    def decode_jwt(self, token, type="normal_token"):
        try:
            secret_key = myConf.get("user", "secret_key").encode('utf-8')
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
            if payload.get("type") != type:
                return {"success": False}
            return {**payload, "success": True}
        except jwt.ExpiredSignatureError:
            return {"success": False}
        except jwt.InvalidTokenError:
            return {"success": False}

    def generate_otp(self):
        otp = str(random.randint(10000, 99999))
        return otp
