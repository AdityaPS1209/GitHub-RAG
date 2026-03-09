from backend.core.database import get_database
from backend.models.user import UserModel
from bson import ObjectId

class UserRepository:
    @property
    def collection(self):
        return get_database()["users"]

    async def get_user_by_email(self, email: str) -> dict | None:
        return await self.collection.find_one({"email": email})
        
    async def get_user_by_id(self, user_id: str) -> dict | None:
        return await self.collection.find_one({"_id": ObjectId(user_id)})

    async def create_user(self, user_data: dict) -> dict:
        result = await self.collection.insert_one(user_data)
        user_data["_id"] = result.inserted_id
        return user_data

user_repository = UserRepository()
