# Controllers

비즈니스 로직을 담당하는 컨트롤러들입니다. 각 컨트롤러는 라우터와 데이터베이스 사이의 중간 계층으로 작동합니다.

## 파일 구조

```
controllers/
├── __init__.py                    # 컨트롤러 내보내기
├── auth_controller.py             # 인증 비즈니스 로직
├── user_controller.py             # 사용자 관리 비즈니스 로직
├── post_controller.py             # 게시물 관리 비즈니스 로직
├── relay_story_controller.py      # 릴레이 스토리 비즈니스 로직
└── README.md                      # 이 파일
```

---

## 아키텍처

```
[라우터 (Router)]
        ↓
[컨트롤러 (Controller)] ← 비즈니스 로직
        ↓
[데이터베이스 (Database)]
```

### 역할 분담

| 계층 | 역할 | 책임 |
|------|------|------|
| **Router** | 엔드포인트 정의 | HTTP 요청/응답 처리 |
| **Controller** | 비즈니스 로직 | 데이터 검증, 처리, 오류 처리 |
| **Database** | 데이터 저장 | 영속성 관리 |

---

## 1. AuthController

### 역할
- 사용자 가입 처리
- 사용자 로그인 처리
- 비밀번호 변경
- JWT 토큰 검증

### 메서드 목록

#### `signup(user: UserCreate) -> UserResponse`
**목적**: 새로운 사용자를 등록합니다.

**처리 과정**:
1. 이메일 중복 확인
2. 사용자명 중복 확인
3. 비밀번호 해싱
4. 사용자 정보를 데이터베이스에 저장
5. 저장된 사용자 정보 반환

**예외**:
- `ValueError`: 이미 존재하는 이메일/사용자명
- `Exception`: 데이터베이스 오류

---

#### `login(email: str, password: str) -> dict`
**목적**: 사용자 로그인을 처리합니다.

**처리 과정**:
1. 이메일로 사용자 조회
2. 비밀번호 검증
3. JWT 토큰 생성
4. 사용자 정보와 토큰 반환

**반환값**:
```python
{
    "user": UserResponse,
    "access_token": str,
    "token_type": "bearer"
}
```

**예외**:
- `ValueError`: 이메일/비밀번호 일치하지 않음

---

#### `change_password(user_id: int, current_password: str, new_password: str) -> dict`
**목적**: 사용자의 비밀번호를 변경합니다.

**처리 과정**:
1. 사용자 조회
2. 현재 비밀번호 검증
3. 새로운 비밀번호 해싱
4. 데이터베이스 업데이트
5. 성공 메시지 반환

**예외**:
- `ValueError`: 현재 비밀번호 일치하지 않음

---

#### `verify_token(token: str) -> dict`
**목적**: JWT 토큰을 검증합니다.

**반환값**:
```python
{
    "user_id": int,
    "email": str
}
```

**예외**:
- `ValueError`: 토큰 유효하지 않음, 만료됨

---

## 2. UserController

### 역할
- 사용자 정보 조회
- 사용자 정보 수정
- 사용자 삭제
- 사용자 검증

### 메서드 목록

#### `get_all_users(skip: int, limit: int) -> List[UserResponse]`
**목적**: 모든 사용자를 조회합니다 (페이지네이션).

**처리 과정**:
1. 데이터베이스에서 사용자 조회 (offset/limit 적용)
2. UserResponse 리스트로 변환
3. 반환

---

#### `get_user(user_id: int) -> UserResponse`
**목적**: 특정 사용자의 정보를 조회합니다.

**예외**:
- `ValueError`: 사용자를 찾을 수 없음

---

#### `update_user(user_id: int, user: UserUpdate) -> UserResponse`
**목적**: 사용자 정보를 수정합니다.

**처리 과정**:
1. 사용자 존재 확인
2. 수정할 필드 검증 (이메일 중복 확인 등)
3. 데이터베이스 업데이트
4. 수정된 사용자 정보 반환

**예외**:
- `ValueError`: 사용자를 찾을 수 없음, 이메일 이미 존재

