from typing import Optional
from pydantic import BaseModel , EmailStr
from datetime import date, datetime
from pydantic.types import conint
from .models import User

#the below schema helps handle the data the user wants to send to the server by restricting the data.
class PostBase(BaseModel): #by extending to BasModel it is using pydantic to define our schema
        # add: int
        title: str
        content: str 
        published: bool = True

class CreatePost(PostBase):
        pass

class UserCreate(BaseModel):
        email : EmailStr
        password : str

class UserResp(BaseModel):
        id : str
        email: EmailStr
        created_at : datetime
        class Config:
                orm_mode = True
        
class UserLogin(BaseModel):
        email : EmailStr
        password : str

#this pydantic model is for sending a response to a user in a restricted way as defined in the schema.
class PostResp(BaseModel):
        title : str
        content : str
        published : bool
        owner_id :int
        created_at : datetime
        owner : UserResp

        '''
        the pydantic class is able to read dict values only ,but in the create post API 
        we are returning a SQL query , so the below class makes it possible for the 
        pydantic class to read the output even if it is not a dict value . 
        '''
        class Config:
                orm_mode = True

# class Post(BaseModel):
#         content : str
#         title : str
#         created_at : datetime
#         published : bool
#         id : int
#         owner_id : int

#         class Config:
#                 orm_mode = True

class PostVote(BaseModel):
        Post : PostResp 
        votes : int

        class Config:
                orm_mode = True


class Token(BaseModel):
        access_token : str
        token_type : str

        class Config:
                orm_mode = True

class TokenData(BaseModel):
        id : str

class VoteData(BaseModel):
        post_id : int
        direct : int