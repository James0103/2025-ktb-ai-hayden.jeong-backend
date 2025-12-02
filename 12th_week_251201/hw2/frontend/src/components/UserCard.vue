<script setup>
defineProps({
  user: {
    type: Object,
    required: true,
  },
})
</script>

<template>
  <div class="user-card">
    <div class="user-avatar" v-if="user.profile_image">
      <img :src="user.profile_image" :alt="user.nickname" />
    </div>
    <div class="user-avatar placeholder" v-else>
      {{ user.nickname.charAt(0).toUpperCase() }}
    </div>
    <div class="user-info">
      <h3 class="user-nickname">{{ user.nickname }}</h3>
      <p class="user-email">{{ user.email }}</p>
    </div>
  </div>
</template>

<style scoped>
.user-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  transition: box-shadow 0.3s ease;
}

.user-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.user-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
}

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-avatar.placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-weight: 700;
  font-size: 1.2rem;
}

.user-info {
  flex: 1;
}

.user-nickname {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #333;
}

.user-email {
  margin: 0.25rem 0 0 0;
  font-size: 0.875rem;
  color: #666;
}
</style>
