from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class Post(BaseModel):
    title: str
    content: str
    published: bool = False


class CreatePost(Post):
    pass


class CreateUserApiResponse(BaseModel):
    id: int
    email: EmailStr
    createdAt: datetime

    class Config:
        orm_mode = True
        

class PostApiResponse(Post):
    id: int
    createdAt: datetime
    userId: int
    user: CreateUserApiResponse

    class Config:
        orm_mode = True


class PostsWithVotes(Post):
    Post: PostApiResponse
    votes: int

    class Config:
        orm_mode = True


class CreateUser(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class PostVote(BaseModel):
    postId: int
    dir: conint(le=1)
