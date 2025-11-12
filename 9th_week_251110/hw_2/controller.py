from fastapi import HTTPException
from typing import Optional, Any
from pydantic import BaseModel
import json, datetime, time

class UserModel(BaseModel):
    email: str
    password: str
    nickname: str
    profile_image: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class UserProfile(BaseModel):
    user_id: str
    nickname: str
    profile_image: Optional[str] = None

# 헬퍼 함수
# 추후 DB 조회로 변경
# DB 데이터 호출
def __get_raw_user_db():
    raw_data = ""
    with open("../user.json", 'r') as usr:
        raw_data = json.load(usr)
    return raw_data
# DB 저장
def __set_raw_user_db(user_info: list[dict]):
    with open("../user.json", "w") as usr:
        json.dump(user_info, usr, indent=2)
# DB 조회(이메일)
def __find_user_by_email(email: str) -> Optional[tuple[UserModel, int]]:
    users = __get_raw_user_db()
    user = next((u for u in users if u["email"] == email), None)
    if not user:
        return None
    # password 관련 룰이 정확하지 않기 때문에 일단 공백으로 대체
    if "password" not in user:
        user["password"] = ""
    return (UserModel(**user), user["id"])
# DB 조회(아이디)
def __find_user_by_id(id: str) -> Optional[tuple[UserModel, int]]:
    users = __get_raw_user_db()
    user = next((u for u in users if u["id"] == id), None)
    if not user:
        return None
    if "password" not in user:
        user["password"] = ""
    return (UserModel(**user), user["id"])
# DB 조회(닉네임)
def __find_user_by_nickname(nickname: str) -> dict[str, Any]:
    users = __get_raw_user_db()
    user = next((u for u in users if u["nickname"] == nickname), None)
    if not user:
        return {"status": True, "message": "nickname is not exists"}
    else:
        return {"status": False, "message": "someone who used it"}
# DB 일부 수정
def __edit_user_profile(profile_data: UserProfile):
    users = __get_raw_user_db()
    user_idx = next((i for i, u in enumerate(users) if u["id"] == profile_data.user_id), None)
    if user_idx is None:
        raise HTTPException(status_code=404, detail="user_not_found")

    users[user_idx]["nickname"] = profile_data.nickname
    if profile_data.profile_image != None:
        users[user_idx]["profile_image"] = profile_data.profile_image

    __set_raw_user_db(users)

    return {"message": "success"}

# 컨트롤러 함수
# 사용자 관련
# 회원가입
def create_user(user_info: UserModel):
    # 각 필드가 빈 문자열인지 확인
    if not user_info.email or user_info.email.strip() == "":
        raise HTTPException(status_code=400, detail="invalid_request")
    
    if not user_info.password or user_info.password.strip() == "":
        raise HTTPException(status_code=400, detail="invalid_request")
    
    if not user_info.nickname or user_info.nickname.strip() == "":
        raise HTTPException(status_code=400, detail="invalid_request")
    
    exist_email = __find_user_by_email(user_info.email)
    if exist_email != None:
        raise HTTPException(status_code=409, detail="email_already_used")
    
    raw_user = __get_raw_user_db()
    user_id = int(raw_user[-1]["id"]) + 1
    raw_user.append({
        "id": str(user_id),
        "nickname": user_info.nickname,
        "email": user_info.email,
        "profile_image": user_info.profile_image
    })

    __set_raw_user_db(raw_user)
    
    return {'message': 'register_success', 'data': {"user_id": user_id}}

# 로그인
def read_user(user_login: UserLogin):
    # 각 필드가 빈 문자열인지 확인    
    if not user_login.email or user_login.email.strip() == "":
        raise HTTPException(status_code=401, detail="invalid_email_or_pwd")
    
    if not user_login.password or user_login.password.strip() == "":
        raise HTTPException(status_code=401, detail="invalid_email_or_pwd")
    
    user_info = __find_user_by_email(user_login.email)
    if user_info == None:
        raise HTTPException(status_code=404, detail="user_not_found")
    else:
        _info = user_info[0]
        _id = user_info[1]
        return {'message': 'success', 'data': {"user_id": _id, "nickname": _info.nickname, "profile_image": _info.profile_image}}

# 회원정보수정
def edit_profile(user_info: UserProfile):
    # 각 필드가 빈 문자열인지 확인    
    if not user_info.nickname or user_info.nickname.strip() == "":
        raise HTTPException(status_code=400, detail="invalid_request")
    
    if not user_info.profile_image or user_info.profile_image.strip() == "":
        raise HTTPException(status_code=400, detail="invalid_request")
    
    is_nickname_exists = __find_user_by_nickname(user_info.nickname)

    if is_nickname_exists["status"] == True:
        return __edit_user_profile(user_info)
    else:
        raise HTTPException(status_code=409, detail="nickname_already_used")

# 비밀번호 수정(비밀번호는 양쪽의 암호화 부분을 먼저 설계한 뒤 수정 및 비교 코드 작성 예정)

############
# 게시글 관련 #
############
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
# DB 데이터 호출
def __get_raw_post_db() -> list:
    raw_data = ""
    with open("../posts.json", 'r') as usr:
        raw_data = json.load(usr)
    return raw_data
# DB 저장
def __set_raw_post_db(data: PostContentsModel):
    with open("../posts.json", "w") as usr:
        json.dump(data, usr, indent=2)

