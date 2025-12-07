<template>
  <div class="password-container">
    <div class="password-box">
      <div class="header">
        <h1>비밀번호 변경</h1>
      </div>
      <form @submit.prevent="handleChangePassword">
        <div class="form-group">
          <label for="new-password">새 비밀번호</label>
          <input
            id="new-password"
            :class="{ 'error': form.newPassword && !isValidPassword(form.newPassword) }"
            v-model="form.newPassword"
            type="password"
            placeholder="새 비밀번호를 입력하세요"
            maxlength="20"
            required
          />
          <span v-if="form.newPassword && !isValidPassword(form.newPassword)" class="error-text">
            비밀번호는 8자 이상, 20자 이하, 대/소문자, 숫자, 특수문자를 각각 최소 1개 포함해야 합니다.
          </span>
        </div>
        <div class="form-group">
          <label for="confirm-password">새 비밀번호 확인</label>
          <input
            id="confirm-password"
            v-model="form.confirmPassword"
            type="password"
            placeholder="새 비밀번호를 한번 더 입력하세요"
            required
          />
          <span v-if="!isPwConfirmed(form)" class="error-text">
            비밀번호가 다릅니다.
          </span>
        </div>
        <div class="button-group">
          <button type="submit" class="btn-primary">비밀번호 변경</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'

const router = useRouter()
const userStore = useUserStore()

const form = reactive({
  newPassword: '',
  confirmPassword: '',
})

onMounted(() => {
  if (!userStore.isLoggedIn) {
    router.push('/login')
  }
})

const handleChangePassword = async () => {
  if (form.newPassword !== form.confirmPassword) {
    alert('새 비밀번호가 일치하지 않습니다.')
    return
  }

  if (form.newPassword.length < 6) {
    alert('비밀번호는 최소 6자 이상이어야 합니다.')
    return
  }

  try {
    await userStore.updateProfile(null, form.newPassword, null)
    alert('비밀번호가 변경되었습니다.')
  } catch (error) {
    alert('비밀번호 변경 실패: ' + error.message)
  }
}

// 유효성 검사 함수
const isValidPassword = (password) => {
  const pwRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[a-zA-Z\d@$!%*?&]{8,20}$/
  return pwRegex.test(password)
}

const isPwConfirmed = (form) => {
  return form.newPassword == form.confirmPassword
}
</script>

<style scoped>
.password-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-image: url('@/assets/background.png');
  background-size: cover;
}

.password-box {
  background: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 500px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

h1 {
  color: #333;
  margin: 0;
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
  font-family: inherit;
}

input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.button-group {
  display: flex;
  gap: 10px;
  margin-top: 30px;
}

.error-text {
  font-size: 10px;
  font-weight: bold;
  color: var(--error-color);
}
</style>
