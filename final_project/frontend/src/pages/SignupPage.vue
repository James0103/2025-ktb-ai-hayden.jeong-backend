<template>
  <div class="signup-container">
    <div class="signup-box">
      <div class="box-header">
        <router-link to="/login" class="btn-back">
          <span class="material-symbols-outlined">chevron_backward</span>
        </router-link>
      </div>
      <h1>회원가입</h1>

      <!-- 프로필 사진 업로드 -->
      <div class="profile-photo-section">
        <div class="profile-photo-container" @click="handlePhotoClick">
          <img v-if="profilePhotoPreview" :src="profilePhotoPreview" alt="프로필 사진" class="profile-photo-preview" />
          <div v-else class="profile-photo-placeholder">
            <span class="image-plus">+</span>
          </div>
        </div>
        <input
          ref="fileInput"
          type="file"
          accept="image/*"
          @change="handleProfilePhotoChange"
          style="display: none"
        />
      </div>

      <form @submit.prevent="handleSignup">
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
            :class="{ 'error': form.password && !isValidPassword(form.password) }"
            v-model="form.password"
            type="password"
            placeholder="비밀번호를 입력하세요"
            maxlength="20"
            required
          />
          <span v-if="form.password && !isValidPassword(form.password)" class="error-text">
            비밀번호는 8자 이상, 20자 이하, 대/소문자, 숫자, 특수문자를 각각 최소 1개 포함해야 합니다.
          </span>
        </div>
        <div class="form-group">
          <label for="password-confirm">비밀번호 확인</label>
          <input
            id="password-confirm"
            v-model="form.passwordConfirm"
            type="password"
            placeholder="비밀번호를 한번 더 입력하세요"
            maxlength="20"
            required
          />
          <span v-if="!isPwConfirmed(form)" class="error-text">
            비밀번호가 다릅니다.
          </span>
        </div>
        <div class="form-group">
          <label for="nickname">닉네임</label>
          <input
            id="nickname"
            v-model="form.nickname"
            type="text"
            placeholder="닉네임을 입력하세요"
            maxlength="10"
            required
          />
          <span v-if="!isValidNickname(form.nickname)" class="error-text">
            닉네임은 띄어쓰기불가, 10글자 이내로 작성해주세요
          </span>
        </div>
        <button type="submit" class="btn-primary">회원가입</button>
      </form>
      <p class="login-link">
        이미 계정이 있으신가요?
        <router-link to="/login">로그인</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'

const fileInput = ref(null)
const profilePhotoPreview = ref(null)
const userStore = useUserStore()
const router = useRouter()

const form = reactive({
  email: '',
  password: '',
  passwordConfirm: '',
  nickname: '',
  profilePhoto: null,
})

const handlePhotoClick = () => {
  if (profilePhotoPreview.value) {
    // 이미지가 있으면 삭제
    profilePhotoPreview.value = null
    form.profilePhoto = null
    fileInput.value.value = ''
  } else {
    // 이미지가 없으면 파일 선택
    fileInput.value?.click()
  }
}

const handleProfilePhotoChange = (event) => {
  const file = event.target.files?.[0]
  if (file) {
    form.profilePhoto = file
    const reader = new FileReader()
    reader.onload = (e) => {
      profilePhotoPreview.value = e.target?.result
    }
    reader.readAsDataURL(file)
  }
}

const handleSignup = async () => {
  const _email = isValidEmail(form.email)
  if (_email == false) {
    return window.alert("이메일이 올바르지 않습니다")
  }

  const _pwd = isValidPassword(form.password)
  if (_pwd == false) {
    return window.alert("비밀번호가 올바르지 않습니다")
  }

  const _pwdConfirm = form.password == form.passwordConfirm
  if (_pwdConfirm == false) {
    return window.alert("비밀번호 확인이 올바르지 않습니다")
  }

  const _nick = isValidNickname(form.nickname)
  if (_nick == false) {
    return window.alert("닉네임 형식이 올바르지 않습니다")
  }

  try {
    const result = await userStore.signup(form)
    if (result) {
      alert('회원가입 성공! 로그인해주세요.')
      router.push('/login')
    }
  } catch (error) {
    alert('회원가입 실패: ' + error.message)
  }
}

// 유효성 검사 함수
const isValidEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

const isValidPassword = (password) => {
  const pwRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[a-zA-Z\d@$!%*?&]{8,20}$/
  return pwRegex.test(password)
}

const isPwConfirmed = (form) => {
  return form.password == form.passwordConfirm
}

const isValidNickname = (nickname) => {
  const nicknameRegex = /^[^\s]{1,10}$/  // 띄어쓰기 없고 1-10자
  return nicknameRegex.test(nickname)
}
</script>

<style scoped>
.signup-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-image: url('@/assets/background.png');
  background-size: cover;
}

.signup-box {
  background: white;
  padding: 20px 30px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-height: 80%;
  max-width: 400px;
  position: relative;
}

.box-header {
  display: flex;
  justify-content: flex-start;
  margin-bottom: 20px;
}

h1 {
  text-align: center;
  margin-bottom: 25px;
  color: #333;
  font-size: 24px;
}

.profile-photo-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 30px;
}

.profile-photo-container {
  width: 100px;
  height: 100px;
  margin-bottom: 12px;
  border-radius: 50%;
  overflow: hidden;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid #e0e0e0;
  cursor: pointer;
  transition: all 0.2s;
}

.profile-photo-container:hover {
  border-color: var(--primary-color);
  background: #f0f0f0;
}

.profile-photo-preview {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.profile-photo-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
}

.image-plus {
  font-size: 24px;
  font-weight: bold;
}

.form-group {
  margin-bottom: 8px;
  height: 100px;
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

.login-link {
  text-align: center;
  margin-top: 20px;
  color: #666;
  font-size: 14px;
}

.login-link a {
  color: var(--primary-color);
  text-decoration: none;
  font-weight: 600;
}

.login-link a:hover {
  text-decoration: underline;
}

.material-symbols-outlined {
  font-variation-settings:
  'FILL' 0,
  'wght' 400,
  'GRAD' 0,
  'opsz' 24
}

.error-text {
  font-size: 10px;
  font-weight: bold;
  color: var(--error-color);
}
</style>
