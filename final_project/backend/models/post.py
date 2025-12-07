"""
Post Pydantic models for API validation and serialization
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from .relay_story import RelayStoryResponse


class PostCreate(BaseModel):
  """Model for creating a new post"""
  title: str = Field(..., min_length=1, max_length=500)
  content: str = Field(..., min_length=1)
  genre: str = Field(..., min_length=1)
  nickname: str = Field(..., min_length=1, max_length=50)
  user_id: int
  next_story_count: int = Field(..., ge=4, le=16)


class PostUpdate(BaseModel):
  """Model for updating a post"""
  title: Optional[str] = Field(None, min_length=1, max_length=500)
  content: Optional[str] = Field(None, min_length=1)
  genre: Optional[str] = Field(None, min_length=1)
  author: Optional[str] = Field(None, min_length=1, max_length=50)


class Post(BaseModel):
  """Post model for database"""
  id: Optional[int] = None
  title: str = Field(..., min_length=1, max_length=500)
  content: str = Field(..., min_length=1)
  genre: str = Field(..., min_length=1)
  author: str = Field(..., min_length=1, max_length=50)
  user_id: int
  next_story_count: int = Field(..., ge=4, le=16)
  created_at: datetime = Field(default_factory=datetime.utcnow)
  updated_at: datetime = Field(default_factory=datetime.utcnow)
  comments: List[dict] = Field(default_factory=list)

  class Config:
    from_attributes = True


class PostResponse(BaseModel):
  """Response model for post information"""
  id: int
  title: str
  content: str
  genre: str
  author: str
  user_id: int
  next_story_count: int
  created_at: datetime
  updated_at: datetime
  comments: List["RelayStoryResponse"] = Field(default_factory=list)
  commentCount: int = Field(default=0)

  @property
  def comment_count(self) -> int:
    """Calculate remaining stories count"""
    return len(self.comments)

  @property
  def remaining_stories(self) -> int:
    """Calculate remaining stories count"""
    current_count = len(self.comments)
    return max(0, self.nextStoryCount - current_count)

  class Config:
    from_attributes = True

PostResponse.model_rebuild()

# AI 생성형 모델
class MainStoryGenerate(BaseModel):
  title: str
  content: Optional[str]
  genre: str
  next_story_count: int

class RelayStoryGenerate(BaseModel):
  title: str
  content_story: str
  genre: str
  next_story_count: int
  prev_story_count: int