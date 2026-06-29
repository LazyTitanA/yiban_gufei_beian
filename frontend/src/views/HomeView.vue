<template>
  <div class="home-page">
    <!-- Hero 横幅 -->
    <section class="hero-section">
      <div class="container hero-inner">
        <div class="hero-content">
          <h1 class="hero-title">青海省一般工业固体废物<br>跨省转移备案系统</h1>
          <p class="hero-desc">在线填报 · 一站办理 · 高效便捷 · 全程监管</p>
          <div class="hero-actions">
            <router-link to="/apply" class="btn btn-accent btn-lg">立即申请备案</router-link>
            <router-link to="/guide" class="btn btn-outline btn-lg" style="color:#FFF;border-color:rgba(255,255,255,0.5);">查看办事指南</router-link>
          </div>
        </div>
        <div class="hero-right">
          <div class="hero-stats">
            <div class="stat-item">
              <div class="stat-number">{{ stats.total }}</div>
              <div class="stat-label">累计备案</div>
            </div>
            <div class="stat-item">
              <div class="stat-number">{{ stats.completed }}</div>
              <div class="stat-label">备案完成</div>
            </div>
            <div class="stat-item">
              <div class="stat-number">{{ stats.completion_rate }}%</div>
              <div class="stat-label">办结率</div>
            </div>
          </div>
          <div class="hero-flow">
            <h3 class="hero-flow-title">备案流程</h3>
            <div class="hero-flow-steps">
              <div class="hero-flow-step">
                <div class="hero-flow-step-icon">1</div>
                <span>企业注册</span>
              </div>
              <div class="hero-flow-arrow">→</div>
              <div class="hero-flow-step">
                <div class="hero-flow-step-icon">2</div>
                <span>填写申请表</span>
              </div>
              <div class="hero-flow-arrow">→</div>
              <div class="hero-flow-step">
                <div class="hero-flow-step-icon">3</div>
                <span>上传材料</span>
              </div>
              <div class="hero-flow-arrow">→</div>
              <div class="hero-flow-step">
                <div class="hero-flow-step-icon">4</div>
                <span>提交审核</span>
              </div>
              <div class="hero-flow-arrow">→</div>
              <div class="hero-flow-step">
                <div class="hero-flow-step-icon">5</div>
                <span>备案完成</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 通知公告 + 政策法规 -->
    <section class="section bg-gray">
      <div class="container">
        <div class="info-grid">
          <!-- 通知公告 -->
          <div class="card">
            <div class="card-header">
              <h2>通知公告</h2>
              <a href="#" class="text-sm">更多 &gt;</a>
            </div>
            <div class="card-body notice-list">
              <div class="notice-item" v-for="n in notices" :key="n.id">
                <span class="notice-tag" :class="n.tagClass">{{ n.tag }}</span>
                <a href="#" class="notice-title">{{ n.title }}</a>
                <span class="notice-date">{{ n.date }}</span>
              </div>
            </div>
          </div>

          <!-- 政策法规 -->
          <div class="card">
            <div class="card-header">
              <h2>政策法规</h2>
              <a href="#" class="text-sm">更多 &gt;</a>
            </div>
            <div class="card-body notice-list">
              <div class="notice-item" v-for="p in policies" :key="p.id">
                <span class="notice-dot">●</span>
                <a href="#" class="notice-title">{{ p.title }}</a>
                <span class="notice-date">{{ p.date }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getStats } from '../api'

const stats = ref({ total: '--', completed: '--', completion_rate: '--' })

onMounted(async () => {
  try {
    const res = await getStats()
    stats.value = res.data
  } catch (e) { /* 忽略 */ }
})

