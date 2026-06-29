<template>
  <header class="app-header">
    <div class="header-top">
      <div class="container header-top-inner">
        <span class="header-welcome">欢迎访问青海省一般工业固体废物跨省转移备案系统</span>
        <div class="header-links">
          <template v-if="user">
            <span class="header-user">{{ user.enterprise_name || user.username }}</span>
            <a href="#" @click.prevent="logout">退出登录</a>
          </template>
          <template v-else>
            <router-link to="/login">企业登录</router-link>
            <router-link to="/register">企业注册</router-link>
          </template>
        </div>
      </div>
    </div>
    <div class="header-main">
      <div class="container header-main-inner">
        <router-link to="/" class="header-logo">
          <img src="/src/assets/logo.png" alt="青海固废备案" class="logo-emblem" />
          <div class="logo-text">
            <div class="logo-title">青海省一般工业固体废物</div>
            <div class="logo-subtitle">跨省转移备案系统</div>
          </div>
        </router-link>
        <nav class="header-nav">
          <router-link to="/" class="nav-item" active-class="nav-active">首页</router-link>
          <router-link to="/apply" class="nav-item" active-class="nav-active">在线申请</router-link>
          <router-link to="/applications" class="nav-item" active-class="nav-active">我的申请</router-link>
          <router-link to="/guide" class="nav-item" active-class="nav-active">办事指南</router-link>
        </nav>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getMe } from '../api'

const router = useRouter()
const user = ref(null)

onMounted(async () => {
  const stored = localStorage.getItem('user')
  if (stored) {
    try { user.value = JSON.parse(stored) } catch (e) { /* ignore */ }
  }
  // 尝试从后端获取最新用户信息
  if (localStorage.getItem('token')) {
    try {
      const res = await getMe()
      if (res.data.enterprise) {
        user.value = {
          enterprise_name: res.data.enterprise.enterprise_name,
          username: res.data.username,
        }
        localStorage.setItem('user', JSON.stringify(user.value))
      }
    } catch (e) { /* token 过期 */ }
  }
})

function logout() {
  localStorage.removeItem('user')
  localStorage.removeItem('token')
  user.value = null
  router.push('/')
}
</script>

<style scoped>
.app-header {
  background: #FFFFFF;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  position: sticky;
  top: 0;
  z-index: 100;
}

/* 顶部栏 */
.header-top {
  background: var(--primary);
  color: rgba(255,255,255,0.85);
  font-size: 13px;
  padding: 6px 0;
}

.header-top-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-links {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-links a {
  color: rgba(255,255,255,0.85);
  font-size: 13px;
}

.header-links a:hover {
  color: #FFFFFF;
}

.header-user {
  color: rgba(255,255,255,0.7);
}

/* 主导航 */
.header-main {
  border-bottom: 3px solid var(--primary);
}

.header-main-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 0;
}

.header-logo {
  display: flex;
  align-items: center;
  gap: 14px;
  text-decoration: none;
}

.logo-emblem {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
}

.logo-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--primary);
  line-height: 1.3;
}

.logo-subtitle {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.3;
}

.header-nav {
  display: flex;
  align-items: center;
  gap: 4px;
}

.nav-item {
  padding: 8px 20px;
  font-size: 15px;
  color: var(--text);
  border-radius: var(--radius);
  transition: all 0.2s;
  text-decoration: none;
  font-weight: 500;
}

.nav-item:hover {
  background: var(--primary-bg);
  color: var(--primary);
}

.nav-active {
  background: var(--primary);
  color: #FFFFFF;
}

.nav-active:hover {
  background: var(--primary-light);
  color: #FFFFFF;
}

@media (max-width: 768px) {
  .header-top-inner {
    flex-direction: column;
    gap: 4px;
    text-align: center;
  }

  .header-main-inner {
    flex-direction: column;
    gap: 12px;
  }

  .header-nav {
    flex-wrap: wrap;
    justify-content: center;
  }

  .nav-item {
    padding: 6px 14px;
    font-size: 14px;
  }
}
</style>