from fastapi import APIRouter
from typing import Optional
from models.reply_model import GetReplyQuery, MakeReplyModel
import controller.reply_controller as rc

reply_router = APIRouter()

@reply_router.get(
    "/reply",
    tags=["댓글"],
    responses={
        200: {"description": "댓글 목록 조회 성공"},
        204: {"description": "댓글이 더 이상 없음"},
        404: {"description": "게시글을 찾을 수 없음"},
    }
)
def get_replies(post_id: str, limit_count: int = 10, next: Optional[str] = None):
    """
    댓글 목록 조회 (커서 기반 페이지네이션)

    **쿼리 파라미터:**
    - post_id: 게시글 ID (String, 필수)
    - limit_count: 한 번에 가져올 댓글 수 (int, 기본값: 10)
    - next: 다음 페이지 커서 ID (String, 선택사항)

    **응답 성공 (200):**
    - message: "success"
    - data.reply_data: 댓글 배열 (id, post_id, author, contents, last_upload_at)
    - data.page_info.has_next_page: 다음 페이지 존재 여부
    - data.page_info.start_cursor: 다음 페이지 커서 ID

    **응답 (204):**
    - message: "not_exists_next_reply_data"
    """
    query = GetReplyQuery(post_id=post_id, limit_count=limit_count, next=next)
    result = rc.get_replies(query)
    return result

@reply_router.post(
    "/reply",
    status_code=200,
    tags=["댓글"],
    responses={
        200: {"description": "댓글 작성 성공"},
        400: {"description": "잘못된 요청 (필수 필드 누락)"},
        404: {"description": "해당 게시글을 찾을 수 없음"},
    }
)
def make_reply(data: MakeReplyModel):
    """
    댓글 작성

    **필수 입력:**
    - post_id: 게시글 ID (String)
    - author: 댓글 작성자 이름 (String)
    - contents: 댓글 내용 (String)

    **응답 성공 (200):**
    - message: "success"
    - data: null
    """
    return rc.make_reply(data)

@reply_router.patch(
    "/reply",
    status_code=200,    
    tags=["댓글"],
    responses={
        200: {"description": "댓글 수정 성공"},
        400: {"description": "잘못된 요청 (필수 필드 누락 또는 빈 값)"},
        404: {"description": "해당 댓글을 찾을 수 없음"},
    }
)
def edit_reply(reply_id: str, contents: str):
    """
    댓글 수정

    **쿼리 파라미터:**
    - reply_id: 댓글 ID (String, 필수)
    - contents: 변경할 댓글 내용 (String, 필수)

    **응답 성공 (200):**
    - message: "success"
    - data: null
    """
    return rc.edit_reply({"reply_id": reply_id, "contents": contents})

@reply_router.delete(
    "/reply",
    status_code=200,
    tags=["댓글"],
    responses={
        200: {"description": "댓글 삭제 성공"},
        400: {"description": "잘못된 요청 (reply_id 누락)"},
        404: {"description": "해당 댓글을 찾을 수 없음"},
    }
)
def delete_reply(reply_id: str):
    """
    댓글 삭제

    **쿼리 파라미터:**
    - reply_id: 삭제할 댓글 ID (String, 필수)

    **응답 성공 (200):**
    - message: "success"
    - data: null
    """
    return rc.delete_reply(reply_id)