const notices = [
  { id: 1, tag: '通知', tagClass: 'tag-notice', title: '关于规范一般工业固体废物跨省转移备案工作的通知', date: '2024-12-01' },
  { id: 2, tag: '公告', tagClass: 'tag-announce', title: '青海省2024年度一般固废跨省转移备案情况通报', date: '2024-11-15' },
  { id: 3, tag: '提醒', tagClass: 'tag-remind', title: '关于系统升级维护的公告（12月10日）', date: '2024-12-08' },
  { id: 4, tag: '通知', tagClass: 'tag-notice', title: '关于开展2025年度固废管理培训的通知', date: '2024-11-28' },
  { id: 5, tag: '公告', tagClass: 'tag-announce', title: '青海省生态环境厅关于进一步加强固废管理的公告', date: '2024-11-10' },
]

const policies = [
  { id: 1, title: '《中华人民共和国固体废物污染环境防治法》', date: '2020-09-01' },
  { id: 2, title: '《青海省固体废物污染环境防治条例》', date: '2022-01-01' },
  { id: 3, title: '《一般工业固体废物管理台账制定指南》', date: '2021-12-01' },
  { id: 4, title: '《固体废物跨省转移许可管理办法》', date: '2023-03-15' },
  { id: 5, title: '《关于进一步加强一般工业固废跨省转移管理的通知》', date: '2024-06-01' },
]

const materials = [
  { id: '01', title: '申请表', desc: '在线如实填写的《青海省一般工业固体废物跨省转移申请表》' },
  { id: '02', title: '委托合同', desc: '与接收单位签订的合同复印件，需明确环保责任条款并加盖公章' },
  { id: '03', title: '接收方资质', desc: '接收单位的营业执照复印件及处置能力证明，均需加盖公章' },
  { id: '04', title: '运输方资质', desc: '运输单位的资质证明及污染防治承诺书，加盖公章' },
  { id: '05', title: '法人身份证明', desc: '转移和接收单位法定代表人的身份证复印件，加盖公章' },
  { id: '06', title: '授权委托书', desc: '如委托他人办理，需提供载明代理人信息、委托事项和期限的授权委托书' },
]
</script>

<style scoped>
/* Hero */
.hero-section {
  background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 50%, var(--primary-light) 100%);
  padding: 80px 0;
  color: #FFFFFF;
  position: relative;
  overflow: hidden;
}

.hero-section::before {
  content: '';
  position: absolute;
  inset: 0;
  background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
}

.hero-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-3xl);
  position: relative;
  z-index: 1;
}

.hero-title {
  font-size: 40px;
  font-weight: 700;
  color: #FFFFFF;
  line-height: 1.3;
  margin: 0 0 var(--space-lg);
}

.hero-desc {
  font-size: 18px;
  color: rgba(255,255,255,0.8);
  margin-bottom: var(--space-xl);
  letter-spacing: 4px;
}

.hero-actions {
  display: flex;
  gap: var(--space-md);
}

.hero-stats {
  display: flex;
  gap: var(--space-lg);
  flex-shrink: 0;
}

.stat-item {
  text-align: center;
  padding: var(--space-lg) var(--space-xl);
  background: rgba(255,255,255,0.1);
  border-radius: var(--radius-lg);
  border: 1px solid rgba(255,255,255,0.15);
  min-width: 120px;
}

.stat-number {
  font-size: 32px;
  font-weight: 700;
  color: #FFFFFF;
  line-height: 1.2;
}

.stat-label {
  font-size: 13px;
  color: rgba(255,255,255,0.7);
  margin-top: var(--space-xs);
}

/* Hero 右侧区域 */
.hero-right {
  display: flex;
  flex-direction: column;
  gap: var(--space-xl);
  flex-shrink: 0;
}

/* Hero 备案流程 */
.hero-flow {
  background: rgba(255,255,255,0.08);
  border-radius: var(--radius-lg);
  border: 1px solid rgba(255,255,255,0.12);
  padding: var(--space-lg) var(--space-xl);
}

.hero-flow-title {
  font-size: 15px;
  font-weight: 600;
  color: rgba(255,255,255,0.9);
  margin: 0 0 var(--space-md);
  text-align: center;
}

