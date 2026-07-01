<template>
  <div class="review-page">
    <div class="page-container">
      <div class="breadcrumb">
        <router-link to="/">首页</router-link>
        <span class="separator">/</span>
        <span>人工审核</span>
      </div>
      <h1 class="page-title">人工审核</h1>
      <p class="page-subtitle">查看待审核的申请并进行审核操作</p>

      <div class="review-layout">
        <div class="review-sidebar">
          <div class="sidebar-header">
            <h3>待审核列表</h3>
            <span class="badge">{{ pendingList.length }}</span>
          </div>
          <div class="sidebar-list">
            <div
              v-for="item in pendingList"
              :key="item.id"
              class="sidebar-item"
              :class="{ active: selectedId === item.id }"
              @click="selectApplication(item)"
            >
              <div class="item-header">
                <span class="item-no">{{ item.application_no }}</span>
                <span class="status-tag" :class="'status-' + item.status">{{ statusMap[item.status] }}</span>
              </div>
              <div class="item-body">
                <div class="item-unit">{{ item.transfer_unit }}</div>
                <div class="item-time">{{ formatTime(item.created_at) }}</div>
              </div>
              <div class="item-meta">
                <span class="file-count">{{ item.file_count }} 个附件</span>
                <span v-if="item.ai_review_status === 'passed'" class="ai-tag passed">✓ AI通过</span>
                <span v-else-if="item.ai_review_status === 'failed'" class="ai-tag failed">✗ AI不通过</span>
                <span v-else class="ai-tag">AI待审</span>
              </div>
            </div>
            <div v-if="pendingList.length === 0" class="empty-state">
              <div class="empty-icon">📋</div>
              <p>暂无待审核申请</p>
            </div>
          </div>
        </div>

        <div class="review-content">
          <div v-if="!selectedApp" class="content-empty">
            <div class="empty-icon">👈</div>
            <h3>请选择要审核的申请</h3>
            <p>从左侧列表中选择一个申请进行审核</p>
          </div>

          <div v-else>
            <div class="content-header">
              <div class="header-info">
                <h2>{{ selectedApp.application_no }}</h2>
                <p class="applicant-info">{{ selectedApp.applicant_name }} | {{ selectedApp.applicant_credit_code }}</p>
              </div>
              <div class="header-actions">
                <span class="status-tag large" :class="'status-' + selectedApp.status">{{ statusMap[selectedApp.status] }}</span>
              </div>
            </div>

            <div class="review-cards">
              <div class="card-row">
                <div class="card primary">
                  <div class="card-header">
                    <h3>📋 申请信息概览</h3>
                  </div>
                  <div class="card-body">
                    <div class="overview-grid">
                      <div class="overview-item">
                        <span class="overview-label">转移单位</span>
                        <span class="overview-value">{{ selectedApp.transfer_unit }}</span>
                      </div>
                      <div class="overview-item">
                        <span class="overview-label">接收单位</span>
                        <span class="overview-value">{{ selectedApp.receive_unit }}</span>
                      </div>
                      <div class="overview-item">
                        <span class="overview-label">废物名称</span>
                        <span class="overview-value">{{ selectedApp.waste_name }}</span>
                      </div>
                      <div class="overview-item">
                        <span class="overview-label">转移数量</span>
                        <span class="overview-value">{{ selectedApp.transfer_amount }} 吨</span>
                      </div>
                      <div class="overview-item">
                        <span class="overview-label">接收省份</span>
                        <span class="overview-value">{{ selectedApp.receive_province }}</span>
                      </div>
                      <div class="overview-item">
                        <span class="overview-label">处置方式</span>
                        <span class="overview-value">{{ selectedApp.disposal_method }}</span>
                      </div>
                    </div>
                  </div>
                </div>

                <div class="card" v-if="aiReview">
                  <div class="card-header">
                    <h3>🤖 AI 预审结果</h3>
                  </div>
                  <div class="card-body">
                    <div class="ai-summary-row">
                      <div class="ai-score-badge" :class="aiReview.status">
                        {{ aiReview.score || '--' }}分
                      </div>
                      <div class="ai-status-text" :class="aiReview.status">
                        {{ aiReview.status === 'passed' ? '✅ 预审通过' : aiReview.status === 'failed' ? '❌ 预审不通过' : '⏳ 处理中' }}
                      </div>
                    </div>
                    <p class="ai-summary">{{ aiReview.summary }}</p>
                    <div v-if="aiReview.issues && aiReview.issues.length > 0" class="ai-issues-list">
                      <h4>⚠️ 发现问题</h4>
                      <ul>
                        <li v-for="(issue, i) in aiReview.issues" :key="i">{{ issue }}</li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>

              <div class="card-row full">
                <div class="card">
                  <div class="card-header">
                    <h3>📝 详细申请信息</h3>
                    <div class="card-tabs">
                      <button
                        v-for="tab in infoTabs"
                        :key="tab.key"
                        class="tab-btn"
                        :class="{ active: activeInfoTab === tab.key }"
                        @click="activeInfoTab = tab.key"
                      >{{ tab.label }}</button>
                    </div>
                  </div>
                  <div class="card-body">
                    <div v-if="activeInfoTab === 'transfer'" class="info-section">
                      <div class="detail-grid">
                        <div class="detail-item"><span class="detail-label">单位名称</span><span class="detail-value">{{ selectedApp.transfer_unit }}</span></div>
                        <div class="detail-item"><span class="detail-label">单位地址</span><span class="detail-value">{{ selectedApp.transfer_address }}</span></div>
                        <div class="detail-item"><span class="detail-label">联系人</span><span class="detail-value">{{ selectedApp.transfer_contact }}</span></div>
                        <div class="detail-item"><span class="detail-label">联系电话</span><span class="detail-value">{{ selectedApp.transfer_phone }}</span></div>
                      </div>
                    </div>
                    <div v-if="activeInfoTab === 'receive'" class="info-section">
                      <div class="detail-grid">
                        <div class="detail-item"><span class="detail-label">单位名称</span><span class="detail-value">{{ selectedApp.receive_unit }}</span></div>
                        <div class="detail-item"><span class="detail-label">所在省份</span><span class="detail-value">{{ selectedApp.receive_province }}</span></div>
                        <div class="detail-item"><span class="detail-label">单位地址</span><span class="detail-value">{{ selectedApp.receive_address }}</span></div>
                        <div class="detail-item"><span class="detail-label">联系人</span><span class="detail-value">{{ selectedApp.receive_contact }}</span></div>
                        <div class="detail-item"><span class="detail-label">联系电话</span><span class="detail-value">{{ selectedApp.receive_phone }}</span></div>
                        <div class="detail-item"><span class="detail-label">处置方式</span><span class="detail-value">{{ selectedApp.disposal_method }}</span></div>
                      </div>
                    </div>
                    <div v-if="activeInfoTab === 'waste'" class="info-section">
                      <div class="detail-grid">
                        <div class="detail-item"><span class="detail-label">废物名称</span><span class="detail-value">{{ selectedApp.waste_name }}</span></div>
                        <div class="detail-item"><span class="detail-label">废物类别</span><span class="detail-value">{{ selectedApp.waste_category }}</span></div>
                        <div class="detail-item"><span class="detail-label">废物代码</span><span class="detail-value">{{ selectedApp.waste_code }}</span></div>
                        <div class="detail-item"><span class="detail-label">转移数量</span><span class="detail-value">{{ selectedApp.transfer_amount }} 吨</span></div>
                        <div class="detail-item"><span class="detail-label">形态</span><span class="detail-value">{{ selectedApp.waste_form }}</span></div>
                        <div class="detail-item"><span class="detail-label">包装方式</span><span class="detail-value">{{ selectedApp.packaging }}</span></div>
                        <div class="detail-item"><span class="detail-label">主要成分</span><span class="detail-value">{{ selectedApp.main_components || '--' }}</span></div>
                        <div class="detail-item"><span class="detail-label">危险特性</span><span class="detail-value">{{ selectedApp.hazardous || '--' }}</span></div>
                      </div>
                    </div>
                    <div v-if="activeInfoTab === 'transport'" class="info-section">
                      <div class="detail-grid">
                        <div class="detail-item"><span class="detail-label">运输单位</span><span class="detail-value">{{ selectedApp.transport_unit }}</span></div>
                        <div class="detail-item"><span class="detail-label">运输方式</span><span class="detail-value">{{ selectedApp.transport_method }}</span></div>
                        <div class="detail-item"><span class="detail-label">转移期限</span><span class="detail-value">{{ selectedApp.transfer_start }} 至 {{ selectedApp.transfer_end }}</span></div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="card-row full">
                <div class="card">
                  <div class="card-header">
                    <h3>📎 上传材料</h3>
                    <span class="material-count">共 {{ selectedApp.files?.length || 0 }} 份材料</span>
                  </div>
                  <div class="card-body">
                    <div class="materials-grid">
                      <div
                        v-for="item in requiredMaterials"
                        :key="item.key"
                        class="material-item"
                        :class="{ uploaded: getFile(item.key), missing: !getFile(item.key) }"
                      >
                        <div class="material-icon">{{ getFile(item.key) ? '📄' : '📭' }}</div>
                        <div class="material-info">
                          <div class="material-title">{{ item.title }}</div>
                          <div class="material-desc">{{ item.desc }}</div>
                        </div>
                        <div class="material-action">
                          <a
                            v-if="getFile(item.key)"
                            :href="getFile(item.key).file"
                            target="_blank"
                            class="btn btn-sm btn-primary"
                          >下载查看</a>
                          <span v-else class="material-status missing">未上传</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="card-row full">
                <div class="card review-action-card">
                  <div class="card-header">
                    <h3>✅ 审核操作</h3>
                  </div>
                  <div class="card-body">
                    <div v-if="selectedApp.review_comment" class="previous-comment">
                      <div class="comment-header" :class="selectedApp.status === 'rejected' ? 'rejected' : 'approved'">
                        {{ selectedApp.status === 'rejected' ? '上一次驳回意见' : '上一次审核意见' }}
                      </div>
                      <div class="comment-body">{{ selectedApp.review_comment }}</div>
                    </div>
                    <div class="review-form">
                      <textarea
                        v-model="reviewComment"
                        class="form-input"
                        rows="3"
                        placeholder="请输入审核意见..."
                      ></textarea>
                      <div class="review-buttons">
                        <button
                          v-if="selectedApp.status !== 'approved'"
                          class="btn btn-accent"
                          :disabled="reviewing"
                          @click="handleReview('approve')"
                        >{{ reviewing ? '处理中...' : '审核通过' }}</button>
                        <button
                          v-if="selectedApp.status !== 'rejected'"
                          class="btn btn-danger"
                          :disabled="reviewing"
                          @click="handleReview('reject')"
                        >{{ reviewing ? '处理中...' : '驳回申请' }}</button>
                        <button
                          v-if="selectedApp.status === 'approved'"
                          class="btn btn-success"
                          :disabled="reviewing"
                          @click="handleReview('complete')"
                        >{{ reviewing ? '处理中...' : '备案完成' }}</button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getApplications, getApplication, getAIReview, reviewApplication } from '../api'

