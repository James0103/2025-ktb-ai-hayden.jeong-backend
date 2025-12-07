"""
RelayStory Router
Handles relay story (comment) management endpoints
"""

from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from models import RelayStoryCreate, RelayStoryUpdate, RelayStoryResponse
from controllers.relay_story_controller import RelayStoryController
from db.session import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/api/posts",
    tags=["relay_stories"],
    responses={
        400: {"description": "Bad request"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        404: {"description": "Not found"},
        500: {"description": "Internal server error"},
    }
)

@router.post("/{post_id}/comments", response_model=RelayStoryResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(post_id: int, comment: RelayStoryCreate, db: Session = Depends(get_db)):
  """
  새로운 댓글(릴레이 스토리) 생성

  - **post_id**: 게시물 ID
  - **comment**: 댓글 정보 (content, author, post_id, user_id)
  - **return**: 생성된 댓글 정보
  """
  return await RelayStoryController.create_comment(db, post_id, comment)


@router.put("/{post_id}/comments/{comment_id}", response_model=RelayStoryResponse)
async def update_comment(post_id: int, comment_id: int, comment: RelayStoryUpdate):
  """
  댓글(릴레이 스토리) 수정

  - **post_id**: 게시물 ID
  - **comment_id**: 댓글 ID
  - **comment**: 수정할 댓글 정보 (content, author)
  - **return**: 수정된 댓글 정보
  """
  pass


@router.delete("/{post_id}/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(post_id: int, comment_id: int, db: Session = Depends(get_db)):
  """
  댓글(릴레이 스토리) 삭제

  - **post_id**: 게시물 ID
  - **comment_id**: 댓글 ID
  - **return**: 없음 (204 No Content)
  """
  try:
    await RelayStoryController.delete_comment(db, post_id, comment_id)
  except ValueError as e:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