.hero-flow-steps {
  display: flex;
  align-items: center;
  gap: 0;
}

.hero-flow-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  flex: 1;
}

.hero-flow-step-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(255,255,255,0.15);
  color: #FFFFFF;
  font-size: 15px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-flow-step span {
  font-size: 12px;
  color: rgba(255,255,255,0.75);
  white-space: nowrap;
}

.hero-flow-arrow {
  font-size: 16px;
  color: rgba(255,255,255,0.3);
  margin-bottom: 18px;
  flex-shrink: 0;
}

/* 通用 section */
.section {
  padding: var(--space-3xl) 0;
}

.bg-gray {
  background: var(--bg-gray);
}

.section-header {
  text-align: center;
  margin-bottom: var(--space-2xl);
}

.section-title {
  font-size: 28px;
  font-weight: 600;
  color: var(--primary);
  margin-bottom: var(--space-sm);
}

.section-desc {
  font-size: 15px;
  color: var(--text-secondary);
}

/* 流程步骤 */
.flow-steps {
  display: flex;
  align-items: flex-start;
  gap: 0;
}

.flow-step {
  flex: 1;
  text-align: center;
  padding: 0 var(--space-md);
}

.flow-step-icon {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: var(--primary);
  color: #FFFFFF;
  font-size: 22px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto var(--space-md);
}

.flow-step-body h4 {
  font-size: 16px;
  font-weight: 600;
  color: var(--primary);
  margin-bottom: var(--space-sm);
}

.flow-step-body p {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.6;
}

.flow-arrow {
  font-size: 24px;
  color: var(--border);
  margin-top: 16px;
  flex-shrink: 0;
}

/* 通知公告 */
.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-xl);
}

.notice-list {
  padding: 0;
}

.notice-item {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  padding: 12px 0;
  border-bottom: 1px dashed var(--border-light);
}

.notice-item:last-child {
  border-bottom: none;
}

.notice-tag {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 3px;
  flex-shrink: 0;
  font-weight: 500;
}

.tag-notice { background: var(--info-bg); color: var(--info); }
.tag-announce { background: var(--warning-bg); color: var(--warning); }
.tag-remind { background: var(--accent-bg); color: var(--accent); }

.notice-dot {
  color: var(--accent);
  font-size: 8px;
  flex-shrink: 0;
}

.notice-title {
  flex: 1;
  font-size: 14px;
  color: var(--text);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.notice-title:hover {
  color: var(--primary);
}

.notice-date {
  font-size: 12px;
  color: var(--text-light);
  flex-shrink: 0;
}

/* 材料清单 */
.material-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-lg);
}

.material-card {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: var(--space-xl);
  display: flex;
  gap: var(--space-lg);
  transition: box-shadow 0.2s;
}

.material-card:hover {
  box-shadow: var(--shadow-md);
}

.material-num {
  font-size: 28px;
  font-weight: 700;
  color: var(--primary);
  opacity: 0.3;
  line-height: 1;
  flex-shrink: 0;
}

.material-info h4 {
  font-size: 15px;
  font-weight: 600;
  color: var(--text);
  margin-bottom: var(--space-sm);
}

.material-info p {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.5;
}

@media (max-width: 768px) {
  .hero-section {
    padding: 48px 0;
  }

  .hero-inner {
    flex-direction: column;
    text-align: center;
  }

  .hero-title {
    font-size: 28px;
  }

  .hero-actions {
    flex-direction: column;
    align-items: center;
  }

  .hero-right {
    width: 100%;
  }

  .hero-stats {
    width: 100%;
    justify-content: center;
  }

  .stat-item {
    min-width: auto;
    padding: var(--space-md) var(--space-lg);
  }

  .stat-number {
    font-size: 24px;
  }

  .hero-flow-steps {
    flex-wrap: wrap;
    justify-content: center;
  }

  .hero-flow-arrow {
    display: none;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }
}
</style>