const pendingList = ref([])
const selectedId = ref(null)
const selectedApp = ref(null)
const aiReview = ref(null)
const reviewComment = ref('')
const reviewing = ref(false)
const activeInfoTab = ref('transfer')

const statusMap = {
  draft: '草稿', pending: '待审核', reviewing: '审核中',
  approved: '已通过', rejected: '已驳回', completed: '备案完成',
}

const fileTypeMap = {
  contract: '委托合同', receiver_license: '接收方营业执照',
  receiver_capacity: '接收方处置能力证明', transporter_license: '运输方资质证明',
  transporter_pledge: '运输方污染防治承诺书', legal_id: '法人身份证明', authorization: '授权委托书',
}

const requiredMaterials = [
  { key: 'contract', title: '委托合同', desc: '与接收单位签订的合同复印件' },
  { key: 'receiver_license', title: '接收方营业执照', desc: '接收单位的营业执照复印件' },
  { key: 'receiver_capacity', title: '接收方处置能力证明', desc: '接收单位的处置能力证明文件' },
  { key: 'transporter_license', title: '运输方资质证明', desc: '运输单位的资质证明文件' },
  { key: 'transporter_pledge', title: '运输方污染防治承诺书', desc: '运输单位出具的污染防治承诺书' },
  { key: 'legal_id', title: '法人身份证明', desc: '转移和接收单位法定代表人的身份证复印件' },
  { key: 'authorization', title: '授权委托书', desc: '如委托他人办理，需提供授权委托书' },
]

