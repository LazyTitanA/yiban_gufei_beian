<template>
  <div class="detail-page">
    <div class="page-container">
      <div class="breadcrumb">
        <router-link to="/">首页</router-link>
        <span class="separator">/</span>
        <router-link to="/applications">我的申请</router-link>
        <span class="separator">/</span>
        <span>申请详情</span>
      </div>

      <div class="flex-between mb-lg">
        <div>
          <h1 class="page-title">申请详情</h1>
          <p class="page-subtitle">申请编号：{{ app.application_no }}</p>
        </div>
        <span class="status-tag" :class="'status-' + app.status" style="font-size:14px;padding:6px 16px;">{{ statusMap[app.status] }}</span>
      </div>

      <!-- AI 预审结果 -->
      <div v-if="aiReview && aiReview.status !== 'pending'" class="card mb-lg">
        <div class="card-header">
          <h2>AI 智能预审结果</h2>
        </div>
        <div class="card-body">
          <div class="ai-result-header">
            <div class="ai-score" :class="aiReview.status">
              <span class="ai-score-num">{{ aiReview.score || '--' }}</span>
              <span class="ai-score-label">综合评分</span>
            </div>
            <div class="ai-summary">
              <div class="ai-status" :class="aiReview.status">
                {{ aiReview.status === 'passed' ? '预审通过' : aiReview.status === 'failed' ? '预审不通过' : '处理异常' }}
              </div>
              <p>{{ aiReview.summary }}</p>
            </div>
          </div>
          <div v-if="aiReview.issues && aiReview.issues.length > 0" class="ai-issues">
            <h4>发现的问题</h4>
            <ul>
              <li v-for="(issue, i) in aiReview.issues" :key="i">{{ issue }}</li>
            </ul>
          </div>
          <div v-if="aiReview.suggestions && aiReview.suggestions.length > 0" class="ai-suggestions">
            <h4>修改建议</h4>
            <ul>
              <li v-for="(s, i) in aiReview.suggestions" :key="i">{{ s }}</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- 备案进度 -->
      <div class="card mb-lg">
        <div class="card-header"><h2>备案进度</h2></div>
        <div class="card-body">
          <div class="progress-tracker">
            <div class="progress-node" v-for="(node, idx) in progressNodes" :key="node.key"
              :class="{ done: node.done, active: node.active }">
              <div class="node-dot">
                <span v-if="node.done">&#10003;</span>
                <span v-else>{{ idx + 1 }}</span>
              </div>
              <div class="node-line" v-if="idx < progressNodes.length - 1" :class="{ done: node.done }"></div>
              <div class="node-info">
                <div class="node-title">{{ node.title }}</div>
                <div class="node-time" v-if="node.time">{{ node.time }}</div>
              </div>
            </div>
          </div>

          <!-- 审核意见 -->
          <div v-if="app.review_comment" class="review-box mt-lg">
            <div class="review-header" :class="app.status === 'rejected' ? 'rejected' : 'approved'">
              {{ app.status === 'rejected' ? '审核驳回意见' : '审核意见' }}
            </div>
            <div class="review-body">
              <p>{{ app.review_comment }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 申请信息 -->
      <div class="card mb-lg">
        <div class="card-header"><h2>申请信息</h2></div>
        <div class="card-body">
          <div class="detail-section">
            <h3 class="detail-section-title">转移单位信息</h3>
            <div class="detail-grid">
              <div class="detail-item"><span class="detail-label">单位名称</span><span class="detail-value">{{ app.transfer_unit }}</span></div>
              <div class="detail-item"><span class="detail-label">单位地址</span><span class="detail-value">{{ app.transfer_address }}</span></div>
              <div class="detail-item"><span class="detail-label">联系人</span><span class="detail-value">{{ app.transfer_contact }}</span></div>
              <div class="detail-item"><span class="detail-label">联系电话</span><span class="detail-value">{{ app.transfer_phone }}</span></div>
            </div>
          </div>
          <div class="detail-section">
            <h3 class="detail-section-title">接收单位信息</h3>
            <div class="detail-grid">
              <div class="detail-item"><span class="detail-label">单位名称</span><span class="detail-value">{{ app.receive_unit }}</span></div>
              <div class="detail-item"><span class="detail-label">所在省份</span><span class="detail-value">{{ app.receive_province }}</span></div>
              <div class="detail-item"><span class="detail-label">单位地址</span><span class="detail-value">{{ app.receive_address }}</span></div>
              <div class="detail-item"><span class="detail-label">联系人</span><span class="detail-value">{{ app.receive_contact }}</span></div>
              <div class="detail-item"><span class="detail-label">联系电话</span><span class="detail-value">{{ app.receive_phone }}</span></div>
              <div class="detail-item"><span class="detail-label">处置方式</span><span class="detail-value">{{ app.disposal_method }}</span></div>
            </div>
          </div>
          <div class="detail-section">
            <h3 class="detail-section-title">固体废物信息</h3>
            <div class="detail-grid">
              <div class="detail-item"><span class="detail-label">废物名称</span><span class="detail-value">{{ app.waste_name }}</span></div>
              <div class="detail-item"><span class="detail-label">废物类别</span><span class="detail-value">{{ app.waste_category }}</span></div>
              <div class="detail-item"><span class="detail-label">废物代码</span><span class="detail-value">{{ app.waste_code }}</span></div>
              <div class="detail-item"><span class="detail-label">转移数量(吨)</span><span class="detail-value">{{ app.transfer_amount }}</span></div>
              <div class="detail-item"><span class="detail-label">形态</span><span class="detail-value">{{ app.waste_form }}</span></div>
              <div class="detail-item"><span class="detail-label">包装方式</span><span class="detail-value">{{ app.packaging }}</span></div>
            </div>
          </div>
          <div class="detail-section">
            <h3 class="detail-section-title">运输信息</h3>
            <div class="detail-grid">
              <div class="detail-item"><span class="detail-label">运输单位</span><span class="detail-value">{{ app.transport_unit }}</span></div>
              <div class="detail-item"><span class="detail-label">运输方式</span><span class="detail-value">{{ app.transport_method }}</span></div>
              <div class="detail-item"><span class="detail-label">转移期限</span><span class="detail-value">{{ app.transfer_start }} 至 {{ app.transfer_end }}</span></div>
            </div>
          </div>
        </div>
      </div>

      <!-- 上传材料 -->
      <div class="card mb-lg">
        <div class="card-header"><h2>上传材料</h2></div>
        <div class="card-body">
          <div class="file-list">
            <div class="file-item" v-for="f in app.files" :key="f.id">
              <span class="file-icon">📄</span>
              <span class="file-name">{{ f.original_name }}</span>
              <span class="file-type">{{ fileTypeMap[f.file_type] || f.file_type }}</span>
              <span class="file-status uploaded">已上传</span>
            </div>
            <div v-if="!app.files || app.files.length === 0" class="text-muted text-center">暂无上传材料</div>
          </div>
        </div>
      </div>

      <div class="flex-center gap-md mt-lg">
        <router-link to="/applications" class="btn btn-ghost">返回列表</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getApplication, getAIReview } from '../api'

