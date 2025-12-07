<template>
  <div class="posts-container">
    <header class="posts-header">
      <div class="header-actions">
        <router-link to="/posts/create" class="btn-create">글 작성</router-link>
      </div>
    </header>

    <div class="posts-list">
      <div v-if="postStore.posts.length === 0" class="empty-state">
        <p>아직 작성된 글이 없습니다.</p>
      </div>
      <div v-else class="post-cards">
        <div
          v-for="post in paginatedPosts"
          :key="post.id"
          @click="onClickPostCard(post)"
          class="post-card"
        >
          <div class="post-header">
            <h2>{{ post.title }}</h2>
            <span class="post-author">{{ post.author }}</span>
          </div>
          <p class="post-content">{{ post.content.substring(0, 150) }}...</p>
          <div class="post-meta">
            <span class="post-date">{{ formatDate(post.created_at) }}</span>
            <span class="post-comments">아무글 갯수: {{ post.comments.length }}</span>
          </div>
          <div class="btn-read">자세히 보기</div>
        </div>
      </div>

      <!-- 페이지네이션 -->
      <div v-if="totalPages > 1" class="pagination">
        <button
          @click="goToPage(currentPage - 1)"
          :disabled="currentPage === 1"
          class="pagination-btn"
        >
          이전
        </button>
        <button
          v-for="page in pageNumbers"
          :key="page"
          @click="goToPage(page)"
          :class="{ active: currentPage === page }"
          class="pagination-btn"
        >
          {{ page }}
        </button>
        <button
          @click="goToPage(currentPage + 1)"
          :disabled="currentPage === totalPages"
          class="pagination-btn"
        >
          다음
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { usePostStore } from '@/stores/postStore'
import { useRouter } from 'vue-router'

const postStore = usePostStore()
const router = useRouter()

const currentPage = ref(1)
const itemsPerPage = ref(6)

const onClickPostCard = (post) => {
  router.push(`/posts/${post.id}`)
}

// 페이지네이션을 위한 계산
const sortedPosts = computed(() => {
  return [...postStore.posts].sort((a, b) => {
    return new Date(b.created_at) - new Date(a.created_at)
  })
})

const paginatedPosts = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return sortedPosts.value.slice(start, end)
})

const totalPages = computed(() => {
  return Math.ceil(sortedPosts.value.length / itemsPerPage.value)
})

const pageNumbers = computed(() => {
  const pages = []
  for (let i = 1; i <= totalPages.value; i++) {
    pages.push(i)
  }
  return pages
})

onMounted(async () => {
  try {
    await postStore.fetchPosts()
  } catch (error) {
    console.error('Failed to fetch posts:', error)
  }
})

const goToPage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
  }
}

const formatDate = (date) => {
  const options = { year: 'numeric', month: '2-digit', day: '2-digit' }
  return new Date(date).toLocaleDateString('ko-KR', options)
}
</script>

<style scoped>
.posts-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.posts-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 2px solid #ddd;
}

.header-actions {
  width: 100%;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.btn-create {
  padding: 10px 20px;
  background: var(--primary-color);
  color: white;
  text-decoration: none;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-create:hover {
  transform: scale(1.05);
}

.posts-list {
  min-height: 400px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #999;
}

.post-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.post-card {
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px 20px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.post-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.1);
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.post-header h2 {
  max-width: 170px;
  margin: 0;
  color: #333;
  font-size: 18px;
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.post-author {
  background: #8c8c8c;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 10px;
  font-weight: bold;
  color: white;
  white-space: nowrap;
  margin-left: 8px;
}

.post-content {
  color: #666;
  font-size: 14px;
  line-height: 1.6;
  margin: 0 0 15px 0;
  display: -webkit-box;
  line-clamp: 3;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.post-meta {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #999;
  margin-bottom: 15px;
}

.btn-read {
  display: inline-block;
  padding: 8px 16px;
  background: var(--primary-color);
  color: white;
  text-decoration: none;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  margin-top: 40px;
  padding-top: 20px;
  border-top: 2px solid #f0f0f0;
}

.pagination-btn {
  padding: 8px 12px;
  background: white;
  color: var(--primary-color);
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.pagination-btn:hover:not(:disabled) {
  background: var(--primary-color);
  color: white;
}

.pagination-btn.active {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

.pagination-btn:disabled {
  background: #f5f5f5;
  color: #ccc;
  cursor: not-allowed;
  border-color: #ddd;
}

@media (max-width: 768px) {
  .posts-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }

  .post-cards {
    grid-template-columns: 1fr;
  }

  .pagination {
    flex-wrap: wrap;
  }

  .pagination-btn {
    padding: 6px 10px;
    font-size: 12px;
  }
}
</style>
