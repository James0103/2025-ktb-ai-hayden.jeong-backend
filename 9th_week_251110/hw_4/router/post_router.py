from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from models.post_model import GetListQuery, PostContentsModel
from typing import Optional
import controller.post_controller as pc

post_router = APIRouter()

@post_router.get(
    "/posts",
    tags=["게시글"],
    responses={
        200: {"description": "게시글 목록 조회 성공 (다음 페이지 있음)"},
        204: {"description": "게시글이 더 이상 없음 (마지막 페이지)"},
        404: {"description": "게시글 데이터가 없음"},
    }
)
def get_posts(limit_count: int = 10, next: Optional[str] = None):
    """
    게시글 목록 조회 (커서 기반 페이지네이션)

    **쿼리 파라미터:**
    - limit_count: 한 번에 가져올 게시글 수 (int, 기본값: 10)
    - next: 다음 페이지 커서 ID (String, 선택사항)

    **응답 성공 (200):**
    - message: "success"
    - data.post_data: 게시글 배열 (id, title, author, contents, like_count, reply_count, view_count, last_upload_at, img)
    - data.page_info.has_next_page: 다음 페이지 존재 여부
    - data.page_info.start_cursor: 다음 페이지 커서 ID (없으면 null)

    **응답 (204):**
    - message: "not_exists_next_post_data"
    """
    query = GetListQuery(limit_count=limit_count, next=next)
    result = pc.get_posts(query)
    return result

@post_router.post(
    "/make-post",
    status_code=200,
    tags=["게시글"],
    responses={
        200: {"description": "게시글 작성 성공"},
        400: {"description": "잘못된 요청 (필수 필드 누락)"},
        401: {"description": "유효하지 않은 사용자 ID"},
    }
)
def make_post(data: PostContentsModel):
    """
    게시글 작성

    **필수 입력:**
    - id: 작성자 사용자 ID (String)
    - title: 게시글 제목 (String)
    - contents: 게시글 내용 (String)

    **선택 입력:**
    - img: 게시글 이미지 URL (String)

    **응답 성공 (200):**
    - message: "success"
    - data: null
    """
    return pc.make_posts(data)

@post_router.get(
    "/post",
    tags=["게시글"],
    responses={
        200: {"description": "게시글 조회 성공"},
        400: {"description": "잘못된 요청 (post_id 누락)"},
        404: {"description": "해당 게시글을 찾을 수 없음"},
    }
)
def get_post_detail(post_id: str):
    """
    게시글 상세 조회

    **쿼리 파라미터:**
    - post_id: 조회할 게시글 ID (String, 필수)

    **응답 성공 (200):**
    - message: "success"
    - data: 게시글 정보 (id, title, author, contents, like_count, reply_count, view_count, last_upload_at, img)
    """
    return pc.get_post_detail(post_id)

@post_router.patch(
    "/edit-post",
    status_code=303,
    tags=["게시글"],
    responses={
        303: {"description": "게시글 수정 성공 - Location 헤더에 리다이렉트 URL 포함"},
        400: {"description": "잘못된 요청 (필수 필드 누락)"},
        404: {"description": "해당 게시글을 찾을 수 없음"},
    }
)
def edit_post(data: PostContentsModel):
    """
    게시글 수정

    **필수 입력:**
    - id: 게시글 ID (String)
    - title: 변경할 게시글 제목 (String)
    - contents: 변경할 게시글 내용 (String)

    **선택 입력:**
    - img: 게시글 이미지 URL (String)

    **응답 성공 (303):**
    - HTTP Header: Location: /posts?next={post_id}&limit=10
    - message: "redirect_to_post"
    """
    result = pc.edit_post(data)
    return RedirectResponse(url=f"/posts?next={data.id}&limit=10", status_code=303)

@post_router.delete(
    "/post",
    tags=["게시글"],
    responses={
        200: {"description": "게시글 삭제 성공"},
        400: {"description": "잘못된 요청 (post_id 누락)"},
        404: {"description": "해당 게시글을 찾을 수 없음"},
    }
)
def delete_post(post_id: str):
    """
    게시글 삭제

    **쿼리 파라미터:**
    - post_id: 삭제할 게시글 ID (String, 필수)

    **응답 성공 (200):**
    - message: "success"
    - data: null
    """
    return pc.delete_post(post_id)