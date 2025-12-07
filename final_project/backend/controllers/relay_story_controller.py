"""
RelayStory Controller
Handles relay story (comment) management business logic
"""

from typing import List
from models import RelayStoryCreate, RelayStoryUpdate, RelayStoryResponse
from sqlalchemy.orm import Session
from db.models import RelayStoryDB, PostDB
from datetime import datetime


class RelayStoryController:
    """
    릴레이 스토리(댓글) 관리 관련 비즈니스 로직을 담당합니다.
    """

    @staticmethod
    async def get_post_comments(post_id: int, skip: int = 0, limit: int = 50) -> List[RelayStoryResponse]:
        """
        특정 게시물의 모든 댓글(릴레이 스토리)을 조회합니다.

        Args:
            post_id (int): 게시물 ID
            skip (int): 건너뛸 개수
            limit (int): 반환할 최대 개수

        Returns:
            List[RelayStoryResponse]: 댓글 리스트

        Raises:
            ValueError: 게시물을 찾을 수 없는 경우
            Exception: 데이터베이스 오류
        """
        pass

    @staticmethod
    async def get_comment(post_id: int, comment_id: int) -> RelayStoryResponse:
        """
        특정 댓글(릴레이 스토리)을 조회합니다.

        Args:
            post_id (int): 게시물 ID
            comment_id (int): 댓글 ID

        Returns:
            RelayStoryResponse: 댓글 정보

        Raises:
            ValueError: 댓글을 찾을 수 없는 경우
            Exception: 데이터베이스 오류
        """
        pass

    @staticmethod
    async def create_comment(db: Session, post_id: int, comment: RelayStoryCreate) -> RelayStoryResponse:
        """
        새로운 댓글(릴레이 스토리)을 생성합니다.

        Args:
            db (Session): 데이터베이스 세션
            post_id (int): 게시물 ID
            comment (RelayStoryCreate): 댓글 정보

        Returns:
            RelayStoryResponse: 생성된 댓글 정보

        Raises:
            ValueError: 게시물을 찾을 수 없거나 이야기가 완성된 경우
            Exception: 데이터베이스 오류
        """
        # 게시물 존재 여부 확인
        post = db.query(PostDB).filter(PostDB.id == post_id).first()
        if not post:
            raise ValueError(f"게시물을 찾을 수 없습니다. (ID: {post_id})")

        # 릴레이 스토리 생성
        relay_story = RelayStoryDB(
            content=comment.content,
            author=comment.author,
            user_id=comment.user_id,
            post_id=post_id,
        )

        db.add(relay_story)
        db.commit()
        db.refresh(relay_story)

        return RelayStoryResponse.from_orm(relay_story)

    @staticmethod
    async def update_comment(post_id: int, comment_id: int, comment: RelayStoryUpdate) -> RelayStoryResponse:
        """
        댓글(릴레이 스토리)을 수정합니다.

        Args:
            post_id (int): 게시물 ID
            comment_id (int): 댓글 ID
            comment (RelayStoryUpdate): 수정할 정보

        Returns:
            RelayStoryResponse: 수정된 댓글 정보

        Raises:
            ValueError: 댓글을 찾을 수 없거나 권한이 없는 경우
            Exception: 데이터베이스 오류
        """
        pass

    @staticmethod
    async def delete_comment(db: Session, post_id: int, comment_id: int) -> dict:
        """
        댓글(릴레이 스토리)을 삭제합니다.

        Args:
            db (Session): 데이터베이스 세션
            post_id (int): 게시물 ID
            comment_id (int): 댓글 ID

        Returns:
            dict: {"message": "댓글이 삭제되었습니다"}

        Raises:
            ValueError: 댓글을 찾을 수 없거나 권한이 없는 경우
            Exception: 데이터베이스 오류
        """
        # 댓글 존재 여부 및 게시물 ID 확인
        relay_story = db.query(RelayStoryDB).filter(
            RelayStoryDB.id == comment_id,
            RelayStoryDB.post_id == post_id
        ).first()

        if not relay_story:
            raise ValueError(f"댓글을 찾을 수 없습니다. (ID: {comment_id})")

        db.delete(relay_story)
        db.commit()

        return {"message": "댓글이 삭제되었습니다"}

    @staticmethod
    async def get_user_comments(user_id: int, skip: int = 0, limit: int = 20) -> List[RelayStoryResponse]:
        """
        특정 사용자가 작성한 모든 댓글을 조회합니다.

        Args:
            user_id (int): 사용자 ID
            skip (int): 건너뛸 개수
            limit (int): 반환할 최대 개수

        Returns:
            List[RelayStoryResponse]: 댓글 리스트

        Raises:
            Exception: 데이터베이스 오류
        """
        pass

    @staticmethod
    async def check_story_complete(post_id: int) -> dict:
        """
        릴레이 스토리의 완성 여부를 확인합니다.

        Args:
            post_id (int): 게시물 ID

        Returns:
            dict: {
                "is_complete": bool,
                "remaining_count": int,
                "current_count": int,
                "total_count": int
            }

        Raises:
            ValueError: 게시물을 찾을 수 없는 경우
        """
        pass

    @staticmethod
    async def can_add_comment(post_id: int) -> dict:
        """
        새로운 댓글을 추가할 수 있는지 확인합니다.

        Args:
            post_id (int): 게시물 ID

        Returns:
            dict: {
                "can_add": bool,
                "reason": str (can_add가 False인 경우만)
            }

        Raises:
            ValueError: 게시물을 찾을 수 없는 경우
        """
        pass

    @staticmethod
    async def get_comments_by_author(post_id: int, author: str) -> List[RelayStoryResponse]:
        """
        특정 게시물에서 특정 작성자의 댓글을 조회합니다.

        Args:
            post_id (int): 게시물 ID
            author (str): 작성자명

        Returns:
            List[RelayStoryResponse]: 댓글 리스트

        Raises:
            ValueError: 게시물을 찾을 수 없는 경우
            Exception: 데이터베이스 오류
        """
        pass
