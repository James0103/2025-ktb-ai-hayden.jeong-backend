<template>
  <div class="post-detail-container">
    <!-- 로딩 오버레이 -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-spinner">
        <div class="spinner"></div>
        <p>AI가 다음 이야기를 생성하고 있습니다...</p>
      </div>
    </div>

    <div v-if="post" class="post-detail">
      <div class="post-header">
        <div class="header-top">
          <router-link to="/posts" class="btn-back">
            <span class="material-symbols-outlined">chevron_backward</span>
          </router-link>
          <button v-if="userStore.user?.id === post.user_id" @click="handleDelete" class="btn-delete-header">
            전체 글 삭제
          </button>
        </div>
        <h1>{{ post.title }}</h1>
        <div class="post-info">
          <span class="author">{{ post.author }}</span>
          <span class="date">{{ formatDate(post.created_at) }}</span>
          <span class="next_story">전체 이야기수 : {{ post.next_story_count }}</span>
          <span class="genre">#{{ post.genre }}</span>
        </div>
      </div>

      <div class="post-content">
        {{ post.content }}
      </div>

      <div class="next-stories-section">
        <div v-if="post.comments?.length === 0" class="no-stories">
          <p>아직 다음 이야기가 없습니다.</p>
        </div>
        <div v-else class="stories-list">
          <div v-for="comment in post.comments" :key="comment.id" class="story">
            <p class="story-content">{{ comment.content }}</p>
            <div class="story-info">
              <strong>{{ comment.author }}</strong>
              <span class="story-date">{{ formatDate(comment.created_at) }}</span>
            </div>
            <div v-if="userStore.user?.id === comment.user_id" class="story-actions">
              <!-- <button @click="handleEditComment(comment)" class="btn-small">
                수정
              </button> -->
              <button @click="handleDeleteComment(comment.id)" class="btn-small">
                삭제
              </button>
            </div>
          </div>
        </div>
        <div class="divider"></div>
        <div v-if="getRemainingStories() > 0" class="stories-header">
          <h2>남은 이야기 ({{ getRemainingStories() }})</h2>
          <button @click="handleGenerateAI" class="btn-ai-generate-header">
            AI로 초안쓰기
          </button>
        </div>
        <div v-if="getRemainingStories() > 0" class="add-next-story">
          <textarea
            v-model="newStory"
            placeholder="다음 이야기를 작성하세요"
            rows="4"
          ></textarea>
          <button @click="handleAddComment" class="btn-primary">
            이야기 등록
          </button>
        </div>
        <div v-else class="no-remaining-stories">
          <p>이야기가 완성되었습니다 :)</p>
          <button @click="showFullStoryModal = true" class="btn-view-all">
            전체 이야기 보기
          </button>
        </div>
      </div>
    </div>

    <!-- 전체 이야기 모달 -->
    <div v-if="showFullStoryModal" class="modal-overlay" @click="showFullStoryModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>전체 이야기</h2>
          <button @click="showFullStoryModal = false" class="btn-close">
            <span class="material-symbols-outlined">close</span>
          </button>
        </div>
        <div class="modal-body">
          <div class="modal-post-content">
            <h3>{{ post.title }}</h3>
            <div class="modal-post-info">
              <span class="author">{{ post.author }}</span>
              <span class="date">{{ formatDate(post.created_at) }}</span>
            </div>
          </div>
          <div v-if="post.comments?.length > 0" class="modal-stories">
            <span>{{ post.content }}</span>
            <span v-for="comment in post.comments" :key="comment.id">
              {{ comment.content }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="loading">
      <p>로딩 중...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { usePostStore } from '@/stores/postStore'
import { useUserStore } from '@/stores/userStore'
import { RelayStory } from '@/models'

const route = useRoute()
const router = useRouter()
const postStore = usePostStore()
const userStore = useUserStore()

const post = ref(null)
const newStory = ref('')
const isLoading = ref(false)
const showFullStoryModal = ref(false)

onMounted(async () => {
  if (!userStore.user) {
    router.push('/login')
    return
  }
  try {
    await postStore.fetchPostDetail(route.params.id)
    post.value = postStore.currentPost
  } catch (error) {
    console.error('Failed to fetch post detail:', error)
    router.push('/posts')
  }
})

const formatDate = (date) => {
  const options = { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' }
  return new Date(date).toLocaleDateString('ko-KR', options)
}

const handleDelete = async () => {
  if (confirm('이 글을 삭제하시겠습니까?')) {
    try {
      await postStore.deletePost(post.value.id)
      alert('글이 삭제되었습니다.')
      router.push('/posts')
    } catch (error) {
      alert('삭제 실패: ' + error.message)
    }
  }
}

const handleAddComment = async () => {
  if (!newStory.value.trim()) {
    alert('다음 이야기를 입력하세요.')
    return
  }

  try {
    // RelayStory 모델을 사용하여 다음 이야기 생성
    const relayStory = new RelayStory({
      content: newStory.value,
      author: userStore.user?.nickname || '익명',
      userId: userStore.user?.id,
      postId: post.value.id,
      createdAt: new Date().toISOString()
    })
    await postStore.addComment(post.value.id, relayStory.toJSON())
    newStory.value = ''
    await postStore.fetchPostDetail(post.value.id)
    post.value = postStore.currentPost
    alert('다음 이야기가 등록되었습니다.')
  } catch (error) {
    console.error('Failed to add comment:', error)
    alert('다음 이야기 작성 실패: ' + error.message)
  }
}

// const handleEditComment = (comment) => {
//   newStory.value = comment.content
// }

const handleDeleteComment = async (commentId) => {
  if (confirm('이 다음 이야기를 삭제하시겠습니까?')) {
    try {
      await postStore.deleteComment(post.value.id, commentId)
      await postStore.fetchPostDetail(post.value.id)
      post.value = postStore.currentPost
    } catch (error) {
      alert('다음 이야기 삭제 실패: ' + error.message)
    }
  }
}

const getRemainingStories = () => {
  // post.nextStoryCount가 있으면 그 값에서 현재 댓글 수를 뺀 값, 없으면 현재 댓글 수만 표시
  const totalStories = post.value?.next_story_count || 0
  const currentStories = post.value?.comments?.length || 0
  return totalStories > 0 ? totalStories - currentStories : currentStories
}

const handleGenerateAI = async () => {
  isLoading.value = true

  const isEnding = post.value?.next_story_count - post.value?.comments.length == 1
  let contents = ''

  try {
    if (isEnding == false) {
      contents = await postStore.generateRelayStory(post.value)
    } else {
      contents = await postStore.generateEndingContent(post.value)
    }
    newStory.value = contents
  } catch (error) {
    alert('AI 생성 실패: ' + error.message)
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.post-detail-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.post-detail {
  background: white;
  border-radius: 8px;
  padding: 40px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.post-header {
  margin-bottom: 16px;
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 16px;
}

.header-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

h1 {
  margin: 15px 0;
  color: #333;
  font-size: 28px;
}

.btn-delete-header {
  padding: 8px 16px;
  background: transparent;
  color: var(--error-color);
  border: 1px solid var(--error-color);
  border-radius: 4px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-delete-header:hover {
  background: #ffe0e0;
}

.post-info {
  display: flex;
  flex-direction: column;
  align-items: end;
  gap: 4px;
  font-size: 14px;
  color: #666;
}

.author {
  font-weight: 600;
  color: var(--accent-color);
}

.post-info .genre {
  background-color: #999;
  padding: 6px;
  border-radius: 4px;
  color: white;
  font-weight: bold;
}

.post-content {
  color: #555;
  font-size: 16px;
  line-height: 1.8;
  margin-bottom: 30px;
  white-space: pre-wrap;
  word-break: break-word;
}

.post-actions {
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
  padding-bottom: 30px;
  border-bottom: 2px solid #f0f0f0;
}

.btn-edit,
.btn-delete {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
}

.btn-edit {
  background: #667eea;
  color: white;
}

.btn-edit:hover {
  background: #5568d3;
}

.btn-delete {
  background: #f5f5f5;
  color: #d32f2f;
  border: 1px solid #ddd;
}

.btn-delete:hover {
  background: #ffe0e0;
}

.next-stories-section {
  margin-top: 40px;
}

.stories-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 20px 0;
}

.stories-header h2 {
  color: #333;
  margin: 0;
}

.btn-ai-generate-header {
  padding: 8px 16px;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--warning-color) 100%);
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  filter: brightness(1);
}

.btn-ai-generate-header:hover {
  filter: brightness(1.1);
  transform: translateY(-2px);
}

.add-next-story {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
}

textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  font-family: inherit;
  resize: none;
  box-sizing: border-box;
}

textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.no-stories {
  text-align: center;
  padding: 40px 20px;
  color: #999;
}

.stories-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.story {
  background: #f8f9fa;
  padding: 16px;
  border-radius: 4px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
}

.story-info {
  flex: 1;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  justify-content: end;
  font-size: 14px;
}

.story-date {
  color: #999;
}

.story-content {
  width: 100%;
  flex: 3;
  color: #555;
  margin: 0;
  line-height: 1.6;
  font-size: 14px;
  font-weight: bold;
}

.story-actions {
  width: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: end;
  gap: 10px;
  margin-top: 10px;
}

.btn-small {
  padding: 4px 12px;
  background: white;
  color: #667eea;
  border: 1px solid #667eea;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
}

.btn-small:hover {
  background: #667eea;
  color: white;
}

.loading {
  text-align: center;
  padding: 60px 20px;
  color: #999;
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

.no-remaining-stories {
  text-align: center;
  padding: 40px 20px;
  background: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 30px;
}

.no-remaining-stories p {
  color: #666;
  margin: 0 0 20px 0;
  font-size: 16px;
}

.btn-view-all {
  padding: 12px 24px;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--warning-color) 100%);
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  filter: brightness(1);
}

.btn-view-all:hover {
  filter: brightness(1.1);
  transform: translateY(-2px);
}

/* 모달 스타일 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10000;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2);
  max-width: 800px;
  width: 100%;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #f0f0f0;
}

.modal-header h2 {
  margin: 0;
  color: #333;
  font-size: 24px;
}

.btn-close {
  background: transparent;
  border: none;
  color: #666;
  font-size: 24px;
  cursor: pointer;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  transition: all 0.2s;
}

.btn-close:hover {
  color: #333;
  background: #f0f0f0;
  border-radius: 4px;
}

.modal-body {
  padding: 30px;
  overflow-y: auto;
}

.modal-post-content {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid #f0f0f0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.modal-post-content h3 {
  margin: 0 0 15px 0;
  color: #333;
  font-size: 22px;
}

.modal-post-info {
  display: flex;
  gap: 15px;
  margin-bottom: 15px;
  font-size: 14px;
  color: #666;
}

.modal-post-info .author {
  font-weight: 600;
  color: var(--accent-color);
}

.modal-content {
  color: #555;
  font-size: 16px;
  line-height: 1.8;
  white-space: pre-wrap;
  word-break: break-word;
}

.modal-stories h3 {
  margin: 0 0 15px 0;
  color: #333;
  font-size: 18px;
}

.modal-stories {
  display: flex;
  flex-direction: column;
  padding: 16px;
  margin-bottom: 16px;
}

.modal-story-content {
  color: #555;
  margin: 0 0 10px 0;
  line-height: 1.6;
  font-size: 14px;
}

.modal-story-info {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #999;
}

.modal-story-date {
  color: #999;
}
</style>
