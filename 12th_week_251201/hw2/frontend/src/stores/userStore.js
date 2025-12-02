import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getAllUsers } from '@/api/index'

export const useUserStore = defineStore('user', () => {
  const users = ref([])
  const loading = ref(false)
  const error = ref(null)

  const fetchUsers = async () => {
    loading.value = true
    error.value = null
    try {
      const data = await getAllUsers()
      users.value = Array.isArray(data) ? data : []
    } catch (err) {
      error.value = err.message
      console.error('Error fetching users:', err)
    } finally {
      loading.value = false
    }
  }

  const getUserById = computed(() => (userId) => {
    return users.value.find((user) => user.id === userId)
  })

  return {
    users,
    loading,
    error,
    fetchUsers,
    getUserById,
  }
})