---

#### `delete_user(user_id: int) -> dict`
**목적**: 사용자를 삭제합니다.

**처리 과정**:
1. 사용자 존재 확인
2. 관련 데이터 정리 (게시물, 댓글 등)
3. 사용자 정보 삭제
4. 성공 메시지 반환

---

#### `get_user_by_email(email: str) -> UserResponse`
**목적**: 이메일로 사용자를 조회합니다.

**예외**:
- `ValueError`: 사용자를 찾을 수 없음

---

#### `check_email_exists(email: str) -> bool`
**목적**: 이메일의 존재 여부를 확인합니다.

**반환값**:
- `True`: 이메일 존재
- `False`: 이메일 미존재

---

#### `check_username_exists(username: str) -> bool`
**목적**: 사용자명의 존재 여부를 확인합니다.

---

## 3. PostController

### 역할
- 게시물 CRUD 작업
- 게시물 검색
- AI 콘텐츠 생성
- 릴레이 스토리 상태 확인

### 메서드 목록

#### `get_all_posts(skip: int, limit: int) -> List[PostResponse]`
**목적**: 모든 게시물을 조회합니다 (최신순).

**처리 과정**:
1. 데이터베이스에서 게시물 조회 (offset/limit, 최신순 정렬)
2. 각 게시물의 댓글 개수 계산
3. PostResponse 리스트로 변환
4. 반환

---

#### `get_post(post_id: int) -> PostResponse`
**목적**: 특정 게시물과 그 댓글을 모두 조회합니다.

**처리 과정**:
1. 게시물 조회
2. 게시물의 모든 댓글 조회
3. PostResponse로 변환하여 반환

---

#### `create_post(post: PostCreate, user_id: int) -> PostResponse`
**목적**: 새로운 게시물을 생성합니다.

**처리 과정**:
1. 입력값 검증 (nextStoryCount 범위: 4-16)
2. 사용자 존재 확인
3. 게시물 데이터베이스 저장
4. 생성된 게시물 반환

---

#### `update_post(post_id: int, post: PostUpdate) -> PostResponse`
**목적**: 게시물을 수정합니다.

**처리 과정**:
1. 게시물 존재 확인
2. 권한 확인 (작성자만 수정 가능)
3. 데이터베이스 업데이트
4. 수정된 게시물 반환

---

#### `delete_post(post_id: int) -> dict`
**목적**: 게시물을 삭제합니다.

**처리 과정**:
1. 게시물 존재 확인
2. 권한 확인
3. 관련 댓글 삭제
4. 게시물 삭제
5. 성공 메시지 반환

---

#### `get_user_posts(user_id: int, skip: int, limit: int) -> List[PostResponse]`
**목적**: 특정 사용자의 모든 게시물을 조회합니다.

---

#### `get_remaining_stories(post_id: int) -> dict`
**목적**: 남은 이야기 개수를 계산합니다.

**반환값**:
```python
{
    "remaining_count": int,    # 남은 개수
    "total_count": int,        # 목표 개수
    "current_count": int,      # 현재 개수
    "is_complete": bool        # 완성 여부
}
```

---

#### `generate_ai_content(post_id: int) -> dict`
**목적**: AI를 사용하여 다음 이야기를 생성합니다.

**처리 과정**:
1. 게시물 조회
2. 게시물의 제목, 내용, 기존 댓글 수집
3. AI 모델에 입력 전달
4. 생성된 내용 반환

**반환값**:
```python
{
    "generated_content": str
}
```

---

#### `search_posts(keyword: str, skip: int, limit: int) -> List[PostResponse]`
**목적**: 게시물을 검색합니다 (제목, 내용).

**처리 과정**:
1. 키워드로 데이터베이스 검색
2. 매칭된 게시물 조회
3. 최신순 정렬
4. 페이지네이션 적용
5. 결과 반환

---

## 4. RelayStoryController

### 역할
- 댓글(릴레이 스토리) CRUD 작업
- 스토리 완성 여부 확인
- 댓글 추가 가능 여부 확인

