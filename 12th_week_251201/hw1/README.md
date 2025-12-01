## 12주차 과제 1번
### 미니퀘스트
교재에 있는 미니퀘스트 모두 해보기
문제에 대한 답이나 직접적인 해결책은 검색하거나 GPT 활용 금지, 문법이나 사용법 등은 검색 가능

---
### 과제 설명

### - 서버의 이해 및 실습
- ✅ 1번 퀘스트 : VSCode 설치하기 -> 로컬 컴퓨터 스크린샷 제출
- ✅ 2번 퀘스트 : Node.js 설치하기 -> 로컬 컴퓨터 스크린샷 제출
- ✅ 3번 & 4번 퀘스트 : express.js 설치하기, 브라우저와 express.js를 이용하여 get요청을 확인하기<br>
-> package.json 확인 및 프로젝트 실행(node index.js 혹은 npm run start로 실행)<br>
-> curl 테스트를 이용한 GET 요청 확인<br>
- ✅ 5번 퀘스트 : 포스트맨 설치하기 -> 로컬 컴퓨터 스크린샷 제출
- ✅ 6번 퀘스트 : ESLint & Prettier, Airbnb Style Guide로 설정하기<br>
📦 no_6_7_style_guide<br>
 ┣ 📜 index_unfix.js -> fix전 원본 파일<br>
 ┗ 📜 index.js -> main index 파일(lint로 fix)<br>
->     "lint:index": "eslint --fix index.js" 명령어로 특정 파일만 수정해서 동작 확인<br>
- ✅ 7번 퀘스트 : 포스트맨과 express.js를 이용하여 get요청을 확인하기 -> 로컬 컴퓨터 스크린샷 제출
- ✅ 8번 퀘스트 : HTTP메서드, 상태코드에 대해서 각각 한 줄로 정리해보세요<br>
`1. HTTP메서드 : 클라이언트와 호스트(서버)가 통신할 때 어떤 방식으로 소통할 것인지를 정하는 규칙`<br>
`2. 상태코드 : 호스트(서버)에서 클라이언트의 요청에 대한 응답의 상태를 숫자로 표현하는 규칙. 미리 정해진 규칙에 의해 숫자가 정해지고 이 숫자를 통해 클라이언트는 호스트(서버)에 대한 요청 상황을 대략적인 상황을 유추할 수 있다.`<br><br>

- ✅ 9번&10번 퀘스트 : response.send() vs response.json() vs response.end() 공부하고 적용해보세요.<br>
-> 각각의 end point를 만들어서 적용<br>
-> POST의 경우 /post-test로 이름 데이터인 {"name": "ryan"} 을 전달하면 해당 저장 내용이 출력<br>
-> 그외의 데이터는 모두 404 반환<br>

- ✅ 11번&12번&13번 퀘스트 : 
-> 11번 : connect-timeout 모듈에 대해 공부하고 적용해보세요.<br>
`/test_timeout과 /no_timeout 으로 구분. 내부적으로 10초를 세는 타이머를 만들고 타임아웃을 5초로 두어 /test_timeout은 내부 타이머와 상관없이 5초 뒤에 에러 반환.`<br>
`/no_timeout은 내부 타이머 완료 후 결과값 반환`<br>
-> 12번 : express-rate-limit 모듈에 대해 공부하고 적용해보세요.<br>
`/rate_limit에 limit을 두어 최대 1회의 요청에만 반응하도록 함`<br>
`테스트는 POSTMAN, CURL 양쪽에서 진행했고, 요청 이후 10초의 시간이 흐르면 새 요청 가능`<br>
-> 13번 : 컨텐츠 보안 정책에 대해 알아보고 express에 미들웨어를 이용하여 적용해보세요.<br>
`콘텐츠 보안 정책 (CSP)는 교차 사이트 스크립팅(XSS)과 데이터 주입 공격을 비롯한 특정 유형의 공격을 탐지하고 완화하는 데 도움이 되는 추가 보안 계층입니다. 이러한 공격은 데이터 절도에서 사이트 훼손, 맬웨어 배포에 이르기까지 모든 것에 사용됩니다.`<br>
`/secure_path와 /unsecure_path로 나누어 각각 동일한 웹상의 이미지를 서빙하는 코드를 전달합니다. secure_path의 경우 이미지가 나오질 않고, 웹 디버거에서 block되었다고 나오는 반면 unsecure_path는 그렇지 않고 이미지가 출력됩니다`<br>
- 14번 퀘스트 : 비지니스 로직과 routes, controller, model에 대해서 공부하시고 routes, controller만 적용해보세요!<br><br>

