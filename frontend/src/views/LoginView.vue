<template>
  <div class="login-page">
    <div class="page-container">
      <div class="login-wrapper">
        <div class="login-card">
          <div class="login-header">
            <h1>企业登录</h1>
            <p>青海省一般工业固体废物跨省转移备案系统</p>
          </div>
          <div class="login-body">
            <div class="form-group">
              <label class="form-label">企业账号 <span class="required">*</span></label>
              <input
                v-model="form.username"
                type="text"
                class="form-input"
                placeholder="请输入统一社会信用代码或注册账号"
              />
            </div>
            <div class="form-group">
              <label class="form-label">登录密码 <span class="required">*</span></label>
              <input
                v-model="form.password"
                type="password"
                class="form-input"
                placeholder="请输入登录密码"
                @keyup.enter="handleLogin"
              />
            </div>
            <div class="form-group flex-between">
              <label class="remember-label">
                <input type="checkbox" v-model="remember" /> 记住登录状态
              </label>
              <a href="#" class="text-sm">忘记密码？</a>
            </div>
            <button class="btn btn-primary btn-lg login-btn" @click="handleLogin" :disabled="loading">
              {{ loading ? '登录中...' : '登 录' }}
            </button>
            <div class="login-footer">
              还没有账号？<router-link to="/register">立即注册</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '../api'

const router = useRouter()
const loading = ref(false)
const remember = ref(false)
const form = reactive({
  username: '',
  password: '',
})

async function handleLogin() {
  if (!form.username || !form.password) {
    alert('请输入账号和密码')
    return
  }
  loading.value = true
  try {
    const res = await login({ ...form })
    localStorage.setItem('token', res.data.access)
    localStorage.setItem('user', JSON.stringify(res.data.user))
    if (res.data.user.is_staff) {
      router.push('/review')
    } else {
      router.push('/apply')
    }
  } catch (e) {
    // 错误已由拦截器处理
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: calc(100vh - 200px);
  display: flex;
  align-items: center;
  background: var(--bg-gray);
}

.login-wrapper {
  max-width: 440px;
  margin: 0 auto;
  width: 100%;
}

.login-card {
  background: var(--bg);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  overflow: hidden;
}

.login-header {
  background: linear-gradient(135deg, var(--primary-dark), var(--primary));
  padding: var(--space-2xl) var(--space-xl) var(--space-xl);
  text-align: center;
  color: #FFFFFF;
}

.login-header h1 {
  font-size: 22px;
  font-weight: 600;
  color: #FFFFFF;
  margin: 0 0 var(--space-xs);
}

.login-header p {
  font-size: 13px;
  color: rgba(255,255,255,0.7);
}

.login-body {
  padding: var(--space-xl);
}

.remember-label {
  font-size: 13px;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: var(--space-xs);
  cursor: pointer;
}

.login-btn {
  width: 100%;
  margin-top: var(--space-md);
  padding: 14px;
  font-size: 16px;
}

.login-footer {
  text-align: center;
  margin-top: var(--space-lg);
  font-size: 14px;
  color: var(--text-secondary);
}

.login-footer a {
  color: var(--primary);
  font-weight: 500;
}
</style>