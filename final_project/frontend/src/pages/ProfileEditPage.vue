<template>
  <div class="profile-container">
    <div class="profile-box">
      <div class="header">
        <h1>회원정보 수정</h1>
      </div>
      <form @submit.prevent="handleUpdate">
        <!-- 프로필 사진 변경 -->
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

        <div class="form-group">
          <label for="email">이메일</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            readonly
            disabled
          />
        </div>
        <div class="form-group">
          <label for="nickname">사용자 닉네임</label>
          <input
            id="nickname"
            v-model="form.nickname"
            type="text"
            placeholder="닉네임을 입력하세요"
            maxlength="10"
            required
          />
        </div>
        <div class="button-group">
          <button type="submit" class="btn-primary">수정 완료</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'

const router = useRouter()
const userStore = useUserStore()

const fileInput = ref(null)
const profilePhotoPreview = ref(null)

const form = reactive({
  nickname: '',
  email: '',
  profilePhoto: null,
})

onMounted(() => {
  if (userStore.user) {
    form.nickname = userStore.user.nickname
    form.email = userStore.user.email
    if (userStore.user.profilePhoto) {
      profilePhotoPreview.value = userStore.user.profilePhoto
    }
  } else {
    router.push('/login')
  }
})

const handlePhotoClick = () => {
  if (profilePhotoPreview.value) {
    const resp = window.confirm("확인을 누르면 프로필 이미지가 삭제됩니다")
    if (resp) {
      // 이미지가 있으면 삭제
      profilePhotoPreview.value = null
      form.profilePhoto = null
      fileInput.value.value = ''
    }
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

const handleUpdate = async () => {
  try {
    await userStore.updateProfile(form.nickname, null, form.profilePhoto)
    alert('회원정보가 수정되었습니다.')
  } catch (error) {
    alert('수정 실패: ' + error.message)
  }
}
</script>

<style scoped>
.profile-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-image: url('@/assets/background.png');
  background-size: cover;
}

.profile-box {
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

.profile-photo-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 30px;
}

.profile-photo-container {
  width: 120px;
  height: 120px;
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
  font-size: 28px;
  font-weight: bold;
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

input,
textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  box-sizing: border-box;
  font-family: inherit;
}

input:focus,
textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.button-group {
  display: flex;
  gap: 10px;
  margin-top: 30px;
}
</style>
