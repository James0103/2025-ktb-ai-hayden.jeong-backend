"""
RelayStory Pydantic models for API validation and serialization
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class RelayStoryCreate(BaseModel):
  """Model for creating a new relay story (comment)"""
  content: str = Field(..., min_length=1)
  author: str = Field(..., min_length=1, max_length=50)
  post_id: int
  user_id: int


class RelayStoryUpdate(BaseModel):
  """Model for updating a relay story"""
  content: Optional[str] = Field(None, min_length=1)
  author: Optional[str] = Field(None, min_length=1, max_length=50)


class RelayStory(BaseModel):
  """RelayStory model for database"""
  id: Optional[int] = None
  content: str = Field(..., min_length=1)
  author: str = Field(..., min_length=1, max_length=50)
  user_id: int
  post_id: int
  created_at: datetime = Field(default_factory=datetime.utcnow)
  updated_at: datetime = Field(default_factory=datetime.utcnow)

  class Config:
      from_attributes = True


class RelayStoryResponse(BaseModel):
  """Response model for relay story information"""
  id: int
  content: str
  author: str
  user_id: int
  post_id: int
  created_at: datetime
  updated_at: datetime

  class Config:
    from_attributes = True