### - 데이터베이스
- 15번 퀘스트 : MySQL을 설치하세요. (교재에서는 XAMPP 사용, MySQL Server 로 설치해도 무방합니다)
- ✅ 16번 퀘스트 : DBeaver를 설치하세요. -> 로컬 컴퓨터 스크린샷 제출
- 17번 퀘스트 : aquerytool로 커뮤니티 DB 설계 하기
- 18번 퀘스트 : dot.env에 대해 공부하고 적용해보세요
- 19번 퀘스트 : colors, moment모듈을 사용해서 api에서 보이는 sql문을 express 동작시 콘솔에서 보이게 해보세요!<br>단, 콘솔에 요청하는 시간과 SQL 문이 같이 나오게 해야함
- 20번 퀘스트 : 데이터베이스를 연결하고, 기존의 라우트, 컨트롤러 외에 모델을 추가해 DB 기능을 사용해보세요.
- 21번 퀘스트 : 암호화 종류에 대해 공부해서 각각 한줄로 정의하세요! (md5, sha family, scrypt, bcrypt)
- 22번 퀘스트 : 커뮤니티 프로젝트에 bcrypt 암호화를 로그인, 회원가입을 할 때 패스워드에 적용해보세요!<br><br>

### - 인증/인가
- 23번 퀘스트 : web storage에 대해 공부하고 5단 분석법으로 정리해주세요
- 24번 퀘스트 : 쿠키, 세션으로 인증, 인가를 구현해보세요!<br>인증,인가 받지 않았을 때 400 상태코드를 리턴해보세요!<br><br>

### - 배포
- 25번 퀘스트 : 루트 디렉토리에 README.md 파일을 만들어서 작성해보세요. (기술 리스트, 회고) 
- 26번 퀘스트 : 이용약관 terms 폴더를 만들어 이용약관, 개인정보 페이지를 프론트엔드로 html 파일을 서빙하는 코드를 작성해보세요.
- 27번 퀘스트 : 필요하다고 생각하는 log들을 남겨보세요!<br><br>

### - 프론트엔드의 이해 및 실습
- ✅ 28번 퀘스트 : Codepen에서 HTML만을 이용하여 간단한 form 형태의 페이지를 만들어보세요.<br>정해져 있는 답안지 없이, 자유롭게 만들고 싶은 것을 만들어보세요.<br>
-> 링크 제출 : https://codepen.io/James-Jung-the-styleful/pen/yyOqNzg
<br><br>

  *29~34번 퀘스트는 하나의 디렉토리(no_29_34_frontend)에 합쳐서 진행*<br>
  * npm run start로 실행<br>
  📦 no_29_34_frontend<br>
  ┣ 📂 static<br>
  ┃ ┣ 📜error.html<br>
  ┃ ┣ 📜favicon.ico<br>
  ┃ ┣ 📜index.html<br>
  ┃ ┣ 📜loading.json<br>
  ┃ ┣ 📜main.css<br>
  ┃ ┣ 📜modal.css<br>
  ┃ ┗ 📜post.html<br>
  ┣ 📜 index.js<br>
  ┣ 📜 package-lock.json<br>
  ┗ 📜 package.json<br>
<br>
- ✅ 29번 퀘스트 : 프론트엔드용 express 서버 만들고, 브라우저에서 html 파일 응답해주기<br>
-> `html 서빙용 코드를 app.get("/")에 배치`
- ✅ 30번 퀘스트 : 커뮤니티 홈페이지를 디자인해보세요.<br>
조건1 : HTML, CSS, Flex 만 이용할 것
-> `main.css라는 이름의 별도의 스타일시트 지정`
- ✅ 31번 퀘스트 : 버튼을 클릭하면 다른 페이지로 이동하는 Event 코드를 작성해보세요.
-> `초기 페이지에서 각 게시글의 요약본을 클릭하면 디테일한 포스트 내용으로 이동하도록 설정`
- ✅ 32번 퀘스트 : 버튼을 클릭하면 서버에 데이터 요청하는 코드 작성해보세요.<br>https://jsonplaceholder.typicode.com/posts/1 이 URL로 요청을 하면 더미데이터를 받아볼 수 있습니다!<br>
-> `초기 페이지 및 디테일한 포스트 페이지에서 데이터를 요청하도록 설정`
- ✅ 33번 퀘스트 : DOM과 Event, Fetch를 사용해서 헤더, 게시글, 댓글, 모달창(dialog)를 만들어 보세요.<br>모든 페이지의 상호작용(이벤트) 요소에 Event, Fetch를 이용하여 백엔드 서버와 연동 하세요.
-> `댓글 작성에 모달 적용`
- ✅ 34번 퀘스트 : lottie를 적용할 수 있는 곳에 lottie를 직접 적용해보세요.<br>
-> `초기 데이터 로딩시 페이지 하단에 프로그레스 애니메이션으로 lottie 파일 적용`

### - Release
- 35번 퀘스트 : 프론트엔드 서버 배포를 해봅니다.
- 36번 퀘스트 : http로 접근했을 때 https 로 리다이렉트 합니다.
- 37번 퀘스트 : cors에 대해 5단 분석법을 해보세요.
- 38번 퀘스트 : 배포 후 QA를 진행합니다.
- 39번 퀘스트 : Domain, HTTPS , SEO 적용을 합니다.