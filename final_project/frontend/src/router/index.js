import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/userStore'

// Pages
import LoginPage from '@/pages/LoginPage.vue'
import SignupPage from '@/pages/SignupPage.vue'
import ProfileEditPage from '@/pages/ProfileEditPage.vue'
import PasswordChangePage from '@/pages/PasswordChangePage.vue'
import PostsPage from '@/pages/PostsPage.vue'
import PostDetailPage from '@/pages/PostDetailPage.vue'
import CreateEditPostPage from '@/pages/CreateEditPostPage.vue'

const routes = [
  {
    path: '/',
    redirect: '/posts',
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginPage,
    meta: { requiresAuth: false },
  },
  {
    path: '/signup',
    name: 'Signup',
    component: SignupPage,
    meta: { requiresAuth: false },
  },
  {
    path: '/profile-edit',
    name: 'ProfileEdit',
    component: ProfileEditPage,
    meta: { requiresAuth: true },
  },
  {
    path: '/password-change',
    name: 'PasswordChange',
    component: PasswordChangePage,
    meta: { requiresAuth: true },
  },
  {
    path: '/posts',
    name: 'Posts',
    component: PostsPage,
    meta: { requiresAuth: true },
  },
  {
    path: '/posts/create',
    name: 'CreatePost',
    component: CreateEditPostPage,
    meta: { requiresAuth: true },
  },
  {
    path: '/posts/:id',
    name: 'PostDetail',
    component: PostDetailPage,
    meta: { requiresAuth: true },
  },
  {
    path: '/posts/:id/edit',
    name: 'EditPost',
    component: CreateEditPostPage,
    meta: { requiresAuth: true },
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

// Navigation Guards
router.beforeEach((to, _from, next) => {
  const userStore = useUserStore()

  // 인증이 필요한 페이지인 경우
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next('/login')
  }
  // 로그인/회원가입 페이지인데 이미 로그인한 경우
  else if ((to.path === '/login' || to.path === '/signup') && userStore.isLoggedIn) {
    next('/posts')
  } else {
    next()
  }
})

export default router
