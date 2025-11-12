from fastapi import HTTPException
from typing import Optional
from pydantic import BaseModel
import json
from models.post_model import PageCursorModel


class ReplyModel(BaseModel):
    id: Optional[str]
    post_id: str
    author: str
    contents: str
    last_upload_at: str

class MakeReplyModel(BaseModel):
    post_id: str
    author: str
    contents: str

class GetReplyQuery(BaseModel):
    post_id: str
    limit_count: int
    next: Optional[str]

class ReplyListModel(BaseModel):
    reply_data: list[ReplyModel]
    page_info: PageCursorModel

# DB 데이터 호출
def get_raw_reply_db() -> list:
    raw_data = ""
    with open("../reply.json", 'r') as rpl:
        raw_data = json.load(rpl)
    return raw_data
# DB 저장
def set_raw_reply_db(data: BaseModel):
    with open("../reply.json", "w") as rpl:
        json.dump(data, rpl, indent=2)

# DB 조회(커서 기반 id)
def get_reply_with_cursor(post_id: str, cursor_id: Optional[str] = None, limit: int = 10) -> ReplyModel:
    replies = get_raw_reply_db()
    replies_by_post_id = [reply for reply in replies if reply["post_id"] == post_id]

    if cursor_id is None:
        start_idx = 0
    else:
        target_idx = next((i for i, p in enumerate(replies_by_post_id) if p["id"] == cursor_id), None)

        if target_idx is None:
            raise HTTPException(status_code=404, detail="empty_reply_data")
        start_idx = target_idx  # 커서 ID 다음부터
    # 남은 데이터가 limit보다 많으면 limit+1, 적으면 모두 가져오기
    remaining_count = len(replies_by_post_id) - start_idx

    if remaining_count > limit:
        raw_replies = replies_by_post_id[start_idx : start_idx + limit + 1]
    else:
        raw_replies = replies_by_post_id[start_idx :]  # 남은 것 모두

    reply_data = [ReplyModel(**value) for value in raw_replies]
    has_next_page = len(reply_data) > limit
    if has_next_page:
        start_cursor = raw_replies[limit]["id"]
        reply_data.pop(-1)
    else:
        start_cursor = None

    page_info = PageCursorModel(
        has_next_page=has_next_page,
        start_cursor=start_cursor
    )
    list_model = ReplyListModel(
        reply_data = reply_data,
        page_info = page_info
    )

    return list_model
