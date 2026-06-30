<template>
  <div class="register-page">
    <div class="page-container">
      <div class="breadcrumb">
        <router-link to="/">首页</router-link>
        <span class="separator">/</span>
        <span>企业注册</span>
      </div>
      <h1 class="page-title">企业注册</h1>
      <p class="page-subtitle">请如实填写企业信息，完成注册后即可在线申请备案</p>

      <div class="card">
        <div class="card-header">
          <h2>企业基本信息</h2>
        </div>
        <div class="card-body">
          <div class="form-grid">
            <div class="form-group">
              <label class="form-label">登录用户名 <span class="required">*</span></label>
              <input v-model="form.username" class="form-input" placeholder="用于登录系统（建议使用统一社会信用代码）" />
            </div>
            <div class="form-group">
              <label class="form-label">统一社会信用代码 <span class="required">*</span></label>
              <input v-model="form.credit_code" class="form-input" placeholder="请输入18位统一社会信用代码" maxlength="18" />
            </div>
            <div class="form-group">
              <label class="form-label">企业名称 <span class="required">*</span></label>
              <input v-model="form.enterprise_name" class="form-input" placeholder="请输入企业全称" />
            </div>
            <div class="form-group">
              <label class="form-label">企业所在地 <span class="required">*</span></label>
              <select v-model="form.region" class="form-select">
                <option value="">请选择</option>
                <option v-for="r in regions" :key="r" :value="r">{{ r }}</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">详细地址 <span class="required">*</span></label>
              <input v-model="form.address" class="form-input" placeholder="请输入企业详细地址" />
            </div>
            <div class="form-group">
              <label class="form-label">法定代表人 <span class="required">*</span></label>
              <input v-model="form.legal_person" class="form-input" placeholder="请输入法定代表人姓名" />
            </div>
            <div class="form-group">
              <label class="form-label">法定代表人身份证号 <span class="required">*</span></label>
              <input v-model="form.legal_person_id" class="form-input" placeholder="请输入法定代表人身份证号" />
            </div>
            <div class="form-group">
              <label class="form-label">联系人 <span class="required">*</span></label>
              <input v-model="form.contact_person" class="form-input" placeholder="请输入联系人姓名" />
            </div>
            <div class="form-group">
              <label class="form-label">联系电话 <span class="required">*</span></label>
              <input v-model="form.contact_phone" class="form-input" placeholder="请输入联系电话" />
            </div>
            <div class="form-group">
              <label class="form-label">登录密码 <span class="required">*</span></label>
              <input v-model="form.password" type="password" class="form-input" placeholder="请输入登录密码（至少6位）" />
            </div>
            <div class="form-group">
              <label class="form-label">确认密码 <span class="required">*</span></label>
              <input v-model="form.confirm_password" type="password" class="form-input" placeholder="请再次输入密码" />
            </div>
          </div>
        </div>
        <div class="card-footer">
          <router-link to="/" class="btn btn-ghost">取消</router-link>
          <button class="btn btn-primary" @click="handleRegister" :disabled="loading">
            {{ loading ? '注册中...' : '提交注册' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { register } from '../api'

const router = useRouter()
const loading = ref(false)

const regions = ['西宁市', '海东市', '海北藏族自治州', '黄南藏族自治州', '海南藏族自治州', '果洛藏族自治州', '玉树藏族自治州', '海西蒙古族藏族自治州']

const form = reactive({
  username: '',
  credit_code: '',
  enterprise_name: '',
  region: '',
  address: '',
  legal_person: '',
  legal_person_id: '',
  contact_person: '',
  contact_phone: '',
  password: '',
  confirm_password: '',
})

async function handleRegister() {
  const required = ['username', 'credit_code', 'enterprise_name', 'region', 'address', 'legal_person', 'legal_person_id', 'contact_person', 'contact_phone', 'password']
  for (const key of required) {
    if (!form[key]) {
      alert('请填写所有必填项')
      return
    }
  }
  if (form.password !== form.confirm_password) {
    alert('两次输入的密码不一致')
    return
  }
  if (form.password.length < 6) {
    alert('密码至少6位')
    return
  }
  loading.value = true
  try {
    const res = await register({ ...form })
    localStorage.setItem('token', res.data.access)
    localStorage.setItem('user', JSON.stringify(res.data.user))
    alert('注册成功！即将跳转到备案申请页面。')
    router.push('/apply')
  } catch (e) {
    // 错误已由拦截器处理
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0 var(--space-xl);
}

@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
}
</style>