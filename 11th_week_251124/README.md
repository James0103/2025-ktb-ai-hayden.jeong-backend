### 과제 주제
1. 기존 FastAPI 프로젝트에서 Model 코드의 JSON 반환 대신에 데이터베이스 적용해서 데이터 반환하기

(필수조건) Postman으로 어떠한 요청을 보내던 예외처리가 잘 되어있어야 함

---
### 과제 설명
1. sqlite를 이용해 로컬에서도 호출 가능한 .db파일로 만듬(db/sns.db)
2. .db에 post, user, reply 테이블을 만들어 저장
3. post id로 상세 post 검색 가능

### 실행 방법
- main.py를 python main.py로 실행하면 자동으로 uvicorn이 프로젝트 서빙

### 폴더 구조
📦 11th_week_251124<br>
 ┣ 📂 controller -> db 호출 함수 컨트롤러<br>
 ┣ 📂 db -> 로컬 db 저장 폴더<br>
 ┣ 📂 json_data -> 기존 JSON 파일들<br>
 ┣ 📂 models -> model schema 및 db 호출 함수<br>
 ┣ 📂 router -> api router<br>
 ┣ 📜 main.py -> 메인 파일<br>
 ┣ 📜 make_db.py -> 로컬 DB 생성용 파일<br>
 ┗ 📜 README.md -> 11주차 과제 리드미<br>



