<script setup>
defineProps({
  reply: {
    type: Object,
    required: true,
  },
})
</script>

<template>
  <div class="reply-item">
    <div class="reply-header">
      <span class="reply-author">{{ reply.author }}</span>
      <span class="reply-date">{{ reply.last_upload_at }}</span>
    </div>
    <p class="reply-contents">{{ reply.contents }}</p>
  </div>
</template>

<style scoped>
.reply-item {
  padding: 1rem;
  border-left: 3px solid #0066cc;
  background-color: #f9f9f9;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.reply-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.reply-author {
  font-weight: 600;
  color: #333;
  font-size: 0.95rem;
}

.reply-date {
  font-size: 0.75rem;
  color: #999;
}

.reply-contents {
  margin: 0.5rem 0 0 0;
  color: #555;
  line-height: 1.5;
}
</style>
