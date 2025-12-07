<template>
  <div class="post-form-container">
    <!-- 로딩 오버레이 -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-spinner">
        <div class="spinner"></div>
        <p>AI가 내용을 생성하고 있습니다...</p>
      </div>
    </div>

    <div class="form-box">
      <button type="button" class="btn-back" @click="handleGoBack">
        <span class="material-symbols-outlined">chevron_backward</span>
      </button>
      <h1>{{ isEdit ? '글 수정' : '글 작성' }}</h1>
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="title">제목</label>
          <input
            id="title"
            v-model="form.title"
            type="text"
            placeholder="제목을 입력하세요"
            required
          />
        </div>

        <div class="form-group">
          <label for="genre">장르</label>
          <select
            id="genre"
            v-model="form.genre"
            required
          >
            <option value="">장르를 선택하세요</option>
            <option value="로맨스">로맨스</option>
            <option value="판타지">판타지</option>
            <option value="SF(공상과학)">SF(공상과학)</option>
            <option value="추리/미스터리">추리/미스터리</option>
            <option value="호러(공포)">호러(공포)</option>
            <option value="무협">무협</option>
            <option value="역사/사극">역사/사극</option>
            <option value="현대물">현대물</option>
            <option value="학원물">학원물</option>
            <option value="직장물">직장물</option>
            <option value="기타">기타</option>
          </select>
        </div>

        <div v-if="!isEdit" class="form-group">
          <label for="next-story-count">다음 이야기 갯수</label>
          <input
            id="next-story-count"
            v-model.number="form.next_story_count"
            type="number"
            min="4"
            max="16"
            required
          />
          <span class="input-hint">최소 4개에서 최대 16개까지 선택 가능합니다</span>
        </div>

        <div class="form-group">
          <div class="content-header">
            <label for="content">내용</label>
            <button type="button" class="btn-ai-generate" @click="handleAIGenerate">
              AI로 생성하기
            </button>
          </div>
          <textarea
            id="content"
            v-model="form.content"
            placeholder="내용을 입력하세요"
            rows="15"
            required
          ></textarea>
        </div>

        <div class="form-actions">
          <button type="submit" class="btn-primary">
            {{ isEdit ? '수정 완료' : '작성 완료' }}
          </button>
          <router-link to="/posts" class="btn-primary cancel">취소</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/userStore'
import { usePostStore } from '@/stores/postStore'
import { Post } from '@/models'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const postStore = usePostStore()
const isEdit = ref(false)
const isLoading = ref(false)

const form = reactive({
  title: '',
  genre: '',
  content: '',
  next_story_count: 4,
})

onMounted(async () => {
  if (!userStore.user) {
    router.push('/login')
    return
  }

  // AI로 생성된 내용이 있으면 미리 입력
  if (route.query.aiContent) {
    form.content = route.query.aiContent
  }

  // 수정 모드인 경우
  if (route.params.id) {
    isEdit.value = true
    try {
      // await postStore.fetchPostDetail(route.params.id)
      // const post = postStore.currentPost
      // if (post.userId !== userStore.user.id) {
      //   alert('수정할 권한이 없습니다.')
      //   router.push('/posts')
      //   return
      // }
      // form.title = post.title
      // form.content = post.content
    } catch (error) {
      console.error('Failed to fetch post:', error)
      router.push('/posts')
    }
  }
})

const handleGoBack = () => {
  if (confirm('정말 뒤로 가시겠습니까? 작성 중인 내용은 저장되지 않습니다.')) {
    router.push('/posts')
  }
}

const handleAIGenerate = async () => {
  if (!form.title.trim()) {
    alert('제목을 입력한 후 AI 생성을 시도해주세요.')
    return
  }

  isLoading.value = true
  try {
    const generatedContent = await postStore.generateMainStory(form)
    form.content = generatedContent
    alert('AI가 내용을 생성했습니다.')
  } catch (error) {
    console.error('AI 생성 실패:', error)
    alert('AI 생성 실패: ' + error.message)
  } finally {
    isLoading.value = false
  }
}

const handleSubmit = async () => {
  if (!form.title.trim() || !form.content.trim()) {
    alert('제목과 내용을 입력하세요.')
    return
  }

  // Post 모델을 사용하여 게시물 생성
  const postData = {
    title: form.title,
    genre: form.genre,
    content: form.content,
    nickname: userStore.user?.nickname || '익명',
    user_id: userStore.user?.id,
    next_story_count: form.next_story_count
  }

  const post = Post.fromJSON(postData)

  try {
    if (isEdit.value) {
      // await postStore.updatePost(route.params.id, post.toJSON())
      // alert('글이 수정되었습니다.')
      // router.push(`/posts/${route.params.id}`)
    } else {
      const newPost = await postStore.createPost(post.toJSON())
      console.log(newPost)
      alert('글이 작성되었습니다.')
      router.push('/posts')
    }
  } catch (error) {
    console.error('Failed to submit post:', error)
    alert('요청 실패: ' + error.message)
  }
}
</script>

<style scoped>
.post-form-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  height: 100%;
}

.form-box {
  background: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

h1 {
  color: #333;
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 25px;
}

label {
  display: block;
  margin-bottom: 8px;
  color: #555;
  font-weight: 500;
}

input,
textarea,
select {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  font-family: inherit;
  box-sizing: border-box;
}

input:focus,
textarea:focus,
select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

textarea {
  resize: none;
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.input-hint {
  display: block;
  font-size: 12px;
  color: #999;
  margin-top: 6px;
}

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 30px;
}

.btn-primary.cancel {
  background-color: var(--cancel-color);
  text-decoration: none;
  text-align: center;
}

.btn-primary:hover {
    transform: scale(1.02);
}

/* 로딩 화면 스타일 */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.loading-spinner {
  background: white;
  padding: 40px;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}

.spinner {
  width: 50px;
  height: 50px;
  margin: 0 auto 20px;
  border: 4px solid #f0f0f0;
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading-spinner p {
  color: #333;
  font-size: 16px;
  font-weight: 500;
  margin: 0;
}

@media (max-width: 768px) {
  .form-box {
    padding: 20px;
  }

  h1 {
    font-size: 24px;
  }
}
</style>
