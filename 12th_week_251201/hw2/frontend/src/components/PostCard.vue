<script setup>
import { useRouter } from 'vue-router'


const props = defineProps({
  post: {
    type: Object,
    required: true,
  },
})

const router = useRouter()

const goToDetail = () => {
  router.push({ name: 'postDetail', params: { postId: props.post.id } })
}
</script>

<template>
  <div class="post-card" @click="goToDetail">
    <div class="post-header">
      <h2 class="post-title">{{ post.title }}</h2>
      <span class="post-author">by {{ post.author }}</span>
    </div>

    <div class="post-image" v-if="post.img">
      <img :src="post.img" :alt="post.title" />
    </div>

    <p class="post-contents" v-if="post.contents">{{ post.contents }}</p>

    <div class="post-stats">
      <span class="stat">👁 {{ post.view_count }}</span>
      <span class="stat">❤️ {{ post.like_count }}</span>
      <span class="stat">💬 {{ post.reply_count }}</span>
    </div>

    <p class="post-date">{{ post.last_upload_at }}</p>
  </div>
</template>

<style scoped>
.post-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  cursor: pointer;
  transition: box-shadow 0.3s ease, transform 0.3s ease;
}

.post-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
  gap: 1rem;
}

.post-title {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 700;
  color: #333;
  flex: 1;
}

.post-author {
  font-size: 0.875rem;
  color: #666;
  white-space: nowrap;
}

.post-image {
  margin: 1rem 0;
  border-radius: 8px;
  overflow: hidden;
  max-height: 300px;
}

.post-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.post-contents {
  margin: 1rem 0;
  color: #555;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.post-stats {
  display: flex;
  gap: 1.5rem;
  margin: 1rem 0;
  padding: 0.5rem 0;
  border-top: 1px solid #eee;
  border-bottom: 1px solid #eee;
}

.stat {
  font-size: 0.875rem;
  color: #666;
}

.post-date {
  margin: 0.5rem 0 0 0;
  font-size: 0.75rem;
  color: #999;
}
</style>
