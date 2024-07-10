from pydantic import BaseModel
from typing import Optional, List, ForwardRef
from datetime import datetime
from enum import Enum


class User(BaseModel):
    name: str
    email: str
    full_name: Optional[str] = None
    profile_picture: Optional[str] = None
    bio: Optional[str] = None
    friends: Optional[List['User']] = None

User.model_rebuild()

class UserProfile(BaseModel):
    user_id: int
    bio: Optional[str] = None
    profile_picture_url: Optional[str] = None
    birthday: Optional[datetime] = None
    location: Optional[str] = None
    privacy_settings: dict  # This could be more detailed depending on your needs

class Follow(BaseModel):
    follower_id: int
    followed_user_id: int
    created_at: datetime = datetime.now()

class Message(BaseModel):
    sender_id: int
    receiver_id: int
    content: str
    sent_at: datetime

class Notification(BaseModel):
    user_id: int
    content: str
    created_at: datetime

