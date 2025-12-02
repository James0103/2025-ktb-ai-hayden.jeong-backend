<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goHome = () => {
  router.push({ name: 'home' })
}
</script>

<template>
  <header class="header">
    <div class="header-container">
      <h1 class="logo" @click="goHome">SNS Platform</h1>
      <nav class="nav">
        <router-link to="/" class="nav-link">Home</router-link>
      </nav>
    </div>
  </header>
</template>

<style scoped>
.header {
  background-color: #fff;
  border-bottom: 1px solid #ddd;
  padding: 1rem 0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
  color: #333;
  cursor: pointer;
  transition: color 0.3s ease;
}

.logo:hover {
  color: #0066cc;
}

.nav {
  display: flex;
  gap: 2rem;
}

.nav-link {
  text-decoration: none;
  color: #333;
  font-weight: 500;
  transition: color 0.3s ease;
}

.nav-link:hover {
  color: #0066cc;
}
</style>
