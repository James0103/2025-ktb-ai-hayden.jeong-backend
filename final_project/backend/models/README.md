# Backend Pydantic Models

이 디렉토리는 FastAPI 애플리케이션에서 사용되는 모든 Pydantic 모델을 포함합니다. 이 모델들은 API 요청/응답 검증 및 직렬화에 사용됩니다.

## 모델 개요

### 1. User (사용자)

**목적**: 사용자 정보 관리

**속성**:
- `id` (int, optional): 사용자 고유 ID
- `username` (str): 사용자명 (1-50자)
- `email` (EmailStr): 이메일 주소
- `bio` (str): 사용자 소개 (최대 500자)
- `profilePhoto` (str, optional): 프로필 사진 URL
- `createdAt` (datetime): 생성 날짜
- `updatedAt` (datetime): 수정 날짜

**관련 모델**:
- `UserCreate`: 회원가입 시 사용 (username, email, password)
- `UserUpdate`: 프로필 수정 시 사용 (username, email, bio)
- `UserResponse`: API 응답 모델

**사용 예시**:
```python
# 회원가입
user_data = UserCreate(
    username="john_doe",
    email="john@example.com",
    password="securepassword123"
)

# 프로필 수정
update_data = UserUpdate(
    username="john_updated",
    bio="I like AI and storytelling"
)

# API 응답
response = UserResponse(
    id=1,
    username="john_doe",
    email="john@example.com",
    bio="I like AI and storytelling",
    profilePhoto="https://...",
    createdAt=datetime.now(),
    updatedAt=datetime.now()
)
```

---

### 2. Post (게시물)

**목적**: 릴레이 스토리의 초기 글 관리

**속성**:
- `id` (int, optional): 게시물 고유 ID
- `title` (str): 글 제목 (1-500자)
- `content` (str): 글 내용
- `author` (str): 작성자명 (1-50자)
- `userId` (int): 작성자 ID
- `nextStoryCount` (int): 다음 이야기 개수 (4-16개)
- `createdAt` (datetime): 생성 날짜
- `updatedAt` (datetime): 수정 날짜
- `comments` (List[dict]): 릴레이 스토리 댓글 목록

**관련 모델**:
- `PostCreate`: 게시물 생성 시 사용
- `PostUpdate`: 게시물 수정 시 사용
- `PostResponse`: API 응답 모델

**계산 속성**:
- `comment_count`: 현재 댓글 개수
- `remaining_stories`: 남은 이야기 개수 (nextStoryCount - comment_count)

**사용 예시**:
```python
# 게시물 생성
post_data = PostCreate(
    title="AI 시대의 이야기",
    content="인공지능이 세상을 바꾸고 있습니다...",
    author="john_doe",
    nextStoryCount=8
)

# 게시물 수정
update_data = PostUpdate(
    title="AI 시대의 이야기 - 수정",
    content="인공지능이 세상을 바꾸고 있습니다..."
)

# API 응답
response = PostResponse(
    id=1,
    title="AI 시대의 이야기",
    content="인공지능이 세상을 바꾸고 있습니다...",
    author="john_doe",
    userId=1,
    nextStoryCount=8,
    createdAt=datetime.now(),
    updatedAt=datetime.now(),
    comments=[...],
    commentCount=2
)
```

---

### 3. RelayStory (릴레이 스토리)

**목적**: 게시물의 다음 이야기(댓글) 관리

**속성**:
- `id` (int, optional): 릴레이 스토리 고유 ID
- `content` (str): 이야기 내용
- `author` (str): 작성자명 (1-50자)
- `userId` (int): 작성자 ID
- `postId` (int): 게시물 ID (외래키)
- `createdAt` (datetime): 생성 날짜
- `updatedAt` (datetime): 수정 날짜

**관련 모델**:
- `RelayStoryCreate`: 릴레이 스토리 생성 시 사용
- `RelayStoryUpdate`: 릴레이 스토리 수정 시 사용
- `RelayStoryResponse`: API 응답 모델

