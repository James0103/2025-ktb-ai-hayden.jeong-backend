import { defineStore } from 'pinia'
import { ref } from 'vue'

const getAPIBaseURL = () => {
  const envURL = import.meta.env.VITE_API_BASE_URL
  if (envURL) {
    return envURL
  }

  if (import.meta.env.MODE === 'production') {
    // Railway production environment
    return import.meta.env.VITE_BACKEND_URL || 'https://relay-story-backend-production.up.railway.app'
  }

  console.log(import.meta.env.MODE)

  // Development environment
  return 'http://localhost:8000'
}

const API_BASE_URL = getAPIBaseURL()

// 배열의 내용을 하나의 문자열로 이어 붙이는 헬퍼 함수
const joinArrayToString = (array, separator = '\n') => {
  if (!Array.isArray(array)) {
    return ''
  }
  return array.map(item => {
    if (typeof item === 'object' && item !== null) {
      return item.content || JSON.stringify(item)
    }
    return String(item)
  }).join(separator)
}

export const usePostStore = defineStore('post', () => {
  const posts = ref([])
  const currentPost = ref(null)
  const loading = ref(false)

  const fetchPosts = async () => {
    loading.value = true
    try {
      const response = await fetch(`${API_BASE_URL}/api/posts?limit=1000`)

      if (!response.ok) {
        throw new Error('게시글 목록 조회 실패')
      }

      posts.value = await response.json()
      return posts.value
    } catch (error) {
      console.error('Failed to fetch posts:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const fetchPostDetail = async (postId) => {
    loading.value = true
    try {
      const response = await fetch(`${API_BASE_URL}/api/posts/${postId}`, {
        headers: {
          'Content-Type': 'application/json',
        },
      })

      if (!response.ok) {
        throw new Error('게시글 조회 실패')
      }

      currentPost.value = await response.json()
      return currentPost.value
    } catch (error) {
      console.error('Failed to fetch post detail:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const createPost = async (post) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/posts`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(post),
      })

      console.log(response)

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || '글 작성 실패')
      }

      const newPost = await response.json()
      posts.value.unshift(newPost)
      return newPost
    } catch (error) {
      console.error('Failed to create post:', error)
      throw error
    }
  }

  const updatePost = async (postId, title, content) => {
    try {
      const response = await fetch(`${API_BASE_URL}/posts/${postId}`, {
        method: 'PUT',
        body: JSON.stringify({ title, content }),
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || '글 수정 실패')
      }

      const updatedPost = await response.json()
      currentPost.value = updatedPost

      const index = posts.value.findIndex((p) => p.id === postId)
      if (index !== -1) {
        posts.value[index] = updatedPost
      }

      return updatedPost
    } catch (error) {
      console.error('Failed to update post:', error)
      throw error
    }
  }

  const deletePost = async (postId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/posts/${postId}`, {
        method: 'DELETE'
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || '글 삭제 실패')
      }

      posts.value = posts.value.filter((p) => p.id !== postId)
      currentPost.value = null
    } catch (error) {
      console.error('Failed to delete post:', error)
      throw error
    }
  }

  const addComment = async (postId, relayStory) => {
    try {
      // 백엔드에 맞게 필드명 변환 (camelCase → snake_case)
      const commentData = {
        content: relayStory.content,
        author: relayStory.author,
        post_id: relayStory.postId,
        user_id: relayStory.userId
      }

      const response = await fetch(`${API_BASE_URL}/api/posts/${postId}/comments`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(commentData),
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || '댓글 작성 실패')
      }

      return await response.json()
    } catch (error) {
      console.error('Failed to add comment:', error)
      throw error
    }
  }

  const deleteComment = async (postId, commentId) => {
    try {
      const response = await fetch(
        `${API_BASE_URL}/api/posts/${postId}/comments/${commentId}`,
        {
          method: 'DELETE',
        }
      )

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || '댓글 삭제 실패')
      }
    } catch (error) {
      console.error('Failed to delete comment:', error)
      throw error
    }
  }

  const generateMainStory = async (form) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/posts/generate-main-story`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(form),
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'AI 생성 실패')
      }

      const result = await response.json()
      return result
    } catch (error) {
      console.error('Failed to generate AI content:', error)
      throw error
    }
  }

  const generateRelayStory = async (post) => {
    const relayInfo = {
      title: post.title,
      content_story: joinArrayToString(post.comments),
      genre: post.genre,
      next_story_count: post.next_story_count,
      prev_story_count: post.comments.length
    }

    try {
      const response = await fetch(`${API_BASE_URL}/api/posts/generate-relay-story`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(relayInfo),
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'AI 생성 실패')
      }

      const result = await response.json()
      return result
    } catch (error) {
      console.error('Failed to generate AI content:', error)
      throw error
    }
  }

  const generateEndingContent = async (post) => {
    let prevContents = ""

    try {
      post.comments.length > 0 ?
      prevContents = joinArrayToString(post.comments.map((comment, index) => `${index + 1} : ${comment.content}`)) : ""

      if (prevContents == "") throw new Error('이전 내용이 없습니다.')

      const endingInfo = {
        title: post.title,
        first_contents: post.content,
        contents: prevContents,
        genre: post.genre
      }

      const response = await fetch(`${API_BASE_URL}/api/posts/generate-ending-content`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(endingInfo),
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'AI 생성 실패')
      }

      const result = await response.json()
      return result
    } catch (error) {
      console.error('Failed to generate AI content:', error)
      throw error
    }
  }

  return {
    posts,
    currentPost,
    loading,
    fetchPosts,
    fetchPostDetail,
    createPost,
    updatePost,
    deletePost,
    addComment,
    deleteComment,
    generateMainStory,
    generateRelayStory,
    generateEndingContent
  }
})