const route = useRoute()

const statusMap = {
  draft: '草稿', pending: '待审核', reviewing: '审核中',
  approved: '已通过', rejected: '已驳回', completed: '备案完成',
}

const fileTypeMap = {
  contract: '委托合同', receiver_license: '接收方营业执照',
  receiver_capacity: '接收方处置能力证明', transporter_license: '运输方资质证明',
  transporter_pledge: '运输方污染防治承诺书', legal_id: '法人身份证明', authorization: '授权委托书',
}

const app = ref({})
const aiReview = ref(null)

const progressNodes = computed(() => {
  const status = app.value.status
  const statusOrder = { draft: 0, pending: 0, reviewing: 1, approved: 3, rejected: 2, completed: 4 }
  const currentIdx = statusOrder[status] || 0
  const steps = [
    { key: 'submit', title: '提交申请' },
    { key: 'ai', title: 'AI预审' },
    { key: 'review', title: '人工审核' },
    { key: 'approve', title: '审批决定' },
    { key: 'complete', title: '备案完成' },
  ]
  return steps.map((s, i) => ({
    ...s,
    done: i < currentIdx || (status === 'completed' && i === 4),
    active: i === currentIdx,
    time: (i < currentIdx || (status === 'completed' && i === 4)) ? getTime(i) : '',
  }))
})

function getTime(i) {
  const d = app.value
  const times = [d.created_at, d.updated_at, d.reviewed_at, d.reviewed_at, d.reviewed_at]
  return times[i] ? times[i].split('T')[0] : ''
}

onMounted(async () => {
  const id = route.params.id
  try {
    const res = await getApplication(id)
    app.value = res.data

    // 获取 AI 预审结果
    try {
      const aiRes = await getAIReview(id)
      aiReview.value = aiRes.data
    } catch (e) { /* AI 预审可能未完成 */ }
  } catch (e) {
    // 错误处理
  }
})
</script>

