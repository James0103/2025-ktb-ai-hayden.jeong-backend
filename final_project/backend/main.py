from fastapi import FastAPI
from pathlib import Path
import os
import uvicorn
from routers import user_router, post_router, relay_story_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS 설정 (개발/운영 환경 구분)
def get_allowed_origins():
  """환경에 따라 허용할 origin 목록을 반환합니다."""
  allowed = [
    "http://localhost:5173",  # Vue dev server (로컬 개발)
    "http://localhost:3000",  # Frontend dev server (Docker)
    "*."
  ]

  # 운영 환경에서는 환경 변수로부터 frontend URL 읽기
  frontend_url = os.getenv("VITE_FRONTEND_URL")
  if frontend_url:
    allowed.append(frontend_url)

  return allowed

app.add_middleware(
  CORSMiddleware,
  allow_origins=get_allowed_origins(),
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

# API 라우트
app.include_router(user_router)
app.include_router(post_router)
app.include_router(relay_story_router)

if __name__ == "__main__":
  uvicorn.run("main:app", reload=True)