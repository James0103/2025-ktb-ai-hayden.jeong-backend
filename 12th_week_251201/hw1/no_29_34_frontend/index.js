const express = require('express');
const path = require('path');
const app = express();
const port = 3000

// 정적 파일 전체 서빙
app.use(express.static(path.join(__dirname, 'static')));

// html 서빙
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'static', 'index.html'));
});

app.get('/post', (req, res) => {
  console.log(req.query)
  res.sendFile(path.join(__dirname, 'static', 'post.html'));
});

app.get('/error', (req, res) => {
  res.status(500).sendFile(path.join(__dirname, 'static', 'error.html'));
});

app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).sendFile(path.join(__dirname, 'static', 'error.html'));
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})