### 메서드 목록

#### `get_post_comments(post_id: int, skip: int, limit: int) -> List[RelayStoryResponse]`
**목적**: 특정 게시물의 모든 댓글을 조회합니다 (시간순).

---

#### `get_comment(post_id: int, comment_id: int) -> RelayStoryResponse`
**목적**: 특정 댓글의 정보를 조회합니다.

---

#### `create_comment(post_id: int, comment: RelayStoryCreate, user_id: int) -> RelayStoryResponse`
**목적**: 새로운 댓글(릴레이 스토리)을 생성합니다.

**처리 과정**:
1. 게시물 존재 확인
2. 스토리 완성 여부 확인 (완성되면 불가)
3. 현재 댓글 개수 < 목표 개수 확인
4. 사용자 존재 확인
5. 댓글 데이터베이스 저장
6. 생성된 댓글 반환

**예외**:
- `ValueError`: 게시물 미존재, 스토리 완성됨, 한계 초과

---

#### `update_comment(post_id: int, comment_id: int, comment: RelayStoryUpdate) -> RelayStoryResponse`
**목적**: 댓글을 수정합니다.

**처리 과정**:
1. 댓글 존재 확인
2. 권한 확인 (작성자만 수정 가능)
3. 데이터베이스 업데이트
4. 수정된 댓글 반환

---

#### `delete_comment(post_id: int, comment_id: int) -> dict`
**목적**: 댓글을 삭제합니다.

**처리 과정**:
1. 댓글 존재 확인
2. 권한 확인
3. 데이터베이스 삭제
4. 성공 메시지 반환

---

#### `get_user_comments(user_id: int, skip: int, limit: int) -> List[RelayStoryResponse]`
**목적**: 특정 사용자가 작성한 모든 댓글을 조회합니다.

---

#### `check_story_complete(post_id: int) -> dict`
**목적**: 릴레이 스토리의 완성 여부를 확인합니다.

**반환값**:
```python
{
    "is_complete": bool,
    "remaining_count": int,
    "current_count": int,
    "total_count": int
}
```

---

#### `can_add_comment(post_id: int) -> dict`
**목적**: 새로운 댓글을 추가할 수 있는지 확인합니다.

**반환값** (추가 가능):
```python
{
    "can_add": True
}
```

**반환값** (추가 불가):
```python
{
    "can_add": False,
    "reason": "이야기가 완성되었습니다" 또는 "게시물을 찾을 수 없습니다"
}
```

---

#### `get_comments_by_author(post_id: int, author: str) -> List[RelayStoryResponse]`
**목적**: 특정 게시물에서 특정 작성자의 댓글을 조회합니다.

---

## 사용 예시

### 라우터에서 컨트롤러 호출

```python
from fastapi import APIRouter
from controllers import PostController
from models import PostCreate, PostResponse

router = APIRouter()

@router.post("/posts", response_model=PostResponse)
async def create_post(post: PostCreate):
    # 라우터: HTTP 요청 처리
    # 컨트롤러: 비즈니스 로직 처리
    return await PostController.create_post(post, user_id=1)

@router.get("/posts/{post_id}", response_model=PostResponse)
async def get_post(post_id: int):
    return await PostController.get_post(post_id)
```

---

## 오류 처리

모든 컨트롤러 메서드는 다음과 같은 예외를 발생시킬 수 있습니다:

```python
try:
    result = await PostController.get_post(999)
except ValueError as e:
    # 404 Not Found
    raise HTTPException(status_code=404, detail=str(e))
except Exception as e:
    # 500 Internal Server Error
    raise HTTPException(status_code=500, detail="Internal server error")
```

---

## 다음 단계

1. **데이터베이스 모델 작성** (SQLAlchemy ORM)
2. **데이터베이스 서비스 구현** (데이터 접근 계층)
3. **컨트롤러 구현** (비즈니스 로직)
4. **라우터 구현** (엔드포인트 완성)
5. **인증/인가 추가** (JWT, 권한 확인)
6. **테스트 작성** (단위 테스트, 통합 테스트)
