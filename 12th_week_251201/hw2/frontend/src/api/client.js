import axios from 'axios'

const apiClient = axios.create({
  // 개발용
  // baseURL: 'http://localhost:8000',
  // 배포용 : 같은 서버에 존재하기 때문에 주소가 같음
  baseURL: '/',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

export default apiClient
