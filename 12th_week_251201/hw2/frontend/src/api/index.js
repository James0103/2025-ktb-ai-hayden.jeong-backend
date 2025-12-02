import apiClient from './client'

// 사용자 API
export const getAllUsers = async () => {
  try {
    const response = await apiClient.get('/api/all_users')
    return response.data
  } catch (error) {
    console.error('Failed to fetch users:', error)
    throw error
  }
}

// 게시글 API
export const getAllPosts = async () => {
  try {
    const response = await apiClient.get('/api/all_posts')
    return response.data
  } catch (error) {
    console.error('Failed to fetch posts:', error)
    throw error
  }
}

export const getPostDetail = async (postId) => {
  try {
    const response = await apiClient.get('/api/post', {
      params: { post_id: postId },
    })
    return response.data
  } catch (error) {
    console.error('Failed to fetch post detail:', error)
    throw error
  }
}

// 댓글 API
export const getAllReplies = async () => {
  try {
    const response = await apiClient.get('/api/all_replies')
    return response.data
  } catch (error) {
    console.error('Failed to fetch replies:', error)
    throw error
  }
}
