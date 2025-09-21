from pydantic import BaseModel

class UserModel(BaseModel):
    user_id: int
    username: str
    email: str
    is_active: bool
    age: int
    balance: float
    tags: list[str]
    metadata: dict[str, str]