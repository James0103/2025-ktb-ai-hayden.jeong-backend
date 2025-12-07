"""
User Controller
Handles user profile management business logic
"""

from typing import List
# DB 연결 부분
from sqlalchemy.orm import Session
from fastapi import Depends, UploadFile
from datetime import datetime
from db.models import UserDB 
from db.session import get_db 
from models import UserCreate, UserLogin, UserResponse  
from passlib.context import CryptContext
from services.bucket_service import S3Service

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserController:
  """
  사용자 프로필 관리 관련 비즈니스 로직을 담당합니다.
  """
  @staticmethod
  async def sign_up_user(user_data: UserCreate, db: Session, profile_img_file: UploadFile = None) -> UserResponse:
    """
    사용자 회원가입

    Returns:
        List[UserResponse]: 사용자 리스트

    Raises:
        Exception: 데이터베이스 오류
    """
    hashed_password = pwd_context.hash(user_data.password)
    
    profile_img_url = None
    if profile_img_file:
      profile_img_url = await S3Service.upload_profile_photo(profile_img_file)

    user_info = UserDB(
      nickname=user_data.nickname,
      email=user_data.email,
      password_hash=hashed_password,
      profile_photo=profile_img_url,
      created_at=datetime.utcnow(),
      updated_at=datetime.utcnow()
    )

    db.add(user_info)
    db.commit()
    db.refresh(user_info)
    return UserResponse.from_orm(user_info)
      
  @staticmethod
  async def sign_in_user(user_info: UserLogin, db: Session) -> UserResponse:
    """
    사용자 로그인

    Args:
        email (str): 사용자 이메일
        password (str): 사용자 비밀번호
        db (Session): 데이터베이스 세션

    Returns:
        UserResponse: 사용자 정보

    Raises:
        ValueError: 이메일이 없거나 비밀번호가 일치하지 않는 경우
    """
    user = db.query(UserDB).filter(UserDB.email == user_info.email).first()
    if not user:
        raise ValueError("이메일 또는 비밀번호를 확인해주세요")

    if not pwd_context.verify(user_info.password, user.password_hash):
        raise ValueError("이메일 또는 비밀번호를 확인해주세요")

    return UserResponse.from_orm(user)

  @staticmethod
  async def update_user(user_id: int, nickname: str, password: str, db: Session, profile_img_file: UploadFile = None) -> UserResponse:
    """
    사용자 정보 수정.

    Args:
        user_id (int): 사용자 ID
        user (UserUpdate): 수정할 정보 (nickname, password, photo)

    Returns:
        UserResponse: 수정된 사용자 정보

    Raises:
        ValueError: 사용자를 찾을 수 없는 경우
        Exception: 데이터베이스 오류
    """
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
      raise ValueError(f"ID '{user_id}'에 해당하는 사용자를 찾을 수 없습니다.")
    
    if nickname is not None:
      user.nickname = nickname
    if password is not None:
      user.password_hash = pwd_context.hash(password)
    if profile_img_file:
      profile_img_url = await S3Service.upload_profile_photo(profile_img_file)
      user.profile_photo = profile_img_url

    user.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(user)
    return UserResponse.from_orm(user)

#   @staticmethod
#   async def get_user_by_email(email: str, db: Session) -> UserResponse:
#       """
#       이메일로 사용자를 조회합니다.

#       Args:
#           email (str): 사용자 이메일
#           db (Session): 데이터베이스 세션

#       Returns:
#           UserResponse: 사용자 정보

#       Raises:
#           ValueError: 사용자를 찾을 수 없는 경우
#       """
#       user = db.query(UserDB).filter(UserDB.email == email).first()
#       if not user:
#           raise ValueError(f"이메일 '{email}'에 해당하는 사용자를 찾을 수 없습니다.")
#       return UserResponse.from_orm(user)

#   @staticmethod
#   async def check_email_exists(email: str, db: Session) -> bool:
#       """
#       이메일의 존재 여부를 확인합니다.

#       Args:
#           email (str): 확인할 이메일
#           db (Session): 데이터베이스 세션

#       Returns:
#           bool: 이메일이 존재하면 True, 없으면 False
#       """
#       user = db.query(UserDB).filter(UserDB.email == email).first()
#       return user is not None

#   @staticmethod
#   async def check_nickname_exists(nickname: str, db: Session) -> bool:
#       """
#       닉네임의 존재 여부를 확인합니다.

#       Args:
#           nickname (str): 확인할 닉네임
#           db (Session): 데이터베이스 세션

#       Returns:
#           bool: 닉네임이 존재하면 True, 없으면 False
#       """
#       user = db.query(UserDB).filter(UserDB.nickname == nickname).first()
#       return user is not None
