"""
Database Schemas

Pydantic models that define your MongoDB collections.
Each class name maps to a collection with the lowercase class name.

Examples:
- Lead -> "lead"
- VideoIdea -> "videoidea"
- Script -> "script"
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

class Lead(BaseModel):
    """Inquiries from realtors interested in YouTube growth"""
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Contact email")
    phone: Optional[str] = Field(None, description="Phone number")
    niche: Optional[str] = Field(None, description="Real estate niche (e.g., luxury, first-time buyers)")
    channel_url: Optional[str] = Field(None, description="YouTube channel URL")
    source: Optional[str] = Field("website", description="Lead source tag")

class VideoIdea(BaseModel):
    """Generated video topic ideas with basic metadata"""
    market: str = Field(..., description="City/area focus")
    niche: Optional[str] = Field(None, description="Niche focus")
    title: str = Field(..., description="Video title idea")
    angle: str = Field(..., description="Hook/angle for the video")
    goal: Optional[str] = Field(None, description="Primary goal: awareness | leads | authority")

class Script(BaseModel):
    """Generated script outlines for videos"""
    title: str = Field(..., description="Video title")
    market: str = Field(..., description="City/area focus")
    angle: str = Field(..., description="Hook/angle")
    call_to_action: str = Field(..., description="CTA to drive leads")
    outline: List[str] = Field(..., description="Key beats of the video in order")
