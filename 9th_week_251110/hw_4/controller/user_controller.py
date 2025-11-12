from fastapi import HTTPException
from models.user_model import UserModel, UserLogin, UserProfile
from models.user_model import get_raw_user_db, set_raw_user_db
from models.user_model import find_user_by_email, find_user_by_nickname, edit_user_profile


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
    
    exist_email = find_user_by_email(user_info.email)
    if exist_email != None:
        raise HTTPException(status_code=409, detail="email_already_used")
    
    raw_user = get_raw_user_db()
    user_id = int(raw_user[-1]["id"]) + 1
    raw_user.append({
        "id": str(user_id),
        "nickname": user_info.nickname,
        "email": user_info.email,
        "profile_image": user_info.profile_image
    })

    set_raw_user_db(raw_user)
    
    return {'message': 'register_success', 'data': {"user_id": user_id}}

# 로그인
def read_user(user_login: UserLogin):
    # 각 필드가 빈 문자열인지 확인    
    if not user_login.email or user_login.email.strip() == "":
        raise HTTPException(status_code=401, detail="invalid_email_or_pwd")
    
    if not user_login.password or user_login.password.strip() == "":
        raise HTTPException(status_code=401, detail="invalid_email_or_pwd")
    
    user_info = find_user_by_email(user_login.email)
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
    
    is_nickname_exists = find_user_by_nickname(user_info.nickname)

    if is_nickname_exists["status"] == True:
        return edit_user_profile(user_info)
    else:
        raise HTTPException(status_code=409, detail="nickname_already_used")

# 비밀번호 수정(비밀번호는 양쪽의 암호화 부분을 먼저 설계한 뒤 수정 및 비교 코드 작성 예정)