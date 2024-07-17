from pydantic import BaseModel
from typing import Optional, List, ForwardRef
from datetime import datetime
from enum import Enum
import social_network.app.models as models
from models import User as User

class PostKind(Enum):
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
class SegmentKind(Enum):
    APPAREL = "apparel"
    FOOTWEAR = "footwear"
    ACCESSORIES = "accessories"
    BEAUTY = "beauty"
    JEWELRY = "jewelry"
    BAGS = "bags"
    EYEWEAR = "eyewear"
    WATCHES = "watches"
    ACTIVEWEAR = "activewear"
    SWIMWEAR = "swimwear"
    OUTERWEAR = "outerwear"
    HOME_DECOR = "home_decor"
    TECH_ACCESSORIES = "tech_accessories"
    PET_FASHION = "pet_fashion"
    KIDS_FASHION = "kids_fashion"
    MENS_FASHION = "mens_fashion"
    WOMENS_FASHION = "womens_fashion"
    UNISEX_FASHION = "unisex_fashion"
    LUXURY_FASHION = "luxury_fashion"
    VINTAGE_FASHION = "vintage_fashion"
    STREETWEAR = "streetwear"
    SUSTAINABLE_FASHION = "sustainable_fashion"
    ETHICAL_FASHION = "ethical_fashion"
    FAST_FASHION = "fast_fashion"
    DESIGNER_FASHION = "designer_fashion"
    HIGH_FASHION = "high_fashion"
    COUTURE = "couture"
    BRIDAL_FASHION = "bridal_fashion"
    FASHION_ACCESSORIES = "fashion_accessories"
    FASHION_JEWELRY = "fashion_jewelry"
    FINE_JEWELRY = "fine_jewelry"
    COSTUME_JEWELRY = "costume_jewelry"
    FASHION_BAGS = "fashion_bags"
    LUXURY_BAGS = "luxury_bags"
    DESIGNER_BAGS = "designer_bags"
    HANDBAGS = "handbags"
    TOTES = "totes"
    CLUTCHES = "clutches"
    CROSSBODY_BAGS = "crossbody_bags"
    SHOULDER_BAGS = "shoulder_bags"
    BACKPACKS = "backpacks"
    MESSENGER_BAGS = "messenger_bags"
    DUFFLE_BAGS = "duffle_bags"
    WEEKENDER_BAGS = "weekender_bags"
    LUGGAGE = "luggage"
    TRAVEL_BAGS = "travel_bags"
    SUITCASES = "suitcases"
    ACCESSORY_BAGS = "accessory_bags"
    COSMETIC_BAGS = "cosmetic_bags"
    TOILETRY_BAGS = "toiletry_bags"
    JEWELRY_BOXES = "jewelry_boxes"
    JEWELRY_ORGANIZERS = "jewelry_organizers"
    JEWELRY_CASES = "jewelry_cases"
    JEWELRY_STORAGE = "jewelry_storage"
    JEWELRY_DISPLAY = "jewelry_display"
    JEWELRY_TRAYS = "jewelry_trays"
    JEWELRY_STANDS = "jewelry_stands"
    JEWELRY_HANGERS = "jewelry_hangers"
    JEWELRY_ARMOIRES = "jewelry_armoires"
    JEWELRY_CHESTS = "jewelry_chests"
    JEWELRY_CABINETS = "jewelry_cabinets"

class PostSegment(BaseModel):
    id: int
    name: str
    kind: SegmentKind
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class Comment(BaseModel):
    id: int
    content: str
    created_at: datetime
    updated_at: datetime
    user: User

class ReactionType(Enum):
    LIKE = "like"
    DISLIKE = "dislike"
    LOVE = "love"
    ANGRY = "angry"
    SAD = "sad"
    HAPPY = "happy"
    WOW = "wow"

class Reaction(BaseModel):
    """
    This class represents a like/dislike on a post or post segments
    """
    id: int
    post : Optional['Post'] = None
    segment : Optional['PostSegment'] = None
    created_at: datetime
    user: User
    reactionType: ReactionType

    class MediaAttachment(BaseModel):
    post_id: int
    media_url: str
    media_type: str  # e.g., "image", "video"
    created_at: datetime

class Tag(BaseModel):
    name: str

class PostTag(BaseModel):
    post_id: int
    tag_id: int

class Hashtag(BaseModel):
    post_id: int
    hashtag: str

class PostContent(BaseException):
    """
    This class represents the content of a post. It can be text, image, or video short
    """
    content: str
    title: str
    created_at: datetime
    updated_at: datetime
    video_url: Optional[str] = None
    image_url: Optional[str] = None

class Post(BaseModel):
    id: int
    post_kind: PostKind
    segments: List[PostSegment]  # This is a list of PostSegment objects
    content: PostContent
    kind: PostKind
    created_at: datetime
    updated_at: datetime
    user: User
    reactions: List[Reaction] = []
    comments: List[Comment] = []
    media_attachments: List[str] = []  # New field for media attachments
    tags: List[Tag] = []
    hashtags: List[Hashtag] = []
