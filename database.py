from fastapi import HTTPException
from typing import overload
from decouple import config
from typing import Union
import motor.motor_asyncio
from auth_utils import AuthJwtCsrf
import asyncio

MONGO_API_KEY = config('MONGO_API_KEY')

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_API_KEY)
client.get_io_loop = asyncio.get_event_loop
database = client.FastAPIUkke
collection_user = database.user
auth = AuthJwtCsrf()


def user_serializer(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "image": user["image"],
    }


async def db_signup(data: dict) -> dict:
    name = data.get('name')
    email = data.get("email")
    password = data.get("password")
    image = ""
    overlap_user = await collection_user.find_one({"email": email})
    # 登録するユーザーが既に存在する場合
    if overlap_user:
        raise HTTPException(status_code=400, detail='Email is already taken')
    if not name:
        raise HTTPException(status_code=400, detail="Please enter your name")
    if not password or len(password) < 6:
        raise HTTPException(status_code=400, detail='password too short')
    user = await collection_user.insert_one({"name": name, "email": email, "password": auth.generate_hashed_pw(password), "image": image})
    new_user = await collection_user.find_one({"_id": user.inserted_id})
    return user_serializer(new_user)


async def db_login(data: dict) -> str:
    email = data.get("email")
    password = data.get("password")
    user = await collection_user.find_one({"email": email})
    if not user or not auth.verify_pw(password, user["password"]):
        raise HTTPException(
            status_code=401, detail='Invalid email or password'
        )
    token = auth.encode_jwt(user['email'])
    return token


async def get_user_info(subject: str) -> Union[dict, bool]:
    user = await collection_user.find_one({"email": subject})
    return user_serializer(user)
