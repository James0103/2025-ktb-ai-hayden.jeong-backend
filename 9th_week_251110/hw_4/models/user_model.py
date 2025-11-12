from fastapi import HTTPException
from pydantic import BaseModel
from typing import Optional, Any
import json

# 모델
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
def get_raw_user_db():
    raw_data = ""
    with open("../user.json", 'r') as usr:
        raw_data = json.load(usr)
    return raw_data
# DB 저장
def set_raw_user_db(user_info: list[dict]):
    with open("../user.json", "w") as usr:
        json.dump(user_info, usr, indent=2)
# DB 조회(이메일)
def find_user_by_email(email: str) -> Optional[tuple[UserModel, int]]:
    users = get_raw_user_db()
    user = next((u for u in users if u["email"] == email), None)
    if not user:
        return None
    # password 관련 룰이 정확하지 않기 때문에 일단 공백으로 대체
    if "password" not in user:
        user["password"] = ""
    return (UserModel(**user), user["id"])
# DB 조회(아이디)
def find_user_by_id(id: str) -> Optional[tuple[UserModel, int]]:
    users = get_raw_user_db()
    user = next((u for u in users if u["id"] == id), None)
    if not user:
        return None
    if "password" not in user:
        user["password"] = ""
    return (UserModel(**user), user["id"])
# DB 조회(닉네임)
def find_user_by_nickname(nickname: str) -> dict[str, Any]:
    users = get_raw_user_db()
    user = next((u for u in users if u["nickname"] == nickname), None)
    if not user:
        return {"status": True, "message": "nickname is not exists"}
    else:
        return {"status": False, "message": "someone who used it"}
# DB 일부 수정
def edit_user_profile(profile_data: UserProfile):
    users = get_raw_user_db()
    user_idx = next((i for i, u in enumerate(users) if u["id"] == profile_data.user_id), None)
    if user_idx is None:
        raise HTTPException(status_code=404, detail="user_not_found")

    users[user_idx]["nickname"] = profile_data.nickname
    if profile_data.profile_image != None:
        users[user_idx]["profile_image"] = profile_data.profile_image

    set_raw_user_db(users)

    return {"message": "success"}