# DB 조회(커서 기반 id)
def __get_post_with_cursor(cursor_id: Optional[str] = None, limit: int = 10) -> PostListModel:
    posts = __get_raw_post_db()

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

# 게시글 목록 조회
def get_posts(query: GetListQuery):
    if query.next is None:
        data = __get_post_with_cursor(limit=query.limit_count)
    else:
        data = __get_post_with_cursor(cursor_id=query.next, limit=query.limit_count)

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
    
    is_user_exists = __find_user_by_id(data.user_id)
    
    if is_user_exists == None:
        raise HTTPException(status_code=401, detail="invalid_user_id")

    if data.contents is None or data.title is None:
        raise HTTPException(status_code=400, detail="invalid_request")
    
    try:
        posts = __get_raw_post_db()
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
        __set_raw_post_db(posts)        
        
        return {"message": "success", "data": None}
    except Exception as e:
        return {"message": "internal_server_error", "data": None}

# 게시글 상세 조회
def get_post_detail(post_id: str) -> PostModel:
    if post_id is None or post_id == "":
        raise HTTPException(status_code=400, detail="invalid_request")
    
    posts = __get_raw_post_db()
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
    
    posts = __get_raw_post_db()
    post_idx = next((i for i, p in enumerate(posts) if p["id"] == data.id), None)

    if post_idx is None:
        raise HTTPException(status_code=404, detail="no_exist_post_by_id")
   
    posts[post_idx]["title"] = data.title
    posts[post_idx]["contents"] = data.contents
    if data.img is not None:
        posts[post_idx]["img"] = data.img

    __set_raw_post_db(posts)

    # 저장 속도 확보를 위한 1초 대기(머신 성능에 따라 필요 X)
    time.sleep(1)

    return {"message": "redirect_to_post"}

# 게시글 삭제
def delete_post(post_id: str):
    if post_id is None or post_id == "":
        raise HTTPException(status_code=400, detail="invalid_request")
    
    posts = __get_raw_post_db()
    post_idx = next((i for i, p in enumerate(posts) if p["id"] == post_id), None)
    
    if post_idx == None:
        raise HTTPException(status_code=404, detail="no_exist_post_by_id")
    
    posts.pop(post_idx)

    __set_raw_post_db(posts)

    return {"message": "success"}

############
# 댓글 관련 #
############
# 헬퍼 함수
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
def __get_raw_reply_db() -> list:
    raw_data = ""
    with open("../reply.json", 'r') as rpl:
        raw_data = json.load(rpl)
    return raw_data
# DB 저장
def __set_raw_reply_db(data: BaseModel):
    with open("../reply.json", "w") as rpl:
        json.dump(data, rpl, indent=2)

# DB 조회(커서 기반 id)
def __get_reply_with_cursor(post_id: str, cursor_id: Optional[str] = None, limit: int = 10) -> ReplyModel:
    replies = __get_raw_reply_db()
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

# 게시글 상세조회(댓글)
def get_replies(query: GetReplyQuery):
    if query.next is None:
        data = __get_reply_with_cursor(post_id=query.post_id, limit=query.limit_count)
    else:
        data = __get_reply_with_cursor(post_id=query.post_id, cursor_id=query.next, limit=query.limit_count)

    # 다음 페이지 있으면 200, 없으면 204
    if data.page_info.has_next_page:
        return {"message": "success", "data": data}
    else:
        return {"message": "not_exists_next_reply_data", "data": data}

# 댓글 작성
def make_reply(data: MakeReplyModel):
    if data.post_id is None or data.post_id is "":
        raise HTTPException(status_code=404, detail="invalid_post_id")
    
    posts = __get_raw_post_db()
    post_idx = next((i for i, p in enumerate(posts) if p["id"] == data.post_id), None)

    if post_idx == None:
        raise HTTPException(status_code=404, detail="invalid_post_id")
    
    if data.contents is None or data.author is None:
        raise HTTPException(status_code=401, detail="invalid_request")
    
    try:
        replies = __get_raw_reply_db()
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
        __set_raw_reply_db(replies)        
        
        return {"message": "success", "data": None}
    except Exception as e:
        return {"message": "internal_server_error", "data": None}

# 댓글 수정
def edit_reply(data: dict[str, str]):
    if data["reply_id"] is None:
        raise HTTPException(status_code=400, detail="invalid_request")
    if data["contents"] is None or data["contents"].strip() == "":
        raise HTTPException(status_code=400, detail="invalid_request")
    
    replies = __get_raw_reply_db()
    reply_idx = next((i for i, p in enumerate(replies) if p["id"] == data["reply_id"]), None)

    if reply_idx is None:
        raise HTTPException(status_code=404, detail="no_exist_reply_by_id")
    
    replies[reply_idx]["contents"] = data["contents"]

    __set_raw_reply_db(replies)

    # 저장 속도 확보를 위한 1초 대기(머신 성능에 따라 필요 X)
    time.sleep(1)

    return {"message": "success"}

# 댓글 삭제
def delete_reply(reply_id: str):
    if reply_id is None or reply_id == "":
        raise HTTPException(status_code=400, detail="invalid_request")
        
    replies = __get_raw_reply_db()
    reply_idx = next((i for i, p in enumerate(replies) if p["id"] == reply_id), None)
    
    if reply_idx == None:
        raise HTTPException(status_code=404, detail="no_exist_post_by_id")
    
    replies.pop(reply_idx)

    __set_raw_reply_db(replies)

    return {"message": "success"}