<template>
  <div class="login-container">
    <div class="login-box">
      <h1>로그인</h1>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="email">이메일</label>
          <input
            id="email"
            :class="{ 'error': form.email && !isValidEmail(form.email) }"
            v-model="form.email"
            type="email"
            placeholder="이메일을 입력하세요"
            required
          />
          <span v-if="form.email && !isValidEmail(form.email)" class="error-text">
            올바른 이메일 주소 형식을 입력해주세요
          </span>
        </div>
        <div class="form-group">
          <label for="password">비밀번호</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            placeholder="비밀번호를 입력하세요"
            required
          />
        </div>
        <button type="submit" class="btn-primary">로그인</button>
      </form>
      <p class="signup-link">
        계정이 없으신가요?
        <router-link to="/signup">회원가입</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'

const router = useRouter()
const userStore = useUserStore()

const form = reactive({
  email: '',
  password: '',
})

const handleLogin = async () => {
  try {
    await userStore.login(form.email, form.password)
    router.push('/posts')
  } catch (error) {
    console.log(error)
    alert('로그인 실패: ' + error.message)
  }
}

// 유효성 검사 함수
const isValidEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-image: url('@/assets/background.png');
  background-size: cover;
}

.login-box {
  background: white;
  padding: 20px 30px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  height: 80%;
  max-width: 400px;
}

h1 {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  color: #555;
  font-weight: 500;
}

input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  box-sizing: border-box;
}

input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.signup-link {
  text-align: center;
  margin-top: 20px;
  color: #666;
  font-size: 14px;
}

.signup-link a {
  color: var(--primary-color);
  text-decoration: none;
  font-weight: 600;
}

.signup-link a:hover {
  text-decoration: underline;
}

.error-text {
  font-size: 10px;
  font-weight: bold;
  color: var(--error-color);
}
</style>
