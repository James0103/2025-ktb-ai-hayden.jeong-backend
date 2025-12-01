const express = require('express')
const timeout = require('connect-timeout');
const app = express()
const port = 3000

async function timeout_timer() {
  return new Promise((res) => {
    let i = 0;

    const interval = setInterval(() => {
      console.log(`${10 - i} seconds left`);
      i += 1;
      
      if (i >= 10) {
        clearInterval(interval);
        res("10 seconds completed!");
      }
    }, 1000);
  })
}

// 타임아웃 테스트
// 요청이 들어오고 5초 뒤에 타임아웃으로 503 반환
app.get('/test_timeout', timeout('5s'), async (req, res) => {  
  const result = await timeout_timer()
  res.send(result)
})
// 동일 코드에 타임아웃이 없는 코드로 10초 뒤에 결과 문자열인 "10 seconds completed!" 반환
app.get('/no_timeout', async (req, res) => {
  const result = await timeout_timer()
  res.send(result)
})

// rate-limit 적용
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
  windowMs: 10000,          // 10초
  max: 1,                  // 최대 1회 요청
});

/*
rate-limit를 적용해서 최대 1회 요청 이후에는 모두 429 반환
10초의 제한을 둔뒤 10초가 지나면 새로운 요청이 가능
(현재 timeout_timer 프로세스가 완료된 직후 바로 새 요청을 받을수 있음)
*/
app.get("/rate_limit", limiter, async (req, res) => {
  const result = await timeout_timer()
  res.send(result)
})

/*
CSP 보안 설정
 */
const csp = require("helmet-csp")
app.get("/secure_path", csp({ directives: { 'img-src': ["'none'"] } }), (req, res) => {
  res.send('<img src="https://placehold.co/600x400"> 테스트');
})

app.get('/unsecure_path', (req, res) => {
  res.send('<img src="https://placehold.co/600x400"> 테스트');
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
})