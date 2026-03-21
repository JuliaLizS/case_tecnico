# Schema

from pydantic import BaseModel, EmailStr

class CreateUserRequest(BaseModel):
    name: str
    email: EmailStr
    description: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    description: str

class SearchUserRequest(BaseModel):
    query: str
    top_k: int = 5

class ListUsersRequest(BaseModel):
    limit: int = 10
    offset: int = 0
