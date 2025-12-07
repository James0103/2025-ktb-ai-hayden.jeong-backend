"""
Post Router
Handles post management endpoints (CRUD operations for relay stories)
"""

from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from models import PostCreate, PostUpdate, PostResponse, MainStoryGenerate, RelayStoryGenerate
from controllers.post_controller import PostController 
from controllers.ai_story_controller import AIController
from db.session import get_db

router = APIRouter(
  prefix="/api/posts",
  tags=["posts"],
  responses={
    400: {"description": "Bad request"},
    401: {"description": "Unauthorized"},
    403: {"description": "Forbidden"},
    404: {"description": "Not found"},
    500: {"description": "Internal server error"},
  }
)

@router.get("", response_model=List[PostResponse])
async def get_all_posts(db = Depends(get_db), skip: int = 0, limit: int = 10):
  """
  모든 게시물 목록을 조회합니다 (페이지네이션).

  Args:<br>
    skip (int): 건너뛸 개수<br>
    limit (int): 반환할 최대 개수

  Returns:
    List[PostResponse]: 게시물 리스트

  Raises:
    Exception: 데이터베이스 오류
  """
  return await PostController.get_all_posts(db, skip, limit)

@router.get("/{post_id}", response_model=PostResponse)
async def get_post(db = Depends(get_db), post_id: int = 0):
  """
  특정 게시물을 조회합니다 (댓글 포함).

  Args:<br>
      post_id (int): 게시물 ID

  Returns:<br>
      PostResponse: 게시물 정보와 댓글 목록

  Raises:<br>
      ValueError: 게시물을 찾을 수 없는 경우<br>
      Exception: 데이터베이스 오류
  """
  return await PostController.get_post(db, post_id)


@router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate, db = Depends(get_db)):
  """
  새로운 게시물 생성

  - **post**: 게시물 정보 (title, content, author, nextStoryCount)
  - **return**: 생성된 게시물 정보
  """
  return await PostController.create_post(db, post)

# @router.put("/{post_id}", response_model=PostResponse)
# async def update_post(post_id: int, post: PostUpdate):
#     """
#     게시물 수정

#     - **post_id**: 게시물 ID
#     - **post**: 수정할 게시물 정보 (title, content, author)
#     - **return**: 수정된 게시물 정보
#     """
#     pass

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(db = Depends(get_db), post_id: int = 0):
  return await PostController.delete_post(db, post_id)

@router.post("/generate-main-story")
async def generate_main_story(story_info: MainStoryGenerate):
  return await AIController.generate_main_story(story_info)

@router.post("/generate-relay-story")
async def generate_relay_story(story_info: RelayStoryGenerate):
  return await AIController.generate_relay_story(story_info)

