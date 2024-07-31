from pydantic import BaseModel
from typing import Optional, List, ForwardRef
from datetime import datetime
from enum import Enum

social_network_events = ['user_created', 
                         'user_updated',
                         'user_deleted', 
                         'friend_added', 
                         'friend_removed', 
                         'message_sent', 
                         'notification_sent',
                            'followed_user',
                            'unfollowed_user',
                            'user_blocked',
                            'user_unblocked'
                            'user_reported',
                            'message_unsent',
                            'notification_unsent',
                            'user_profile_updated',
                            'user_profile_deleted',
                            'video_short_created',
                            'video_short_updated',
                            'video_short_deleted',
                            'video_short_viewed',
                            'video_short_liked',
                            'video_short_disliked',
                            'video_short_commented'
                            'video_short_unliked',
                            'video_short_undisliked',
                            'video_short_uncommented',
                            'video_short_shared'
                            'video_short_unshared'
                            'video_short_reported',
                            'video_short_blocked',
                            'video_short_unblocked'
                            'video_short_deleted',
                            'video_short_updated',
                            'video_short_created',
                            'video_short_viewed'
                         ]
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

