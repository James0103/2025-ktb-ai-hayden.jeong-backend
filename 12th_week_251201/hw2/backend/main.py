from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import os
import uvicorn
from router.db_router import db_router

app = FastAPI()
vue_dist_path = "./dist"

# 개발 중 CORS 우회
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vue dev server 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우트
app.include_router(db_router)

# 정적 파일 서빙 (CSS, JS 등)
app.mount("/assets", StaticFiles(directory=f"{vue_dist_path}/assets"), name="assets")

# favicon 등 루트의 정적 파일들
@app.get("/favicon.ico")
async def favicon():
    return FileResponse(f"{vue_dist_path}/favicon.ico")

# SPA를 위한 catch-all 라우트 (모든 경로를 index.html로)
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    return FileResponse(f"{vue_dist_path}/index.html")

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)