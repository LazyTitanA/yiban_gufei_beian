<template>
  <div class="applications-page">
    <div class="page-container">
      <div class="breadcrumb">
        <router-link to="/">首页</router-link>
        <span class="separator">/</span>
        <span>我的申请</span>
      </div>
      <div class="flex-between mb-lg">
        <div>
          <h1 class="page-title">我的申请</h1>
          <p class="page-subtitle">查看和管理您的备案申请记录</p>
        </div>
        <router-link to="/apply" class="btn btn-primary">新建申请</router-link>
      </div>

      <div class="card">
        <div class="table-wrapper" v-if="applications.length > 0">
          <table>
            <thead>
              <tr>
                <th>申请编号</th>
                <th>转移单位</th>
                <th>接收单位</th>
                <th>废物名称</th>
                <th>转移数量(吨)</th>
                <th>申请日期</th>
                <th>状态</th>
                <th>AI预审</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="app in applications" :key="app.id">
                <td class="app-id">{{ app.application_no }}</td>
                <td>{{ app.transfer_unit }}</td>
                <td>{{ app.receive_unit }}</td>
                <td>{{ app.waste_name }}</td>
                <td>{{ app.transfer_amount }}</td>
                <td>{{ app.created_at?.split('T')[0] }}</td>
                <td><span class="status-tag" :class="'status-' + app.status">{{ statusMap[app.status] }}</span></td>
                <td>
                  <span v-if="app.ai_review_status" class="status-tag" :class="'status-' + (app.ai_review_status === 'passed' ? 'approved' : app.ai_review_status === 'failed' ? 'rejected' : 'draft')">
                    {{ aiStatusMap[app.ai_review_status] || '--' }}
                  </span>
                  <span v-else class="text-muted">--</span>
                </td>
                <td>
                  <router-link :to="'/application/' + app.id" class="btn btn-ghost btn-sm">查看详情</router-link>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else class="empty-state">
          <div class="empty-state-icon">📋</div>
          <div class="empty-state-title">暂无申请记录</div>
          <div class="empty-state-desc">您还没有提交过备案申请，点击下方按钮开始申请</div>
          <router-link to="/apply" class="btn btn-primary mt-lg">立即申请</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getApplications } from '../api'

const statusMap = {
  draft: '草稿',
  pending: '待审核',
  reviewing: '审核中',
  approved: '已通过',
  rejected: '已驳回',
  completed: '备案完成',
}

const aiStatusMap = {
  pending: '待处理',
  passed: '预审通过',
  failed: '预审不通过',
  error: '异常',
}

const applications = ref([])

onMounted(async () => {
  try {
    const res = await getApplications()
    applications.value = res.data.results || res.data
  } catch (e) {
    // 未登录时会跳转登录页
  }
})
</script>

<style scoped>
.app-id {
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 13px;
  color: var(--primary);
  font-weight: 500;
}
</style>