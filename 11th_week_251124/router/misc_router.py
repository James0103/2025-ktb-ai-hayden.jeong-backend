from fastapi import APIRouter

misc_router = APIRouter()

# 그외 경로 처리
@misc_router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"], status_code=404, operation_id="catch_all_any_method")
def catch_all(path: str):
    """
    그외 모든 경로와 method에 대한 예외처리
    404번 에러를 응답으로 전달
    """
    return {"message": "없는 페이지 입니다", "path": f"/{path}"}