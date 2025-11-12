from fastapi import HTTPException
from typing import Optional
from pydantic import BaseModel
import json
from models.user_model import find_user_by_id

# 모델
class PostModel(BaseModel):
    id: str
    title: str
    author: str
    contents: Optional[str]
    like_count: int
    reply_count: int
    view_count: int
    last_upload_at: str
    img: Optional[str]

class PageCursorModel(BaseModel):
    has_next_page: bool
    start_cursor: Optional[str]

class PostListModel(BaseModel):
    post_data: list[PostModel]
    page_info: PageCursorModel

class GetListQuery(BaseModel):
    limit_count: int
    next: Optional[str]

class PostContentsModel(BaseModel):
    id: str
    title: str
    contents: str
    img: Optional[str]

# 헬퍼 함수
# 헬퍼 함수
# DB 데이터 호출
def get_raw_post_db() -> list:
    raw_data = ""
    with open("../posts.json", 'r') as usr:
        raw_data = json.load(usr)
    return raw_data
# DB 저장
def set_raw_post_db(data: PostContentsModel):
    with open("../posts.json", "w") as usr:
        json.dump(data, usr, indent=2)

# DB 조회(커서 기반 id)
def get_post_with_cursor(cursor_id: Optional[str] = None, limit: int = 10) -> PostListModel:
    posts = get_raw_post_db()

    if cursor_id is None:
        # raw_posts = posts[:limit + 1]
        start_idx = 0
    else:
        target_idx = next((i for i, p in enumerate(posts) if p["id"] == cursor_id), None)

        if target_idx is None:
            raise HTTPException(status_code=404, detail="empty_post_data")
        start_idx = target_idx  # 커서 ID 다음부터
    # 남은 데이터가 limit보다 많으면 limit+1, 적으면 모두 가져오기
    remaining_count = len(posts) - start_idx

    if remaining_count > limit:
        raw_posts = posts[start_idx : start_idx + limit + 1]
    else:
        raw_posts = posts[start_idx :]  # 남은 것 모두

    post_data = [PostModel(**value) for value in raw_posts]
    has_next_page = len(post_data) > limit
    start_cursor = raw_posts[limit]["id"] if has_next_page else None

    page_info = PageCursorModel(
        has_next_page=has_next_page,
        start_cursor=start_cursor
    )
    list_model = PostListModel(
        post_data = post_data,
        page_info = page_info
    )

    return list_model