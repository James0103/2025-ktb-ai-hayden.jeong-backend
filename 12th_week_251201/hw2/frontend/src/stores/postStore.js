import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getAllPosts, getPostDetail } from '@/api/index'

export const usePostStore = defineStore('post', () => {
  const posts = ref([])
  const currentPost = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const fetchPosts = async () => {
    loading.value = true
    error.value = null
    try {
      const resp = await getAllPosts()
      // console.log(resp.data)
      posts.value = Array.isArray(resp.data) ? resp.data : []
    } catch (err) {
      error.value = err.message
      console.error('Error fetching posts:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchPostDetail = async (postId) => {
    loading.value = true
    error.value = null
    try {
      const resp = await getPostDetail(postId)
      currentPost.value = Array.isArray(resp.data) ? resp.data[0] : []
    } catch (err) {
      error.value = err.message
      console.error('Error fetching post detail:', err)
    } finally {
      loading.value = false
    }
  }

  const getPostById = computed(() => (postId) => {
    return posts.value.find((post) => post.id === postId)
  })

  return {
    posts,
    currentPost,
    loading,
    error,
    fetchPosts,
    fetchPostDetail,
    getPostById,
  }
})
