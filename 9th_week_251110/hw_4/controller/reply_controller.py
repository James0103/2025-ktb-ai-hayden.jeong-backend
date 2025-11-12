from fastapi import HTTPException
import datetime, time
from models.reply_model import GetReplyQuery, MakeReplyModel, ReplyModel
from models.reply_model import get_raw_reply_db, set_raw_reply_db, get_reply_with_cursor
from models.post_model import get_raw_post_db


# 게시글 상세조회(댓글)
def get_replies(query: GetReplyQuery):
    if query.next is None:
        data = get_reply_with_cursor(post_id=query.post_id, limit=query.limit_count)
    else:
        data = get_reply_with_cursor(post_id=query.post_id, cursor_id=query.next, limit=query.limit_count)

    # 다음 페이지 있으면 200, 없으면 204
    if data.page_info.has_next_page:
        return {"message": "success", "data": data}
    else:
        return {"message": "not_exists_next_reply_data", "data": data}

# 댓글 작성
def make_reply(data: MakeReplyModel):
    if data.post_id is None or data.post_id is "":
        raise HTTPException(status_code=404, detail="invalid_post_id")
    
    posts = get_raw_post_db()
    post_idx = next((i for i, p in enumerate(posts) if p["id"] == data.post_id), None)

    if post_idx == None:
        raise HTTPException(status_code=404, detail="invalid_post_id")
    
    if data.contents is None or data.author is None:
        raise HTTPException(status_code=401, detail="invalid_request")
    
    try:
        replies = get_raw_reply_db()
        last_reply_id_str = replies[-1]["id"].split("reply")
        new_reply_idx = int(last_reply_id_str[-1]) + 1
        new_reply_id = f"reply{new_reply_idx}"

        current_time = datetime.datetime.now()
        current_time_conv = current_time.strftime("%Y-%m-%d %H:%M:%S")
        
        new_reply_model = ReplyModel(
            id=new_reply_id,
            post_id=data.post_id,
            author=data.author,
            contents=data.contents,
            last_upload_at=current_time_conv,
        )

        replies.append(new_reply_model.model_dump())
        set_raw_reply_db(replies)        
        
        return {"message": "success", "data": None}
    except Exception as e:
        return {"message": "internal_server_error", "data": None}

# 댓글 수정
def edit_reply(data: dict[str, str]):
    if data["reply_id"] is None:
        raise HTTPException(status_code=400, detail="invalid_request")
    if data["contents"] is None or data["contents"].strip() == "":
        raise HTTPException(status_code=400, detail="invalid_request")
    
    replies = get_raw_reply_db()
    reply_idx = next((i for i, p in enumerate(replies) if p["id"] == data["reply_id"]), None)

    if reply_idx is None:
        raise HTTPException(status_code=404, detail="no_exist_reply_by_id")
    
    replies[reply_idx]["contents"] = data["contents"]

    set_raw_reply_db(replies)

    # 저장 속도 확보를 위한 1초 대기(머신 성능에 따라 필요 X)
    time.sleep(1)

    return {"message": "success"}

# 댓글 삭제
def delete_reply(reply_id: str):
    if reply_id is None or reply_id == "":
        raise HTTPException(status_code=400, detail="invalid_request")
        
    replies = get_raw_reply_db()
    reply_idx = next((i for i, p in enumerate(replies) if p["id"] == reply_id), None)
    
    if reply_idx == None:
        raise HTTPException(status_code=404, detail="no_exist_post_by_id")
    
    replies.pop(reply_idx)

    set_raw_reply_db(replies)

    return {"message": "success"}