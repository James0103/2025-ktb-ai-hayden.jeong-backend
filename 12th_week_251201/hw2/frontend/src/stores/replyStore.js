import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getAllReplies } from '@/api/index'

export const useReplyStore = defineStore('reply', () => {
  const replies = ref([])
  const loading = ref(false)
  const error = ref(null)

  const fetchReplies = async () => {
    loading.value = true
    error.value = null
    try {
      const resp = await getAllReplies()
      replies.value = Array.isArray(resp.data) ? resp.data : []
    } catch (err) {
      error.value = err.message
      console.error('Error fetching replies:', err)
    } finally {
      loading.value = false
    }
  }

  const getRepliesByPostId = computed(() => (postId) => {
    return replies.value.filter((reply) => reply.post_id === postId)
  })

  return {
    replies,
    loading,
    error,
    fetchReplies,
    getRepliesByPostId,
  }
})
