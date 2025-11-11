### 과제 주제
3. (중급자를 위한) 커뮤니티 서비스 HTTP REST API 사전 설계하여 작성해보기 (복제용 rest api 시트 )

---

### 시트 링크
https://docs.google.com/spreadsheets/d/104pbXSiy46grhG1TARFxoJBPuw9R-2Lpvz8hLaed3D4/edit?usp=sharing

---

### API 요약
### 페이지별 구분

| 회원가입 | 로그인 | 게시글 목록 | 게시글 상세조회 | 회원정보수정 |
|-------|-------|-------|-------|-------|
| 회원가입(/users/signup) | 로그인(/user/signin) | 게시글 목록 조회(/posts?limit={limit_count}&next={next_id}) | 게시글 상세조회(/post/{post_id}) | 회원정보수정(/user/edit-profile) |
|                       |                    | 게시글 추가(/make-post) | 게시글 수정(/edit-post) | 비밀번호수정(/user/edit-password) |
|                       |                    |                      | 게시글 삭제(/post/{post_id}) | |

### 게시글 상세 조회 댓글 기능
| 댓글 기능 |
|-------|
| 댓글조회(/reply/{post_id}?limit={limit_count}&next={next_id})|
| 댓글수정(/reply/{post_id})|
| 댓글삭제(/reply/{post_id})|