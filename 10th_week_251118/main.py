from typing import Dict, Any
from fastapi import FastAPI
from fastapi.responses import JSONResponse, StreamingResponse
from model.model import PromptModel, AnswerModel
import controller.conversation as ct
import uvicorn

app = FastAPI()


@app.post("/generate_text")
def generate_text(user_input: PromptModel) -> AnswerModel:
    '''
    텍스트 생성 API(GPT-2 Small, Pre-trained Only)\n
    *모델이 없을 경우 로컬에 다운로드합니다.\n
    Args:
        user_input (PromptModel): 사용자 입력\n
        -> prompt : 사용자 입력
        -> temperature : 생성 파라미터
    Returns:
        AnswerModel: 모델 답변\n
        -> answer : 생성 답변
        -> process_time : 생성 시간
    '''
    output: AnswerModel = ct.generate_text(user_input)
    return JSONResponse(output.dict(), 200)


@app.get("/")
@app.post("/")
@app.put("/")
@app.patch("/")
@app.options("/")
def index() -> Dict[str, str]:
    return JSONResponse({"msg": "Restricted Access"}, 404)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
