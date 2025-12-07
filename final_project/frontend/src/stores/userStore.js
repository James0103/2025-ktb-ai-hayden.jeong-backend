import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { User } from '@/models'

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

export const useUserStore = defineStore('user', () => {
  const user = ref(null)

  const isLoggedIn = computed(() => !!user.value)

  // 초기화 시 저장된 사용자 정보 복원
  try {
    const savedUser = localStorage.getItem('user')
    if (savedUser) {
      user.value = User.fromJSON(JSON.parse(savedUser))
    }
  } catch (error) {
    console.error('Failed to restore user:', error)
    localStorage.removeItem('user')
  }

  const login = async (email, password) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/users/sign-in`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({'email': email, 'password': password }),
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.message)
      }

      const data = await response.json()
      // token.value = data.access_token
      user.value = User.fromJSON(data)

      // localStorage.setItem('token', token.value)
      localStorage.setItem('user', JSON.stringify(user.value.toJSON()))

      return user.value
    } catch (error) {
      logout()
      throw error
    }
  }

  const signup = async (form) => {
    const formData = new FormData()
    formData.append('nickname', form.nickname)
    formData.append('email', form.email)
    formData.append('password', form.password)
    if (form.profilePhoto) {
      formData.append('profile_img_file', form.profilePhoto)
    }

    try {
      const resp = await fetch(`${API_BASE_URL}/api/users/sign-up`, {
        method: 'POST',
        body: formData
      })
      if (resp.status !== 200) {
        throw Error()
      } else {
        return true
      }
    } catch (error) {
      console.error(error)
      throw error
    }
  }

  const updateProfile = async (nickname, password, profile_photo) => {
    try {
      const formData = new FormData()
      if (nickname != null) {
        formData.append('nickname', nickname)
      }
      if (password != null) {
        formData.append('password', password)
      }
      if (profile_photo) {
        formData.append('profile_img_file', profile_photo)
      }

      const response = await fetch(`${API_BASE_URL}/api/users/${user.value.id}`, {
        method: 'PUT',
        body: formData
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || '수정 실패')
      }

      const updatedUserData = await response.json()
      console.log(updatedUserData)
      user.value = User.fromJSON(updatedUserData)
      localStorage.setItem('user', JSON.stringify(user.value.toJSON()))

      return user.value
    } catch (error) {
      console.error(error)
      throw error
    }
  }

  const logout = () => {
    user.value = null
    // token.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  return {
    user,
    // token,
    isLoggedIn,
    login,
    signup,
    updateProfile,
    logout,
  }
})
