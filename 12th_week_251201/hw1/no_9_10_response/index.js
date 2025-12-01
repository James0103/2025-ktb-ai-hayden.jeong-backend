const express = require('express')
const app = express()
const port = 3000

// POST Body를 읽어오기 위한 추가 config
app.use(express.json({ extended: true }));

// 기본 Send 응답
app.get('/', (req, res) => {
  /*
  HTTP 응답을 전송합니다.
  body 매개변수는 Buffer 객체, 문자열, 객체, Boolean 또는 Array일 수 있습니다.
  */
  res.send('Hello World!')
})

// JSON 응답
app.get("/res_json", (_, res) => {
  /*
  JSON 응답을 전송합니다. 이 메서드는 JSON.stringify()를 사용하여 매개변수를 JSON 문자열로 변환한 응답(올바른 콘텐츠 유형 포함)을 전송합니다.
  매개변수는 객체, 배열, 문자열, 부울, 숫자 또는 null을 포함한 모든 JSON 유형일 수 있으며, 다른 값을 JSON으로 변환하는 데에도 사용할 수 있습니다.
  */
  res.json({ user: 'tomi', age: 5, gender: 'male', description: 'he is adorable!!' })
})

// END 응답
app.get("/end", (_, res) => {
  /*
  응답 프로세스를 종료합니다. 이 메서드는 Node.js 코어, 특히 http.ServerResponse의 response.end() 메서드에서 제공됩니다.
  데이터 없이 응답을 빠르게 종료하는 데 사용합니다. 데이터를 포함하여 응답해야 하는 경우 res.send() 및 res.json()과 같은 메서드를 대신 사용하세요.
  */
  res.write("Hello\n")
  res.write("this is res.end() test\n")
  res.end("end of response")
  // 이 아래로 write는 모두 에러가 난다(Stream이 종료됐는데 보내려고 하므로)
  res.write("it is NOT sending to client")
})

// POST 테스트
app.post("/post-test", (req, res) => {
  const user_request = req.body
  const req_keys = Object.keys(user_request)
  if (req_keys.includes("name") == false) {
    res.status(404).send("no query for parsing")
  } else {
    if (user_request["name"] != "ryan") {
      res.status(404).send(`no data for ${user_request["name"]}`)
    } else {
       res.json({ "name": "ryan", "age": 10, "spicies": "Lion", "company": "kakao" })
    }
  }
})

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})