<style scoped>
.progress-tracker { display: flex; align-items: flex-start; gap: 0; padding: var(--space-lg) 0; }
.progress-node { flex: 1; display: flex; flex-direction: column; align-items: center; text-align: center; position: relative; }
.node-dot { width: 40px; height: 40px; border-radius: 50%; background: var(--bg-gray); border: 3px solid var(--border); display: flex; align-items: center; justify-content: center; font-size: 16px; font-weight: 600; color: var(--text-light); z-index: 1; flex-shrink: 0; }
.progress-node.done .node-dot { background: var(--success); border-color: var(--success); color: #FFFFFF; }
.progress-node.active .node-dot { background: var(--primary); border-color: var(--primary); color: #FFFFFF; }
.node-line { position: absolute; top: 20px; left: calc(50% + 20px); width: calc(100% - 40px); height: 3px; background: var(--border); }
.node-line.done { background: var(--success); }
.node-info { margin-top: var(--space-md); width: 100%; padding: 0 var(--space-xs); }
.node-title { font-size: 14px; font-weight: 600; color: var(--text-secondary); }
.progress-node.done .node-title, .progress-node.active .node-title { color: var(--text); }
.node-time { font-size: 12px; color: var(--text-light); margin-top: 4px; }

.review-box { border: 1px solid var(--border); border-radius: var(--radius-md); overflow: hidden; }
.review-header { padding: 10px 16px; font-size: 14px; font-weight: 600; color: #FFFFFF; }
.review-header.approved { background: var(--success); }
.review-header.rejected { background: var(--error); }
.review-body { padding: var(--space-lg); font-size: 14px; color: var(--text); line-height: 1.8; }

/* AI 预审 */
.ai-result-header { display: flex; gap: var(--space-xl); align-items: center; margin-bottom: var(--space-lg); }
.ai-score { width: 100px; height: 100px; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; flex-shrink: 0; }
.ai-score.passed { background: #e8f5e9; border: 3px solid var(--success); }
.ai-score.failed { background: #fce4ec; border: 3px solid var(--error); }
.ai-score.error { background: #fff3e0; border: 3px solid var(--warning); }
.ai-score-num { font-size: 28px; font-weight: 700; color: var(--text); }
.ai-score-label { font-size: 12px; color: var(--text-secondary); }
.ai-summary { flex: 1; }
.ai-status { display: inline-block; padding: 2px 12px; border-radius: 3px; font-size: 13px; font-weight: 600; margin-bottom: 8px; }
.ai-status.passed { background: var(--success-bg); color: var(--success); }
.ai-status.failed { background: var(--error-bg); color: var(--error); }
.ai-issues, .ai-suggestions { margin-top: var(--space-md); padding: var(--space-md); background: var(--bg-gray); border-radius: var(--radius); }
.ai-issues h4 { color: var(--error); margin-bottom: 8px; }
.ai-suggestions h4 { color: var(--primary); margin-bottom: 8px; }
.ai-issues ul, .ai-suggestions ul { padding-left: 20px; }
.ai-issues li, .ai-suggestions li { font-size: 13px; color: var(--text-secondary); line-height: 1.8; }

.detail-section { margin-bottom: var(--space-xl); }
.detail-section:last-child { margin-bottom: 0; }
.detail-section-title { font-size: 15px; font-weight: 600; color: var(--primary); padding-bottom: var(--space-sm); border-bottom: 1px solid var(--border-light); margin-bottom: var(--space-lg); }
.detail-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0; border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; }
.detail-item { display: flex; border-bottom: 1px solid var(--border-light); }
.detail-item:nth-last-child(-n+2) { border-bottom: none; }
.detail-label { width: 140px; padding: 10px 16px; background: var(--bg-gray); font-size: 13px; color: var(--text-secondary); font-weight: 500; flex-shrink: 0; }
.detail-value { flex: 1; padding: 10px 16px; font-size: 14px; color: var(--text); }

.file-list { display: flex; flex-direction: column; gap: var(--space-sm); }
.file-item { display: flex; align-items: center; gap: var(--space-md); padding: 10px 16px; background: var(--bg-gray); border-radius: var(--radius); }
.file-icon { font-size: 20px; }
.file-name { flex: 1; font-size: 14px; color: var(--text); }
.file-type { font-size: 12px; color: var(--text-light); margin-right: 8px; }
.file-status { font-size: 12px; padding: 2px 8px; border-radius: 3px; font-weight: 500; }
.file-status.uploaded { background: var(--success-bg); color: var(--success); }

@media (max-width: 768px) {
  .progress-tracker { flex-direction: column; gap: var(--space-md); }
  .progress-node { flex-direction: row; align-items: center; text-align: left; gap: var(--space-md); }
  .node-line { display: none; }
  .node-info { margin-top: 0; }
  .detail-grid { grid-template-columns: 1fr; }
  .detail-item:nth-last-child(2) { border-bottom: 1px solid var(--border-light); }
  .ai-result-header { flex-direction: column; text-align: center; }
}
</style>