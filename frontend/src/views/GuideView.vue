<template>
  <div class="guide-page">
    <div class="page-container">
      <div class="breadcrumb">
        <router-link to="/">首页</router-link>
        <span class="separator">/</span>
        <span>办事指南</span>
      </div>
      <h1 class="page-title">办事指南</h1>
      <p class="page-subtitle">青海省一般工业固体废物跨省转移备案办理流程及材料要求</p>

      <!-- 办理流程 -->
      <div class="card mb-lg">
        <div class="card-header">
          <h2>办理流程</h2>
        </div>
        <div class="card-body">
          <div class="guide-steps">
            <div class="guide-step">
              <div class="guide-step-num">01</div>
              <div class="guide-step-content">
                <h4>企业注册与登录</h4>
                <p>企业在系统首页点击"企业注册"，填写统一社会信用代码、企业名称、法定代表人等基本信息，完成注册后登录系统。已注册企业直接使用统一社会信用代码和密码登录。</p>
              </div>
            </div>
            <div class="guide-step">
              <div class="guide-step-num">02</div>
              <div class="guide-step-content">
                <h4>在线填写申请表</h4>
                <p>登录后进入"在线申请"页面，如实填写《青海省一般工业固体废物跨省转移申请表》，包括转移单位信息、接收单位信息、固体废物信息和运输信息等。</p>
              </div>
            </div>
            <div class="guide-step">
              <div class="guide-step-num">03</div>
              <div class="guide-step-content">
                <h4>上传申请材料</h4>
                <p>按要求上传以下材料的扫描件（均需加盖公章）：</p>
                <ul>
                  <li>与接收单位签订的委托合同复印件</li>
                  <li>接收单位营业执照及处置能力证明</li>
                  <li>运输单位资质证明及污染防治承诺书</li>
                  <li>法定代表人身份证复印件</li>
                  <li>授权委托书（如委托他人办理）</li>
                </ul>
              </div>
            </div>
            <div class="guide-step">
              <div class="guide-step-num">04</div>
              <div class="guide-step-content">
                <h4>提交申请</h4>
                <p>确认填写信息和上传材料无误后，勾选承诺声明，点击"确认提交"。系统将自动生成申请编号，备案申请正式进入审核流程。</p>
              </div>
            </div>
            <div class="guide-step">
              <div class="guide-step-num">05</div>
              <div class="guide-step-content">
                <h4>等待审核</h4>
                <p>生态环境部门将在规定工作日内完成审核。企业可在"我的申请"中实时查看审核进度。如需补充材料，系统将发送通知。</p>
              </div>
            </div>
            <div class="guide-step">
              <div class="guide-step-num">06</div>
              <div class="guide-step-content">
                <h4>备案完成</h4>
                <p>审核通过后，系统将生成《一般工业固体废物跨省转出通报》。企业可在申请详情页面下载通报文件，备案流程完成。</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 材料要求 -->
      <div class="card mb-lg">
        <div class="card-header">
          <h2>材料要求</h2>
        </div>
        <div class="card-body">
          <table>
            <thead>
              <tr>
                <th style="width:60px;">序号</th>
                <th>材料名称</th>
                <th>要求</th>
                <th style="width:100px;">是否必需</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="m in materialRequirements" :key="m.id">
                <td>{{ m.id }}</td>
                <td>{{ m.name }}</td>
                <td>{{ m.requirement }}</td>
                <td><span class="status-tag" :class="m.required ? 'status-pending' : 'status-draft'">{{ m.required ? '必需' : '条件必需' }}</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 注意事项 -->
      <div class="card mb-lg">
        <div class="card-header">
          <h2>注意事项</h2>
        </div>
        <div class="card-body">
          <div class="notice-list">
            <div class="notice-item">
              <span class="notice-dot">●</span>
              <p>所有上传材料必须清晰可辨，加盖企业公章，格式为 PDF、JPG 或 PNG，单文件不超过 10MB。</p>
            </div>
            <div class="notice-item">
              <span class="notice-dot">●</span>
              <p>申请单位应确保所填信息真实、准确、完整，如有虚假，将承担相应法律责任。</p>
            </div>
            <div class="notice-item">
              <span class="notice-dot">●</span>
              <p>备案审核时限为 5 个工作日，如材料不齐全需要补充的，审核时限自补正材料提交之日起重新计算。</p>
            </div>
            <div class="notice-item">
              <span class="notice-dot">●</span>
              <p>备案通过后，企业应严格按照备案内容执行转移活动，不得擅自变更转移数量、路线等关键信息。</p>
            </div>
            <div class="notice-item">
              <span class="notice-dot">●</span>
              <p>如有疑问，请联系青海省生态环境厅固体废物管理中心，电话：0971-1234567。</p>
            </div>
          </div>
        </div>
      </div>

      <div class="flex-center">
        <router-link to="/apply" class="btn btn-accent btn-lg">立即申请备案</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
const materialRequirements = [
  { id: 1, name: '申请表', requirement: '在线如实填写《青海省一般工业固体废物跨省转移申请表》', required: true },
  { id: 2, name: '委托合同', requirement: '与接收单位签订的合同复印件，需明确环保责任条款并加盖公章', required: true },
  { id: 3, name: '接收方营业执照', requirement: '接收单位营业执照复印件，加盖公章', required: true },
  { id: 4, name: '接收方处置能力证明', requirement: '接收单位处置能力证明文件，加盖公章', required: true },
  { id: 5, name: '运输方资质证明', requirement: '运输单位资质证明文件，加盖公章', required: true },
  { id: 6, name: '运输方污染防治承诺书', requirement: '运输单位出具的污染防治承诺书，加盖公章', required: true },
  { id: 7, name: '法人身份证明', requirement: '转移和接收单位法定代表人身份证复印件，加盖公章', required: true },
  { id: 8, name: '授权委托书', requirement: '如委托他人办理，需提供载明代理人信息、委托事项和期限的授权委托书', required: false },
]
</script>

<style scoped>
/* 办理流程 */
.guide-steps {
  display: flex;
  flex-direction: column;
  gap: var(--space-lg);
}

.guide-step {
  display: flex;
  gap: var(--space-lg);
  padding: var(--space-lg);
  background: var(--bg-gray);
  border-radius: var(--radius-md);
  border-left: 4px solid var(--primary);
}

.guide-step-num {
  font-size: 28px;
  font-weight: 700;
  color: var(--primary);
  opacity: 0.3;
  line-height: 1;
  flex-shrink: 0;
  min-width: 40px;
}

.guide-step-content h4 {
  font-size: 16px;
  font-weight: 600;
  color: var(--primary);
  margin-bottom: var(--space-sm);
}

.guide-step-content p {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.7;
}

.guide-step-content ul {
  margin-top: var(--space-sm);
  padding-left: 20px;
}

.guide-step-content li {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.8;
}

/* 注意事项 */
.notice-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.notice-item {
  display: flex;
  gap: var(--space-md);
  align-items: flex-start;
}

.notice-dot {
  color: var(--accent);
  font-size: 10px;
  margin-top: 4px;
  flex-shrink: 0;
}

.notice-item p {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.7;
}
</style>