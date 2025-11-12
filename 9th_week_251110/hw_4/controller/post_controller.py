from fastapi import HTTPException
import datetime, time
from models.post_model import GetListQuery, PostContentsModel, PostModel
from models.post_model import get_raw_post_db, set_raw_post_db, get_post_with_cursor
from models.user_model import find_user_by_id

# 게시글 목록 조회
def get_posts(query: GetListQuery):
    if query.next is None:
        data = get_post_with_cursor(limit=query.limit_count)
    else:
        data = get_post_with_cursor(cursor_id=query.next, limit=query.limit_count)

    # 다음 페이지 있으면 200, 없으면 204
    if data.page_info.has_next_page:
        return {"message": "success", "data": data}
    else:
        return {"message": "not_exists_next_post_data", "data": data}
    
# 게시글 추가
def make_posts(data: PostContentsModel):
    if data.id is None:
        raise HTTPException(status_code=401, detail="invalid_user_id")
    try:
        int(data.id)
    except:
        raise HTTPException(status_code=401, detail="invalid_user_id")
    
    is_user_exists = find_user_by_id(data.user_id)
    
    if is_user_exists == None:
        raise HTTPException(status_code=401, detail="invalid_user_id")

    if data.contents is None or data.title is None:
        raise HTTPException(status_code=400, detail="invalid_request")
    
    try:
        posts = get_raw_post_db()
        last_post_id_str = posts[-1]["id"].split("post")
        new_post_idx = int(last_post_id_str[-1]) + 1
        new_post_id = f"post{new_post_idx}"

        current_time = datetime.datetime.now()
        current_time_conv = current_time.strftime("%Y-%m-%d %H:%M:%S")
        
        new_post_model = PostModel(
            id=new_post_id,
            title=data.title,
            author=is_user_exists[0].nickname,
            contents=data.contents,
            like_count=0,
            reply_count=0,
            view_count=0,
            last_upload_at=current_time_conv,
            img=data.img
        )

        posts.append(new_post_model.model_dump())
        set_raw_post_db(posts)        
        
        return {"message": "success", "data": None}
    except Exception as e:
        return {"message": "internal_server_error", "data": None}

# 게시글 상세 조회
def get_post_detail(post_id: str) -> PostModel:
    if post_id is None or post_id == "":
        raise HTTPException(status_code=400, detail="invalid_request")
    
    posts = get_raw_post_db()
    post_by_id = next((val for val in posts if val["id"] == post_id), None)

    if post_by_id == None:
        raise HTTPException(status_code=404, detail="no_exist_post_by_id")

    return {"message": "success", "data": post_by_id}

# 게시글 수정
def edit_post(data: PostContentsModel):
    if data.id is None:
        raise HTTPException(status_code=400, detail="invalid_request")
    if data.title is None or data.title.strip() == "":
        raise HTTPException(status_code=400, detail="invalid_request")
    if data.contents is None or data.contents.strip() == "":
        raise HTTPException(status_code=400, detail="invalid_request")
    
    posts = get_raw_post_db()
    post_idx = next((i for i, p in enumerate(posts) if p["id"] == data.id), None)

    if post_idx is None:
        raise HTTPException(status_code=404, detail="no_exist_post_by_id")
   
    posts[post_idx]["title"] = data.title
    posts[post_idx]["contents"] = data.contents
    if data.img is not None:
        posts[post_idx]["img"] = data.img

    set_raw_post_db(posts)

    # 저장 속도 확보를 위한 1초 대기(머신 성능에 따라 필요 X)
    time.sleep(1)

    return {"message": "redirect_to_post"}

# 게시글 삭제
def delete_post(post_id: str):
    if post_id is None or post_id == "":
        raise HTTPException(status_code=400, detail="invalid_request")
    
    posts = get_raw_post_db()
    post_idx = next((i for i, p in enumerate(posts) if p["id"] == post_id), None)
    
    if post_idx == None:
        raise HTTPException(status_code=404, detail="no_exist_post_by_id")
    
    posts.pop(post_idx)

    set_raw_post_db(posts)

    return {"message": "success"}