from fastapi import APIRouter
from models.user_model import UserLogin, UserModel, UserProfile
import controller.user_controller as uc

user_router = APIRouter()

@user_router.post(
    "/users/signup",
    status_code=201,
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
    return uc.create_user(data)

@user_router.post(
    "/users/signin",
    status_code=200,
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

    **테스트 데이터**
    - 테스트 이메일 : bob@test.com
    - 테스트 비밀번호 : 현재 비밀번호 검증 부분은 제외되었습니다. 공백 제외 아무 입력이나 하시면 됩니다.
    응답 예시 : 
    {
        "id": "2",
        "nickname": "Bob",
        "email": "bob@test.com",
        "profile_image": "https://i.pravatar.cc/150?img=2"
    },
    """
    return uc.read_user(data)

@user_router.patch(
    "/users/edit-profile",
    status_code=200,
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
    return uc.edit_profile(data)