**사용 예시**:
```python
# 릴레이 스토리 생성
story_data = RelayStoryCreate(
    content="그 다음 주인공은 새로운 모험을 시작했습니다...",
    author="jane_doe",
    postId=1
)

# 릴레이 스토리 수정
update_data = RelayStoryUpdate(
    content="그 다음 주인공은 새로운 모험을 시작했습니다... (수정)"
)

# API 응답
response = RelayStoryResponse(
    id=1,
    content="그 다음 주인공은 새로운 모험을 시작했습니다...",
    author="jane_doe",
    userId=2,
    postId=1,
    createdAt=datetime.now(),
    updatedAt=datetime.now()
)
```

---

## 프론트엔드와의 통신

이 Pydantic 모델들은 프론트엔드의 JavaScript 모델과 다음과 같이 매핑됩니다:

| Backend (Pydantic) | Frontend (JavaScript) | 용도 |
|---|---|---|
| `UserCreate` | - | 회원가입 요청 |
| `UserUpdate` | - | 프로필 수정 요청 |
| `UserResponse` | `User` | 사용자 정보 응답 |
| `PostCreate` | `Post` | 게시물 생성 요청 |
| `PostUpdate` | - | 게시물 수정 요청 |
| `PostResponse` | `Post` | 게시물 조회 응답 |
| `RelayStoryCreate` | `RelayStory` | 릴레이 스토리 생성 요청 |
| `RelayStoryUpdate` | - | 릴레이 스토리 수정 요청 |
| `RelayStoryResponse` | `RelayStory` | 릴레이 스토리 조회 응답 |

---

## 주요 특징

### 1. 타입 검증
- `EmailStr`을 통한 이메일 유효성 검증
- `Field(min_length, max_length)`을 통한 문자열 길이 검증
- `ge, le`를 통한 숫자 범위 검증

### 2. 선택적 필드
- `Optional[T]` 타입으로 선택적 필드 지정
- `Field(None)`으로 기본값 설정

### 3. 기본값
- `Field(default_factory=datetime.utcnow)`로 자동 타임스탐프 생성
- `Field(default_factory=list)`로 빈 리스트 초기화

### 4. ORM 호환성
- `Config.from_attributes = True` 설정으로 SQLAlchemy 모델과 호환

---

## 사용 방법

### API 엔드포인트에서 사용

```python
from fastapi import FastAPI
from models import UserCreate, UserResponse

app = FastAPI()

@app.post("/api/auth/signup", response_model=UserResponse)
async def signup(user: UserCreate):
    # user는 자동으로 UserCreate로 검증됨
    # 응답은 UserResponse로 직렬화됨
    return UserResponse(
        id=1,
        username=user.username,
        email=user.email,
        bio="",
        profilePhoto=None,
        createdAt=datetime.now(),
        updatedAt=datetime.now()
    )
```

### 프론트엔드에서의 API 호출

```javascript
// 회원가입
const response = await fetch('/api/auth/signup', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        username: 'john_doe',
        email: 'john@example.com',
        password: 'securepassword123'
    })
})

const userData = await response.json()
// userData는 UserResponse 형식으로 반환됨
```

---

## 참고사항

- 모든 날짜/시간은 UTC 기준입니다
- `createdAt`과 `updatedAt`은 자동으로 설정되므로 생성/수정 요청에서는 포함하지 마세요
- 비밀번호는 `UserCreate`에만 포함되고, 응답에는 절대 포함되지 않습니다
- `from_attributes = True` 설정으로 SQLAlchemy ORM 모델에서 직접 Pydantic 모델로 변환할 수 있습니다

---

## 다음 단계

1. **데이터베이스 모델** (SQLAlchemy): ORM 모델 작성
2. **데이터베이스 설정**: 데이터베이스 연결 및 세션 관리
3. **라우터 구현**: API 엔드포인트 작성
4. **프론트엔드 연동**: API 호출 로직 구현