const infoTabs = [
  { key: 'transfer', label: '转移单位' },
  { key: 'receive', label: '接收单位' },
  { key: 'waste', label: '废物信息' },
  { key: 'transport', label: '运输信息' },
]

function formatTime(time) {
  if (!time) return ''
  return time.split('T')[0]
}

function getFile(key) {
  if (!selectedApp.value || !selectedApp.value.files) return null
  return selectedApp.value.files.find(f => f.file_type === key)
}

async function loadPendingList() {
  try {
    const res = await getApplications({ status: 'pending' })
    pendingList.value = res.data.results || res.data
  } catch (e) {
    console.error('加载待审核列表失败', e)
  }
}

async function selectApplication(item) {
  selectedId.value = item.id
  reviewComment.value = ''
  try {
    const res = await getApplication(item.id)
    selectedApp.value = res.data
    try {
      const aiRes = await getAIReview(item.id)
      aiReview.value = aiRes.data
    } catch (e) {
      aiReview.value = null
    }
  } catch (e) {
    console.error('加载申请详情失败', e)
  }
}

async function handleReview(action) {
  reviewing.value = true
  try {
    await reviewApplication(selectedId.value, {
      action,
      comment: reviewComment.value,
    })
    alert(action === 'approve' ? '审核通过！' : action === 'reject' ? '已驳回申请' : '备案完成！')
    await loadPendingList()
    if (pendingList.value.length > 0) {
      await selectApplication(pendingList.value[0])
    } else {
      selectedApp.value = null
      selectedId.value = null
    }
  } catch (e) {
    alert('审核操作失败，请重试')
  } finally {
    reviewing.value = false
  }
}

