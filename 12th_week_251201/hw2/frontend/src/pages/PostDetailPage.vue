<script setup>
import { onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import Header from '@/components/Header.vue'
import ReplyItem from '@/components/ReplyItem.vue'
import { usePostStore } from '@/stores/postStore'
import { useReplyStore } from '@/stores/replyStore'

const router = useRouter()
const postStore = usePostStore()
const replyStore = useReplyStore()

const postId = computed(() => router.currentRoute.value.params.postId)
const loading = computed(() => postStore.loading || replyStore.loading)

const postReplies = computed(() => {
  return replyStore.getRepliesByPostId(postId.value)
})

onMounted(async () => {
  await Promise.all([
    postStore.fetchPostDetail(postId.value),
    replyStore.fetchReplies(),
  ])
})
</script>

<template>
  <div class="post-detail-page">
    <Header />
    <main class="main-content">
      <div class="container">
        <!-- Loading State -->
        <div class="loading" v-if="loading">
          <p>Loading...</p>
        </div>

        <!-- Error State -->
        <div class="error" v-else-if="postStore.error || replyStore.error">
          <p>{{ postStore.error || replyStore.error }}</p>
        </div>

        <!-- Post Detail -->
        <template v-else-if="postStore.currentPost">
          <article class="post-detail">
            <div class="post-header">
              <h1 class="post-title">{{ postStore.currentPost.title }}</h1>
              <div class="post-meta">
                <span class="post-author">{{ postStore.currentPost.author }}</span>
                <span class="post-date">{{ postStore.currentPost.last_upload_at }}</span>
              </div>
            </div>

            <div class="post-image" v-if="postStore.currentPost.img">
              <img :src="postStore.currentPost.img" :alt="postStore.currentPost.title" />
            </div>

            <div class="post-body">
              <p class="post-contents">{{ postStore.currentPost.contents }}</p>
            </div>

            <div class="post-stats">
              <span class="stat">👁 {{ postStore.currentPost.view_count }} views</span>
              <span class="stat">❤️ {{ postStore.currentPost.like_count }} likes</span>
              <span class="stat">💬 {{ postReplies.length }} replies</span>
            </div>
          </article>

          <!-- Replies Section -->
          <section class="replies-section">
            <h2 class="replies-title">Replies</h2>
            <div class="replies-list" v-if="postReplies.length > 0">
              <ReplyItem v-for="reply in postReplies" :key="reply.id" :reply="reply" />
            </div>
            <p v-else class="empty-message">No replies yet</p>
          </section>
        </template>

        <!-- Post Not Found -->
        <div v-else class="not-found">
          <p>Post not found</p>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.post-detail-page {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.main-content {
  padding: 2rem 0;
}

.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 1rem;
}

.post-detail {
  background-color: #fff;
  border-radius: 8px;
  padding: 2rem;
  margin-bottom: 2rem;
}

.post-header {
  margin-bottom: 1.5rem;
  border-bottom: 1px solid #ddd;
  padding-bottom: 1.5rem;
}

.post-title {
  margin: 0 0 0.5rem 0;
  font-size: 2rem;
  font-weight: 700;
  color: #333;
}

.post-meta {
  display: flex;
  gap: 1rem;
  align-items: center;
  font-size: 0.95rem;
  color: #666;
}

.post-author {
  font-weight: 600;
}

.post-date {
  color: #999;
  font-size: 0.875rem;
}

.post-image {
  margin: 1.5rem 0;
  border-radius: 8px;
  overflow: hidden;
  max-height: 500px;
}

.post-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.post-body {
  margin: 1.5rem 0;
}

.post-contents {
  margin: 0;
  color: #555;
  line-height: 1.8;
  font-size: 1rem;
}

.post-stats {
  display: flex;
  gap: 2rem;
  padding: 1rem 0;
  border-top: 1px solid #ddd;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
}

.stat {
  font-size: 0.95rem;
  color: #666;
}

.replies-section {
  background-color: #fff;
  border-radius: 8px;
  padding: 2rem;
}

.replies-title {
  margin: 0 0 1.5rem 0;
  font-size: 1.5rem;
  font-weight: 700;
  color: #333;
}

.replies-list {
  display: flex;
  flex-direction: column;
}

.loading,
.error,
.not-found {
  padding: 2rem;
  text-align: center;
  border-radius: 8px;
  background-color: #fff;
  border: 1px solid #ddd;
}

.loading {
  color: #0066cc;
  font-weight: 500;
}

.error,
.not-found {
  color: #d32f2f;
  background-color: #ffebee;
  border-color: #f44336;
}

.empty-message {
  padding: 2rem;
  text-align: center;
  color: #999;
  font-size: 1rem;
  margin: 0;
}
</style>
