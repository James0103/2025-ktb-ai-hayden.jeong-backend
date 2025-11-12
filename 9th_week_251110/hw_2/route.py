from fastapi import APIRouter
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional
import controller as cl
from controller import UserModel, UserLogin, UserProfile, GetListQuery, PostContentsModel, GetReplyQuery, MakeReplyModel

router = APIRouter()

# 사용자 관련 경로
@router.post("/users/signup", status_code=201)
def create_user(data: UserModel):
    return cl.create_user(data)

@router.post("/users/signin", status_code=200)
def read_user(data: UserLogin):
    return cl.read_user(data)

@router.patch("/users/edit-profile", status_code=200)
def edit_profile(data: UserProfile):
    return cl.edit_profile(data)

# 게시물 관련 경로
@router.get("/posts")
def get_posts(limit_count: int = 10, next: Optional[str] = None):
    query = GetListQuery(limit_count=limit_count, next=next)
    result = cl.get_posts(query)
    return result

@router.post("/make-post")
def make_post(data: PostContentsModel):
    return cl.make_posts(data)

@router.get("/post")
def get_post_detail(post_id: str):
    return cl.get_post_detail(post_id)

@router.patch("/edit-post")
def edit_post(data: PostContentsModel):
    result = cl.edit_post(data)
    return RedirectResponse(url=f"/posts?next={data.id}&limit=10", status_code=303)

@router.delete("/post")
def delete_post(post_id: str):
    return cl.delete_post(post_id)

# 댓글 관련 경로
@router.get("/reply")
def get_replies(post_id: str, limit_count: int = 10, next: Optional[str] = None):
    query = GetReplyQuery(post_id=post_id, limit_count=limit_count, next=next)
    result = cl.get_replies(query)
    return result

@router.post("/reply")
def make_reply(data: MakeReplyModel):
    return cl.make_reply(data)

@router.patch("/reply")
def edit_reply(reply_id: str, contents: str):
    return cl.edit_reply({"reply_id": reply_id, "contents": contents})

@router.delete("/reply")
def delete_reply(reply_id: str):
    return cl.delete_reply(reply_id)

# 그외 경로 처리
@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"], status_code=401)
def catch_all(path: str):
    return {"message": "허가되지 않은 경로입니다", "path": f"/{path}"}