onMounted(async () => {
  await loadPendingList()
})
</script>

<style scoped>
.review-layout { display: flex; gap: var(--space-lg); margin-top: var(--space-lg); }

.review-sidebar { width: 320px; flex-shrink: 0; background: var(--bg-gray); border-radius: var(--radius-lg); overflow: hidden; }
.sidebar-header { padding: var(--space-lg); display: flex; align-items: center; justify-content: space-between; background: var(--primary); color: #FFFFFF; }
.sidebar-header h3 { margin: 0; font-size: 16px; }
.badge { background: rgba(255,255,255,0.2); padding: 2px 10px; border-radius: 10px; font-size: 12px; font-weight: 600; }

.sidebar-list { padding: var(--space-sm); max-height: calc(100vh - 280px); overflow-y: auto; }
.sidebar-item { background: #FFFFFF; border-radius: var(--radius); padding: var(--space-md); margin-bottom: var(--space-sm); cursor: pointer; border: 2px solid transparent; transition: all 0.2s; }
.sidebar-item:hover { border-color: var(--border-light); }
.sidebar-item.active { border-color: var(--primary); background: var(--primary-bg); }

.item-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
.item-no { font-size: 13px; font-weight: 600; color: var(--primary); }
.status-tag { font-size: 11px; padding: 2px 8px; border-radius: 3px; font-weight: 500; }
.status-tag.pending { background: var(--warning-bg); color: var(--warning); }
.status-tag.approved { background: var(--success-bg); color: var(--success); }
.status-tag.rejected { background: var(--error-bg); color: var(--error); }
.status-tag.large { font-size: 14px; padding: 6px 16px; }

.item-body { margin-bottom: 8px; }
.item-unit { font-size: 14px; color: var(--text); font-weight: 500; }
.item-time { font-size: 12px; color: var(--text-light); }

.item-meta { display: flex; align-items: center; gap: 8px; }
.file-count { font-size: 12px; color: var(--text-secondary); }
.ai-tag { font-size: 11px; padding: 2px 6px; border-radius: 3px; }
.ai-tag.passed { background: var(--success-bg); color: var(--success); }
.ai-tag.failed { background: var(--error-bg); color: var(--error); }
.ai-tag { background: var(--bg-gray); color: var(--text-light); }

.empty-state { padding: var(--space-xl); text-align: center; color: var(--text-light); }
.empty-icon { font-size: 48px; margin-bottom: var(--space-md); }

.review-content { flex: 1; min-width: 0; }

.content-empty { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 80px 0; color: var(--text-light); }
.content-empty h3 { color: var(--text-secondary); margin-bottom: 8px; }

.content-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: var(--space-lg); padding: var(--space-lg); background: var(--primary); border-radius: var(--radius-lg); color: #FFFFFF; }
.content-header h2 { margin: 0; font-size: 20px; }
.applicant-info { font-size: 14px; opacity: 0.9; margin-top: 4px; }

.review-cards { display: flex; flex-direction: column; gap: var(--space-lg); }
.card-row { display: flex; gap: var(--space-lg); }
.card-row.full { display: block; }

.card { background: #FFFFFF; border-radius: var(--radius-lg); overflow: hidden; border: 1px solid var(--border); }
.card.primary { flex: 1; }
.card-header { padding: var(--space-lg); border-bottom: 1px solid var(--border-light); background: var(--bg-gray-light); }
.card-header h3 { margin: 0; font-size: 15px; color: var(--text); }
.card-body { padding: var(--space-lg); }

.card-tabs { margin-top: var(--space-md); display: flex; gap: 4px; }
.tab-btn { padding: 6px 16px; border: 1px solid var(--border); background: #FFFFFF; border-radius: var(--radius); font-size: 13px; color: var(--text-secondary); cursor: pointer; }
.tab-btn:hover { border-color: var(--primary); color: var(--primary); }
.tab-btn.active { background: var(--primary); color: #FFFFFF; border-color: var(--primary); }

.material-count { font-size: 13px; color: var(--text-light); margin-left: var(--space-md); }

.overview-grid { display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-md); }
.overview-item { display: flex; flex-direction: column; padding: var(--space-md); background: var(--bg-gray); border-radius: var(--radius); }
.overview-label { font-size: 12px; color: var(--text-light); margin-bottom: 4px; }
.overview-value { font-size: 14px; color: var(--text); font-weight: 500; }

.ai-summary-row { display: flex; align-items: center; gap: var(--space-md); margin-bottom: var(--space-md); }
.ai-score-badge { width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 18px; font-weight: 700; border: 2px solid; }
.ai-score-badge.passed { background: #e8f5e9; color: var(--success); border-color: var(--success); }
.ai-score-badge.failed { background: #fce4ec; color: var(--error); border-color: var(--error); }
.ai-score-badge.error, .ai-score-badge.pending { background: #fff3e0; color: var(--warning); border-color: var(--warning); }
.ai-status-text { font-size: 14px; font-weight: 600; }
.ai-status-text.passed { color: var(--success); }
.ai-status-text.failed { color: var(--error); }
.ai-status-text.pending, .ai-status-text.error { color: var(--warning); }
.ai-summary { font-size: 14px; color: var(--text-secondary); line-height: 1.6; margin-bottom: var(--space-md); }

.ai-issues-list h4 { font-size: 13px; color: var(--error); margin-bottom: 8px; }
.ai-issues-list ul { padding-left: 20px; margin: 0; }
.ai-issues-list li { font-size: 13px; color: var(--text-secondary); line-height: 1.8; }

.detail-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0; border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; }
.detail-item { display: flex; border-bottom: 1px solid var(--border-light); }
.detail-item:nth-last-child(-n+2) { border-bottom: none; }
.detail-label { width: 130px; padding: 10px 14px; background: var(--bg-gray); font-size: 13px; color: var(--text-secondary); font-weight: 500; flex-shrink: 0; }
.detail-value { flex: 1; padding: 10px 14px; font-size: 14px; color: var(--text); }

.materials-grid { display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-md); }
.material-item { display: flex; align-items: flex-start; gap: var(--space-md); padding: var(--space-md); border: 2px solid var(--border-light); border-radius: var(--radius); }
.material-item.uploaded { border-color: var(--success); background: var(--success-bg); }
.material-item.missing { border-color: var(--warning); background: var(--warning-bg); }
.material-icon { font-size: 24px; }
.material-info { flex: 1; min-width: 0; }
.material-title { font-size: 14px; font-weight: 500; color: var(--text); }
.material-desc { font-size: 12px; color: var(--text-light); margin-top: 2px; }
.material-action { flex-shrink: 0; }
.material-status { font-size: 12px; padding: 4px 10px; border-radius: 3px; }
.material-status.missing { background: var(--warning); color: #FFFFFF; }

.review-action-card { border: 2px solid var(--primary); }

.previous-comment { margin-bottom: var(--space-lg); padding: var(--space-md); background: var(--bg-gray); border-radius: var(--radius); }
.comment-header { padding: 6px 12px; font-size: 13px; font-weight: 600; color: #FFFFFF; border-radius: 3px; display: inline-block; margin-bottom: 8px; }
.comment-header.approved { background: var(--success); }
.comment-header.rejected { background: var(--error); }
.comment-body { font-size: 14px; color: var(--text-secondary); line-height: 1.6; }

.review-form { margin-top: var(--space-md); }
.review-form .form-input { width: 100%; resize: vertical; font-size: 14px; }

.review-buttons { display: flex; gap: var(--space-md); margin-top: var(--space-lg); }
.btn-sm { padding: 6px 14px; font-size: 13px; }
.btn-accent { background: var(--primary); color: #FFFFFF; border: none; }
.btn-danger { background: var(--error); color: #FFFFFF; border: none; }
.btn-success { background: var(--success); color: #FFFFFF; border: none; }

@media (max-width: 1024px) {
  .review-layout { flex-direction: column; }
  .review-sidebar { width: 100%; }
  .sidebar-list { max-height: 300px; }
  .card-row { flex-direction: column; }
  .materials-grid { grid-template-columns: 1fr; }
  .detail-grid { grid-template-columns: 1fr; }
  .detail-item:nth-last-child(2) { border-bottom: 1px solid var(--border-light); }
}
</style>