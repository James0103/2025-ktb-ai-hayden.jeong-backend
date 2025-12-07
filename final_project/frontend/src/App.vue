<script setup>
import { useUserStore } from '@/stores/userStore'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()

const handleLogout = () => {
  if (confirm('로그아웃 하시겠습니까?')) {
    userStore.logout()
    router.push('/login')
  }
}
</script>

<template>
  <header class="navbar" v-if="userStore.isLoggedIn">
    <div class="navbar-container">
      <router-link to="/posts" class="navbar-brand">아무글 대잔치</router-link>
      <nav class="navbar-menu">
        <router-link to="/posts" class="nav-link">홈</router-link>
        <!-- <router-link to="/posts/create" class="nav-link">글 작성</router-link> -->

        <!-- 프로필 드롭다운 -->
        <div class="profile-dropdown">
          <div class="profile-trigger">
            <img
              v-if="userStore.user?.profilePhoto"
              :src="userStore.user.profilePhoto"
              :alt="userStore.user?.nickname"
              class="profile-avatar"
            />
            <div v-else class="profile-avatar-placeholder">
              {{ userStore.user?.nickname?.charAt(0).toUpperCase() }}
            </div>
            <span class="profile-nickname">{{ userStore.user?.nickname }}</span>
          </div>

          <div class="profile-menu">
            <router-link to="/profile-edit" class="profile-menu-item">회원정보수정</router-link>
            <router-link to="/password-change" class="profile-menu-item">비밀번호수정</router-link>
            <button @click="handleLogout" class="profile-menu-item logout-item">로그아웃</button>
          </div>
        </div>
      </nav>
    </div>
  </header>
  <main>
    <router-view />
  </main>
</template>

<style scoped>
.navbar {
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.navbar-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 60px;
}

.navbar-brand {
  font-size: 24px;
  font-weight: 700;
  color: var(--primary-color);
  text-decoration: none;
  margin-right: 30px;
}

.navbar-menu {
  display: flex;
  gap: 20px;
  align-items: center;
}

.nav-link {
  color: #666;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background 0.2s;
  background: none;
  border: none;
  cursor: pointer;
}

.nav-link:hover {
  background: #f0f0f0;
}

.nav-link.router-link-active {
  color: var(--primary-color);
  font-weight: 600;
}

.logout-btn {
  border-radius: 4px;
  border: 1px solid var(--error-color);
  color: var(--error-color);
}

.logout-btn:hover {
  background-color: var(--error-color);
  color: white;
}

.profile-dropdown {
  position: relative;
  display: flex;
  align-items: center;
}

.profile-trigger {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.2s;
}

.profile-trigger:hover {
  background: #f0f0f0;
}

.profile-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
}

.profile-avatar-placeholder {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--primary-color);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
}

.profile-nickname {
  color: #666;
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
}

.profile-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  width: 150px;
  margin-top: 8px;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-8px);
  transition: all 0.2s ease;
  z-index: 1000;
}

.profile-dropdown:hover .profile-menu {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.profile-menu-item {
  box-sizing: border-box;
  display: block;
  width: 100%;
  padding: 12px 16px;
  text-align: left;
  color: #333;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  background: none;
  border: none;
  cursor: pointer;
  transition: background 0.2s;
}

.profile-menu-item:hover {
  background: #f5f5f5;
}

.profile-menu-item:not(:last-child) {
  border-bottom: 1px solid #f0f0f0;
}

.profile-menu-item.logout-item {
  color: var(--error-color);
}

.profile-menu-item.logout-item:hover {
  background: rgba(255, 59, 48, 0.05);
}

@media (max-width: 768px) {
  .navbar-container {
    flex-direction: column;
    gap: 10px;
    height: auto;
    padding: 15px 20px;
  }

  .navbar-brand {
    margin-right: 0;
  }

  .navbar-menu {
    width: 100%;
    flex-wrap: wrap;
    justify-content: center;
  }
}
</style>
