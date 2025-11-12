from fastapi import APIRouter
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional
import controller as cl
from controller import UserModel, UserLogin, UserProfile, GetListQuery, PostContentsModel, GetReplyQuery, MakeReplyModel

router = APIRouter()

# ============ 사용자 관련 경로 ============

@router.post(
    "/users/signup",
    status_code=201,
    summary="회원가입",
    description="새로운 사용자를 등록합니다.",
    tags=["사용자"],
    responses={
        201: {"description": "회원가입 성공 - user_id 반환"},
        400: {"description": "잘못된 요청 (필수 필드 누락 또는 빈 값)"},
        409: {"description": "이미 사용 중인 이메일"},
    }
)
def create_user(data: UserModel):
    """
    사용자 회원가입

    **필수 입력:**
    - email: 사용자 이메일 (String)
    - password: 사용자 비밀번호 (String)
    - nickname: 사용자 닉네임 (String)

    **선택 입력:**
    - profile_image: 프로필 이미지 URL (String)

    **응답 성공 (201):**
    - message: "register_success"
    - data.user_id: 생성된 사용자 ID
    """
    return cl.create_user(data)

@router.post(
    "/users/signin",
    status_code=200,
    summary="로그인",
    description="사용자 로그인",
    tags=["사용자"],
    responses={
        200: {"description": "로그인 성공 - user_id, nickname, profile_image 반환"},
        401: {"description": "잘못된 이메일 또는 비밀번호"},
        404: {"description": "사용자를 찾을 수 없음"},
    }
)
def read_user(data: UserLogin):
    """
    사용자 로그인

    **필수 입력:**
    - email: 사용자 이메일 (String)
    - password: 사용자 비밀번호 (String)

    **응답 성공 (200):**
    - message: "success"
    - data.user_id: 사용자 ID
    - data.nickname: 사용자 닉네임
    - data.profile_image: 프로필 이미지 URL
    """
    return cl.read_user(data)

@router.patch(
    "/users/edit-profile",
    status_code=200,
    summary="회원정보수정",
    description="사용자 프로필 정보를 수정합니다.",
    tags=["사용자"],
    responses={
        200: {"description": "프로필 수정 성공"},
        400: {"description": "잘못된 요청 (필수 필드 누락 또는 빈 값)"},
        404: {"description": "사용자를 찾을 수 없음"},
        409: {"description": "이미 사용 중인 닉네임"},
    }
)
def edit_profile(data: UserProfile):
    """
    회원정보 수정

    **필수 입력:**
    - user_id: 사용자 ID (String)
    - nickname: 변경할 닉네임 (String)

    **선택 입력:**
    - profile_image: 프로필 이미지 URL (String)

    **응답 성공 (200):**
    - message: "success"
    """
    return cl.edit_profile(data)

# ============ 게시글 관련 경로 ============

@router.get(
    "/posts",
    summary="게시글 목록 조회",
    description="커서 기반 페이지네이션으로 게시글 목록을 조회합니다.",
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
    result = cl.get_posts(query)
    return result

@router.post(
    "/make-post",
    status_code=200,
    summary="게시글 작성",
    description="새로운 게시글을 작성합니다.",
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
    return cl.make_posts(data)

@router.get(
    "/post",
    summary="게시글 상세 조회",
    description="특정 게시글의 상세 정보를 조회합니다.",
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
    return cl.get_post_detail(post_id)

@router.patch(
    "/edit-post",
    status_code=303,
    summary="게시글 수정",
    description="게시글을 수정하고 303 See Other로 게시글 목록으로 리다이렉트합니다.",
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
    result = cl.edit_post(data)
    return RedirectResponse(url=f"/posts?next={data.id}&limit=10", status_code=303)

@router.delete(
    "/post",
    summary="게시글 삭제",
    description="특정 게시글을 삭제합니다.",
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
    return cl.delete_post(post_id)

# ============ 댓글 관련 경로 ============

@router.get(
    "/reply",
    summary="댓글 목록 조회",
    description="특정 게시글의 댓글 목록을 커서 기반 페이지네이션으로 조회합니다.",
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
    result = cl.get_replies(query)
    return result

@router.post(
    "/reply",
    status_code=200,
    summary="댓글 작성",
    description="게시글에 댓글을 작성합니다.",
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
    return cl.make_reply(data)

@router.patch(
    "/reply",
    status_code=200,
    summary="댓글 수정",
    description="댓글을 수정합니다.",
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
    return cl.edit_reply({"reply_id": reply_id, "contents": contents})

@router.delete(
    "/reply",
    status_code=200,
    summary="댓글 삭제",
    description="댓글을 삭제합니다.",
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
    return cl.delete_reply(reply_id)

# 그외 경로 처리
@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"], status_code=401)
def catch_all(path: str):
    """
    그외 모든 경로와 method에 대한 예외처리
    401번 에러를 응답으로 전달
    """
    return {"message": "허가되지 않은 경로입니다", "path": f"/{path}"}