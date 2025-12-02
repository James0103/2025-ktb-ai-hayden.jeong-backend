from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from typing import Optional
import controller.db_controller as dbc

db_router = APIRouter()

@db_router.get(
    "/api/all_users",
    tags=["사용자"],
    responses={
        200: {"description": "사용자 목록 조회 성공"},
        404: {"description": "사용자 데이터가 없음"},
    }
)
def get_users():
    return dbc.get_users()


@db_router.get(
    "/api/all_posts",
    tags=["게시글"],
    responses={
        200: {"description": "게시글 목록 조회 성공"},
        404: {"description": "게시글 데이터가 없음"},
    }
)
def get_posts():
    return dbc.get_posts()


@db_router.get(
    "/api/post",
    tags=["게시글"],
    responses={
        200: {"description": "게시글 조회 성공"},
        204: {"description": "게시글 데이터가 없음"},
        404: {"description": "데이터 조회 안됨"},
    }
)
def get_post_detail(post_id: str):
    return dbc.get_post_detail(post_id)


@db_router.get(
    "/api/all_replies",
    tags=["댓글"],
    responses={
        200: {"description": "댓글 목록 조회 성공"},
        404: {"description": "댓글 데이터가 없음"},
    }
)
def get_replies():
    return dbc.get_replies()
