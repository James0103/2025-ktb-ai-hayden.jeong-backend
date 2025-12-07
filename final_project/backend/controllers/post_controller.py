from typing import List
from models import PostCreate, PostUpdate, PostResponse
from sqlalchemy.orm import Session
from db.models import PostDB


class PostController:
  """
  게시물(릴레이 스토리) 관리 관련 비즈니스 로직을 담당합니다.
  """

  @staticmethod
  async def get_all_posts(db: Session, skip: int = 0, limit: int = 10) -> List[PostResponse]:
    posts = db.query(PostDB).offset(skip).limit(limit).all()
    post_resp = [PostResponse.from_orm(post) for post in posts]
    return post_resp

  @staticmethod
  async def get_post(db: Session, post_id: int) -> PostResponse:
    post = db.query(PostDB).filter(PostDB.id == post_id).first()
    return PostResponse.from_orm(post)

  @staticmethod
  async def create_post(db: Session, post: PostCreate) -> PostResponse:
    post_info = PostDB(
      title=post.title,
      content=post.content,
      genre=post.genre,
      author=post.nickname,
      user_id=post.user_id,
      next_story_count=post.next_story_count,
    )

    db.add(post_info)
    db.commit()
    db.refresh(post_info)
    return PostResponse.from_orm(post_info)

  @staticmethod
  async def delete_post(db: Session, post_id: int) -> dict:
    post = db.query(PostDB).filter(PostDB.id == post_id).first()

    if not post:
      raise ValueError(f"게시물을 찾을 수 없습니다. (ID: {post_id})")

    db.delete(post)
    db.commit()

    return {"message": "게시물이 삭제되었습니다"}

  @staticmethod
  async def get_user_posts(user_id: int, skip: int = 0, limit: int = 10) -> List[PostResponse]:
      """
      특정 사용자의 모든 게시물을 조회합니다.

      Args:
          user_id (int): 사용자 ID
          skip (int): 건너뛸 개수
          limit (int): 반환할 최대 개수

      Returns:
          List[PostResponse]: 게시물 리스트

      Raises:
          Exception: 데이터베이스 오류
      """
      pass

  @staticmethod
  async def get_remaining_stories(post_id: int) -> dict:
      """
      남은 이야기 개수를 조회합니다.

      Args:
          post_id (int): 게시물 ID

      Returns:
          dict: {
              "remaining_count": int,
              "total_count": int,
              "current_count": int,
              "is_complete": bool
          }

      Raises:
          ValueError: 게시물을 찾을 수 없는 경우
      """
      pass

  @staticmethod
  async def generate_ai_content(post_id: int) -> dict:
      """
      AI를 사용하여 다음 이야기를 생성합니다.

      Args:
          post_id (int): 게시물 ID

      Returns:
          dict: {"generated_content": str}

      Raises:
          ValueError: 게시물을 찾을 수 없는 경우
          Exception: AI 생성 오류
      """
      pass

  @staticmethod
  async def search_posts(keyword: str, skip: int = 0, limit: int = 10) -> List[PostResponse]:
      """
      게시물을 검색합니다 (제목, 내용).

      Args:
          keyword (str): 검색 키워드
          skip (int): 건너뛸 개수
          limit (int): 반환할 최대 개수

      Returns:
          List[PostResponse]: 검색된 게시물 리스트

      Raises:
          Exception: 데이터베이스 오류
      """
      pass
