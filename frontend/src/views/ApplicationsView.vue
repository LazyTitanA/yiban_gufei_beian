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
        <div class="app-list-mobile" v-if="applications.length > 0">
          <div class="app-card" v-for="app in applications" :key="app.id">
            <div class="app-card-header">
              <div class="app-card-no">{{ app.application_no }}</div>
              <div class="app-card-date">{{ app.created_at?.split('T')[0] }}</div>
            </div>
            <div class="app-card-body">
              <div class="app-card-row">
                <span class="app-card-label">转移单位</span>
                <span class="app-card-value">{{ app.transfer_unit }}</span>
              </div>
              <div class="app-card-row">
                <span class="app-card-label">接收单位</span>
                <span class="app-card-value">{{ app.receive_unit }}</span>
              </div>
              <div class="app-card-row">
                <span class="app-card-label">废物名称</span>
                <span class="app-card-value">{{ app.waste_name }} ({{ app.transfer_amount }}吨)</span>
              </div>
              <div class="app-card-row">
                <span class="app-card-label">当前状态</span>
                <span class="app-card-value">
                  <span class="status-tag" :class="'status-' + app.status">{{ statusMap[app.status] }}</span>
                </span>
              </div>
            </div>
            <div class="app-card-footer">
              <div class="app-card-ai">
                <span class="app-card-ai-label">AI预审：</span>
                <span v-if="app.ai_review_status" class="status-tag" :class="'status-' + (app.ai_review_status === 'passed' ? 'approved' : app.ai_review_status === 'failed' ? 'rejected' : 'draft')">
                  {{ aiStatusMap[app.ai_review_status] || '--' }}
                </span>
                <span v-else class="text-muted">--</span>
              </div>
              <router-link :to="'/application/' + app.id" class="btn btn-primary btn-sm">查看详情</router-link>
            </div>
          </div>
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

.app-list-mobile {
  display: none;
  flex-direction: column;
  gap: var(--space-md);
}

.app-card {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: var(--space-lg);
}

.app-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--space-md);
  padding-bottom: var(--space-sm);
  border-bottom: 1px dashed var(--border-light);
}

.app-card-no {
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 13px;
  color: var(--primary);
  font-weight: 600;
}

.app-card-date {
  font-size: 12px;
  color: var(--text-light);
}

.app-card-body {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
  margin-bottom: var(--space-md);
}

.app-card-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--space-sm);
  font-size: 13px;
}

.app-card-label {
  color: var(--text-secondary);
  flex-shrink: 0;
  width: 80px;
}

.app-card-value {
  flex: 1;
  color: var(--text);
  text-align: right;
  word-break: break-all;
}

.app-card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: var(--space-sm);
  border-top: 1px dashed var(--border-light);
}

.app-card-ai {
  font-size: 12px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.app-card-ai-label {
  color: var(--text-secondary);
}

@media (max-width: 768px) {
  .table-wrapper {
    display: none;
  }

  .app-list-mobile {
    display: flex;
  }
}
</style>