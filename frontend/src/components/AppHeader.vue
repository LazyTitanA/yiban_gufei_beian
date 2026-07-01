<template>
  <header class="app-header">
    <div class="header-top">
      <div class="container header-top-inner">
        <span class="header-welcome">欢迎访问青海省一般工业固体废物跨省转移备案系统</span>
        <div class="header-links">
          <template v-if="user">
            <span class="header-user">{{ user.enterprise_name || user.username }}</span>
            <router-link v-if="user.is_staff" to="/review" class="header-admin-link">审核管理</router-link>
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
        <button class="menu-toggle" @click="menuOpen = !menuOpen" :aria-label="menuOpen ? '关闭菜单' : '打开菜单'">
          <span :class="{ 'open': menuOpen }"></span>
        </button>
        <nav class="header-nav" :class="{ 'nav-open': menuOpen }">
          <router-link to="/" class="nav-item" active-class="nav-active" @click="menuOpen = false">首页</router-link>
          <router-link to="/apply" class="nav-item" active-class="nav-active" @click="menuOpen = false">在线申请</router-link>
          <router-link to="/applications" class="nav-item" active-class="nav-active" @click="menuOpen = false">我的申请</router-link>
          <router-link to="/guide" class="nav-item" active-class="nav-active" @click="menuOpen = false">办事指南</router-link>
          <div class="nav-user-mobile">
            <template v-if="user">
              <div class="nav-user-name">{{ user.enterprise_name || user.username }}</div>
              <a href="#" class="nav-logout" @click.prevent="logout; menuOpen = false">退出登录</a>
            </template>
            <template v-else>
              <router-link to="/login" class="nav-login-btn" @click="menuOpen = false">企业登录</router-link>
              <router-link to="/register" class="nav-register-btn" @click="menuOpen = false">企业注册</router-link>
            </template>
          </div>
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
const menuOpen = ref(false)

onMounted(async () => {
  const stored = localStorage.getItem('user')
  if (stored) {
    try { user.value = JSON.parse(stored) } catch (e) { /* ignore */ }
  }
  if (localStorage.getItem('token')) {
    try {
      const res = await getMe()
      user.value = {
        enterprise_name: res.data.enterprise?.enterprise_name || '',
        username: res.data.username,
        is_staff: res.data.is_staff || false,
      }
      localStorage.setItem('user', JSON.stringify(user.value))
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

.header-admin-link {
  background: rgba(255,255,255,0.2);
  padding: 4px 12px;
  border-radius: 3px;
  font-size: 12px;
  font-weight: 500;
}

.header-admin-link:hover {
  background: rgba(255,255,255,0.3);
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
  .header-top {
    font-size: 11px;
    padding: 4px 0;
  }

  .header-top-inner {
    flex-direction: column;
    gap: 2px;
    text-align: center;
  }

  .header-welcome {
    font-size: 11px;
    line-height: 1.3;
  }

  .header-links {
    gap: 12px;
    font-size: 12px;
  }

  .header-main-inner {
    position: relative;
    padding: 12px 0;
  }

  .header-logo {
    gap: 10px;
  }

  .logo-emblem {
    width: 40px;
    height: 40px;
  }

  .logo-title {
    font-size: 15px;
  }

  .logo-subtitle {
    font-size: 11px;
  }

  .menu-toggle {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 40px;
    height: 40px;
    background: none;
    border: none;
    cursor: pointer;
    padding: 0;
    z-index: 200;
  }

  .menu-toggle span {
    display: block;
    width: 22px;
    height: 2px;
    background: var(--primary);
    position: relative;
    transition: all 0.3s;
  }

  .menu-toggle span::before,
  .menu-toggle span::after {
    content: '';
    position: absolute;
    left: 0;
    width: 100%;
    height: 2px;
    background: var(--primary);
    transition: all 0.3s;
  }

  .menu-toggle span::before {
    top: -7px;
  }

  .menu-toggle span::after {
    top: 7px;
  }

  .menu-toggle span.open {
    background: transparent;
  }

  .menu-toggle span.open::before {
    top: 0;
    transform: rotate(45deg);
  }

  .menu-toggle span.open::after {
    top: 0;
    transform: rotate(-45deg);
  }

  .header-nav {
    position: fixed;
    top: 0;
    right: -100%;
    width: 75%;
    max-width: 280px;
    height: 100vh;
    background: #FFFFFF;
    flex-direction: column;
    align-items: stretch;
    gap: 0;
    padding: 70px 0 var(--space-lg);
    box-shadow: -4px 0 16px rgba(0,0,0,0.1);
    transition: right 0.3s ease;
    z-index: 150;
    overflow-y: auto;
  }

  .header-nav.nav-open {
    right: 0;
  }

  .nav-item {
    padding: 16px var(--space-lg);
    border-radius: 0;
    border-bottom: 1px solid var(--border-light);
    font-size: 15px;
  }

  .nav-item:first-child {
    border-top: 1px solid var(--border-light);
  }

  .nav-active {
    background: var(--primary-bg);
    color: var(--primary);
  }

  .nav-user-mobile {
    padding: var(--space-lg);
    margin-top: var(--space-md);
    border-top: 8px solid var(--bg-gray);
  }

  .nav-user-name {
    font-size: 14px;
    color: var(--text-secondary);
    margin-bottom: var(--space-sm);
  }

  .nav-logout {
    display: block;
    color: var(--accent);
    font-size: 14px;
    padding: 10px 0;
  }

  .nav-login-btn,
  .nav-register-btn {
    display: block;
    text-align: center;
    padding: 12px;
    border-radius: var(--radius);
    margin-bottom: var(--space-sm);
    font-size: 14px;
  }

  .nav-login-btn {
    background: var(--primary);
    color: #FFFFFF;
  }

  .nav-register-btn {
    border: 1px solid var(--primary);
    color: var(--primary);
  }

  .header-links {
    display: none;
  }
}

@media (max-width: 768px) and (min-width: 1px) {
  .menu-toggle {
    display: flex;
  }
}

@media (min-width: 769px) {
  .menu-toggle {
    display: none;
  }

  .nav-user-mobile {
    display: none;
  }
}
</style>