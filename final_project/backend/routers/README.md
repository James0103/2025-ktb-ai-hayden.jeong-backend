# API Routers

FastAPI 라우터 정의 파일들입니다. 각 라우터는 특정 기능 영역의 API 엔드포인트를 정의합니다.

## 파일 구조

```
routers/
├── __init__.py           # 라우터 내보내기
├── auth.py              # 인증 관련 엔드포인트 (가입, 로그인)
├── user.py              # 사용자 관리 엔드포인트 (CRUD)
├── post.py              # 게시물 관리 엔드포인트 (CRUD)
├── relay_story.py       # 릴레이 스토리 댓글 엔드포인트 (CRUD)
└── README.md            # 이 파일
```

---

## 1. Auth Router (`auth.py`)

### 역할
- 사용자 회원가입
- 사용자 로그인
- JWT 토큰 발급

### 엔드포인트

#### POST /api/auth/signup
회원가입

**요청**:
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**응답** (201 Created):
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "bio": "",
  "profilePhoto": null,
  "createdAt": "2024-01-01T12:00:00",
  "updatedAt": "2024-01-01T12:00:00"
}
```

#### POST /api/auth/login
로그인

**요청**:
```json
{
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**응답** (200 OK):
```json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "bio": "",
    "profilePhoto": null,
    "createdAt": "2024-01-01T12:00:00",
    "updatedAt": "2024-01-01T12:00:00"
  },
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

---

## 2. User Router (`user.py`)

### 역할
- 사용자 정보 조회
- 사용자 프로필 수정
- 사용자 삭제
- 비밀번호 변경

### 엔드포인트

#### GET /api/users
모든 사용자 조회

**쿼리 파라미터**:
- `skip`: 건너뛸 개수 (default: 0)
- `limit`: 반환할 최대 개수 (default: 10)

**응답** (200 OK):
```json
[
  {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "bio": "I like AI",
    "profilePhoto": "https://...",
    "createdAt": "2024-01-01T12:00:00",
    "updatedAt": "2024-01-01T12:00:00"
  }
]
```

#### GET /api/users/{user_id}
특정 사용자 조회

**응답** (200 OK):
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "bio": "I like AI",
  "profilePhoto": "https://...",
  "createdAt": "2024-01-01T12:00:00",
  "updatedAt": "2024-01-01T12:00:00"
}
```

#### PUT /api/users/{user_id}
사용자 정보 수정

**요청**:
```json
{
  "username": "john_updated",
  "email": "john_new@example.com",
  "bio": "I like AI and storytelling"
}
```

**응답** (200 OK):
```json
{
  "id": 1,
  "username": "john_updated",
  "email": "john_new@example.com",
  "bio": "I like AI and storytelling",
  "profilePhoto": "https://...",
  "createdAt": "2024-01-01T12:00:00",
  "updatedAt": "2024-01-01T13:00:00"
}
```

#### DELETE /api/users/{user_id}
사용자 삭제

**응답** (204 No Content): 없음

#### PUT /api/users/{user_id}/password
비밀번호 변경

**요청**:
```json
{
  "current_password": "old_password123",
  "new_password": "new_password456"
}
```

**응답** (200 OK):
```json
{
  "message": "비밀번호가 변경되었습니다"
}
```

---

## 3. Post Router (`post.py`)

### 역할
- 게시물 목록 조회
- 게시물 상세 조회
- 게시물 생성
- 게시물 수정
- 게시물 삭제
- AI 내용 생성

### 엔드포인트

#### GET /api/posts
모든 게시물 조회 (페이지네이션)

**쿼리 파라미터**:
- `skip`: 건너뛸 개수 (default: 0)
- `limit`: 반환할 최대 개수 (default: 10)

**응답** (200 OK):
```json
[
  {
    "id": 1,
    "title": "AI 시대의 이야기",
    "content": "인공지능이 세상을 바꾸고 있습니다...",
    "author": "john_doe",
    "userId": 1,
    "nextStoryCount": 8,
    "createdAt": "2024-01-01T12:00:00",
    "updatedAt": "2024-01-01T12:00:00",
    "comments": [...],
    "commentCount": 2
  }
]
```

#### GET /api/posts/{post_id}
특정 게시물 조회 (댓글 포함)

**응답** (200 OK):
```json
{
  "id": 1,
  "title": "AI 시대의 이야기",
  "content": "인공지능이 세상을 바꾸고 있습니다...",
  "author": "john_doe",
  "userId": 1,
  "nextStoryCount": 8,
  "createdAt": "2024-01-01T12:00:00",
  "updatedAt": "2024-01-01T12:00:00",
  "comments": [
    {
      "id": 1,
      "content": "그 다음...",
      "author": "jane_doe",
      "userId": 2,
      "postId": 1,
      "createdAt": "2024-01-01T13:00:00",
      "updatedAt": "2024-01-01T13:00:00"
    }
  ],
  "commentCount": 1
}
```

#### POST /api/posts
게시물 생성

**요청**:
```json
{
  "title": "AI 시대의 이야기",
  "content": "인공지능이 세상을 바꾸고 있습니다...",
  "author": "john_doe",
  "nextStoryCount": 8
}
```

**응답** (201 Created): 생성된 게시물

#### PUT /api/posts/{post_id}
게시물 수정

**요청**:
```json
{
  "title": "AI 시대의 이야기 - 수정",
  "content": "인공지능이 세상을 바꾸고 있습니다... (수정)",
  "author": "john_doe"
}
```

**응답** (200 OK): 수정된 게시물

#### DELETE /api/posts/{post_id}
게시물 삭제

**응답** (204 No Content): 없음

#### GET /api/posts/{post_id}/remaining-stories
남은 이야기 개수 조회

**응답** (200 OK):
```json
{
  "remaining_count": 6,
  "total_count": 8,
  "current_count": 2
}
```

#### POST /api/posts/{post_id}/generate-ai
AI로 다음 이야기 생성

**응답** (200 OK):
```json
{
  "generated_content": "그 다음 주인공은 새로운 모험을 시작했습니다..."
}
```

---

## 4. RelayStory Router (`relay_story.py`)

### 역할
- 게시물의 댓글(릴레이 스토리) 조회
- 댓글 생성
- 댓글 수정
- 댓글 삭제
- 스토리 완성 확인

### 엔드포인트

#### GET /api/posts/{post_id}/comments
게시물의 모든 댓글 조회

**쿼리 파라미터**:
- `skip`: 건너뛸 개수 (default: 0)
- `limit`: 반환할 최대 개수 (default: 50)

**응답** (200 OK):
```json
[
  {
    "id": 1,
    "content": "그 다음...",
    "author": "jane_doe",
    "userId": 2,
    "postId": 1,
    "createdAt": "2024-01-01T13:00:00",
    "updatedAt": "2024-01-01T13:00:00"
  }
]
```

#### GET /api/posts/{post_id}/comments/{comment_id}
특정 댓글 조회

**응답** (200 OK): 댓글 정보

#### POST /api/posts/{post_id}/comments
새로운 댓글 생성

**요청**:
```json
{
  "content": "그 다음 주인공은 새로운 모험을 시작했습니다...",
  "author": "jane_doe"
}
```

**응답** (201 Created): 생성된 댓글

#### PUT /api/posts/{post_id}/comments/{comment_id}
댓글 수정

**요청**:
```json
{
  "content": "그 다음 주인공은 새로운 모험을 시작했습니다... (수정)",
  "author": "jane_doe"
}
```

**응답** (200 OK): 수정된 댓글

#### DELETE /api/posts/{post_id}/comments/{comment_id}
댓글 삭제

**응답** (204 No Content): 없음

#### GET /api/posts/{post_id}/comments/check-complete
스토리 완성 여부 확인

**응답** (200 OK):
```json
{
  "is_complete": false,
  "remaining_count": 6
}
```

---

## 라우터 통합

`main.py`에서 모든 라우터를 등록해야 합니다:

```python
from fastapi import FastAPI
from routers import auth_router, user_router, post_router, relay_story_router

app = FastAPI()

# 라우터 등록
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(post_router)
app.include_router(relay_story_router)
```

---

## 참고사항

- 모든 응답 상태 코드는 RESTful 표준을 따릅니다
- 인증이 필요한 엔드포인트에는 `Depends(verify_token)` 추가 예정
- 권한 확인(본인만 수정/삭제)은 컨트롤러에서 처리 예정
- 비밀번호는 응답에 절대 포함되지 않습니다
