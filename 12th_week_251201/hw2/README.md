## 12주차 과제 2번
### 프론트엔드 서빙
바닐라JS를 사용해 기존 FastAPI 프로젝트에서 서빙하는 모델을 사용할 수 있는 웹 프론트엔드 페이지를 만들어 보세요.

---
### 프로젝트 설명
- Backend 폴더에 fastAPI 파일 및 html 서빙을 위한 dist 폴더를 배치했습니다.
- Frontend 폴더에서 웹 페이지를 제작(Vue.js 사용)했습니다.
- Frontend 에서 build 한 결과물을 자동으로 backend 폴더의 dist로 저장합니다.
- Backend 서버를 실행하고 루트 페이지(ex. http://localhost:8000)로 접속하면 과제를 확인하실수 있습니다.

### 프로젝트 구조

📁 12th_week_251201/hw2/<br>
┣ 📁 backend (FastAPI + SQLite)<br>
┃ ┣ main.py (메인 진입점 - SPA 서빙 + API 라우트)<br>
┃ ┣ requirements.txt (Python 의존성)<br>
┃ ┣ 📁 router/<br>
┃ ┃ ┗ db_router.py (API 엔드포인트)<br>
┃ ┣ 📁 controller/<br>
┃ ┃ ┗ db_controller.py (비즈니스 로직)<br>
┃ ┣ 📁 models/<br>
┃ ┃ ┗ db_models.py (Pydantic 모델 + SQLite 쿼리)<br>
┃ ┣ 📁 db/<br>
┃ ┃ ┣ search_db.py (DB에서 조회하는 파이썬 파일)<br>
┃ ┃ ┗ sns.db (SQLite 데이터베이스)<br>
┃ ┗ 📁 dist/ (Frontend 빌드 결과 - 백엔드에서 정적 파일로 서빙)<br>
┃<br>
┗ 📁 frontend (Vue 3 + Vite)<br>
  ┣ package.json (npm 패키지)<br>
  ┣ vite.config.js (Vite 설정)<br>
  ┣ index.html (진입 HTML)<br>
  ┣ 📁 src/<br>
  ┃ ┣ App.vue (루트 컴포넌트)<br>
  ┃ ┣ main.js (Vue 애플리케이션 초기화)<br>
  ┃ ┣ 📁 router/<br>
  ┃ ┃ ┗ index.js (Vue Router 설정)<br>
  ┃ ┗ 📁 stores/<br>
  ┃   ┗ counter.js (Pinia 상태 관리)<br>
  ┗ 📁 public/ (정적 자산)<br>


