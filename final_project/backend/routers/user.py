"""
User Router
Handles user profile management endpoints
"""
from fastapi import APIRouter, HTTPException, status, Depends, File, UploadFile, Form
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import List
from models import UserCreate, UserLogin, UserResponse
from controllers.user_controller import UserController
from db.session import get_db
from sqlalchemy.orm import Session

router = APIRouter(
  prefix="/api/users",
  tags=["users"],
  responses={
    401: {"description": "Unauthorized"},
    403: {"description": "Forbidden"},
    404: {"description": "Not found"},
    500: {"description": "Internal server error"},
  }
)
@router.post("/sign-up", response_model=UserResponse)
async def sign_up_users(
    nickname: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db = Depends(get_db),
    profile_img_file: UploadFile = File(None)
):
  user_data = UserCreate(nickname=nickname, email=email, password=password)
  return await UserController.sign_up_user(user_data, db, profile_img_file)

@router.post("/sign-in", response_model=UserResponse)
async def sign_in_users(user_info: UserLogin, db = Depends(get_db)):
  try:
    user_data = await UserController.sign_in_user(user_info, db)
    return user_data
  except Exception as e:
    json_data = jsonable_encoder({"message": str(e)})
    return JSONResponse(json_data, status_code=401)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    nickname: str = Form(None),
    password: str = Form(None),
    db = Depends(get_db),
    profile_img_file: UploadFile = File(None)
  ):
  try:
    user_data = await UserController.update_user(user_id, nickname, password, db, profile_img_file)
    return user_data
  except Exception as e:
    json_data = jsonable_encoder({"message": str(e)})
    return JSONResponse(json_data, status_code=400)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    """
    사용자 삭제

    - **user_id**: 사용자 ID
    - **return**: 없음 (204 No Content)
    """
    pass


@router.put("/{user_id}/password")
async def change_password(user_id: int, current_password: str, new_password: str):
    """
    사용자 비밀번호 변경

    - **user_id**: 사용자 ID
    - **current_password**: 현재 비밀번호
    - **new_password**: 새로운 비밀번호
    - **return**: 성공 메시지
    """
    pass
