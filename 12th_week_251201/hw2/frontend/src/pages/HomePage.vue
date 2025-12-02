<script setup>
import { onMounted, computed } from 'vue'
import Header from '@/components/Header.vue'
// import UserCard from '@/components/UserCard.vue'
import PostCard from '@/components/PostCard.vue'
import { usePostStore } from '@/stores/postStore'

const postStore = usePostStore()

const loading = computed(() => postStore.loading)

onMounted(async () => {
  await postStore.fetchPosts()
})
</script>

<template>
  <div class="home-page">
    <Header />
    <main class="main-content">
      <div class="container">
        <!-- Loading State -->
        <div class="loading" v-if="loading">
          <p>Loading...</p>
        </div>

        <!-- Error State -->
        <div class="error" v-else-if="postStore.error">
          <p>{{ postStore.error }}</p>
        </div>

        <!-- Content -->
        <template v-else>
          <!-- Posts Section -->
          <section class="section">
            <h2 class="section-title">Posts</h2>
            <div class="posts-list" v-if="postStore.posts.length > 0">
              <PostCard v-for="post in postStore.posts" :key="post.id" :post="post" />
            </div>
            <p v-else class="empty-message">No posts found</p>
          </section>
        </template>
      </div>
    </main>
  </div>
</template>

<style scoped>
.home-page {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.main-content {
  padding: 2rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.section {
  margin-bottom: 3rem;
}

.section-title {
  margin: 0 0 1.5rem 0;
  font-size: 1.75rem;
  font-weight: 700;
  color: #333;
  border-bottom: 2px solid #0066cc;
  padding-bottom: 0.5rem;
}

.users-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.posts-list {
  display: flex;
  flex-direction: column;
}

.loading,
.error {
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

.error {
  color: #d32f2f;
  background-color: #ffebee;
  border-color: #f44336;
}

.empty-message {
  padding: 2rem;
  text-align: center;
  color: #999;
  font-size: 1rem;
}
</style>
