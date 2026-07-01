import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  { path: '/', name: 'Home', component: HomeView, meta: { title: '首页 - 青海省一般工业固体废物跨省转移备案系统' } },
  { path: '/login', name: 'Login', component: () => import('../views/LoginView.vue'), meta: { title: '企业登录' } },
  { path: '/register', name: 'Register', component: () => import('../views/RegisterView.vue'), meta: { title: '企业注册' } },
  { path: '/apply', name: 'Apply', component: () => import('../views/ApplyView.vue'), meta: { title: '在线申请', requiresAuth: true } },
  { path: '/applications', name: 'Applications', component: () => import('../views/ApplicationsView.vue'), meta: { title: '我的申请', requiresAuth: true } },
  { path: '/application/:id', name: 'ApplicationDetail', component: () => import('../views/ApplicationDetailView.vue'), meta: { title: '申请详情', requiresAuth: true } },
  { path: '/review', name: 'Review', component: () => import('../views/ReviewView.vue'), meta: { title: '人工审核', requiresAuth: true } },
  { path: '/guide', name: 'Guide', component: () => import('../views/GuideView.vue'), meta: { title: '办事指南' } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})

router.beforeEach((to, from, next) => {
  document.title = to.meta.title || '青海省一般工业固体废物跨省转移备案系统'
  if (to.meta.requiresAuth) {
    const token = localStorage.getItem('token')
    if (!token) {
      next('/login')
      return
    }
  }
  if (to.path === '/review') {
    const userStr = localStorage.getItem('user')
    let user = null
    try { user = JSON.parse(userStr) } catch (e) { /* ignore */ }
    if (!user || !user.is_staff) {
      alert('您没有权限访问此页面')
      next('/')
      return
    }
  }
  next()
})

export default router