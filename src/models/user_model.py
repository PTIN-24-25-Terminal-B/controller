from pydantic import BaseModel
from typing import Optional
from enum import Enum
import redis
import json

def get_redis_connection():
    return redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)


class UserState(Enum):
    IDLE = "idle"
    WAITING = "waiting"
    TRAVELING = "traveling"

class User(BaseModel):
    id: str
    state: UserState = UserState.IDLE
    carId: Optional[str] = None
    origin: Optional[tuple[int, int ]] = None
    destination: Optional[tuple[int, int ]] = None

    def __str__(self):
        return json.dumps(self.model_dump(mode="json"), indent=2)

    @staticmethod
    def write_user(user: "User"):
        redis_conn = get_redis_connection()
        key = f"user:{user.id}"
        value = user.model_dump_json(indent=2)
        redis_conn.set(key, value)
        return user
    
    @staticmethod
    def read_user(user_id: str):
        redis_conn = get_redis_connection()
        user_json = redis_conn.get(f"user:{user_id}")
        if user_json:
            return User.model_validate_json(user_json)
        else:
            return None