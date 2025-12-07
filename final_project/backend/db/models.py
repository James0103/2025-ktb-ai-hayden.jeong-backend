from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from .config import Base

class UserDB(Base):
  """사용자 테이블"""
  __tablename__ = "users"
  
  id = Column(Integer, primary_key=True, index=True)
  nickname = Column(String(20), unique=True, nullable=False, index=True)
  email = Column(String(255), unique=True, nullable=False, index=True)
  password_hash = Column(String(255), nullable=False)
  profile_photo = Column(Text, nullable=True)
  created_at = Column(DateTime, default=datetime.utcnow)
  updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
  
  # 관계 설정
  # 대상 클래스에 대한 직접적인 참조와 함께 
  posts = relationship("PostDB", back_populates="author_obj", cascade="all, delete-orphan")
  comments = relationship("RelayStoryDB", back_populates="author_obj", cascade="all, delete-orphan")
  
  def __repr__(self):
      return f"<UserDB(id={self.id}, nickname={self.nickname}, email={self.email})>"


class PostDB(Base):
  """게시물 테이블"""
  __tablename__ = "posts"

  id = Column(Integer, primary_key=True, index=True)
  title = Column(String(255), nullable=False)
  content = Column(Text, nullable=False)
  genre = Column(String(50), nullable=False)
  author = Column(String(50), nullable=False)
  user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
  next_story_count = Column(Integer, nullable=False)
  created_at = Column(DateTime, default=datetime.utcnow)
  updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

  # 관계 설정
  author_obj = relationship("UserDB", back_populates="posts")
  comments = relationship("RelayStoryDB", back_populates="post", cascade="all, delete-orphan")
  
  # 복합 인덱스
  __table_args__ = (
    Index('idx_posts_user_created', 'user_id', 'created_at'),
  )
  
  def __repr__(self):
    return f"<PostDB(id={self.id}, title={self.title}, user_id={self.user_id})>"


class RelayStoryDB(Base):
  """릴레이 스토리 (댓글) 테이블"""
  __tablename__ = "relay_stories"
  
  id = Column(Integer, primary_key=True, index=True)
  content = Column(Text, nullable=False)
  author = Column(String(50), nullable=False)
  user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
  post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False, index=True)
  created_at = Column(DateTime, default=datetime.utcnow)
  updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
  
  # 관계 설정
  author_obj = relationship("UserDB", back_populates="comments")
  post = relationship("PostDB", back_populates="comments")
  
  # 복합 인덱스
  __table_args__ = (
    Index('idx_relay_stories_post_created', 'post_id', 'created_at'),
  )
  
  def __repr__(self):
    return f"<RelayStoryDB(id={self.id}, post_id={self.post_id}, user_id={self.user_id})>"