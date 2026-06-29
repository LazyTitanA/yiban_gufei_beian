<template>
  <div class="apply-page">
    <div class="page-container">
      <div class="breadcrumb">
        <router-link to="/">首页</router-link>
        <span class="separator">/</span>
        <span>在线申请</span>
      </div>
      <h1 class="page-title">在线申请备案</h1>
      <p class="page-subtitle">请如实填写《青海省一般工业固体废物跨省转移申请表》并上传相关材料</p>

      <!-- 步骤条 -->
      <div class="steps mb-xl">
        <div class="step" :class="{ active: currentStep === 1, done: currentStep > 1 }">
          <div class="step-number">1</div>
          <div class="step-content"><div class="step-title">填写申请表</div></div>
        </div>
        <div class="step-line" :class="{ done: currentStep > 1 }"></div>
        <div class="step" :class="{ active: currentStep === 2, done: currentStep > 2 }">
          <div class="step-number">2</div>
          <div class="step-content"><div class="step-title">上传申请材料</div></div>
        </div>
        <div class="step-line" :class="{ done: currentStep > 2 }"></div>
        <div class="step" :class="{ active: currentStep === 3, done: currentStep > 3 }">
          <div class="step-number">3</div>
          <div class="step-content"><div class="step-title">确认提交</div></div>
        </div>
      </div>

      <!-- 步骤一：填写申请表 -->
      <div v-if="currentStep === 1" class="card">
        <div class="card-header"><h2>青海省一般工业固体废物跨省转移申请表</h2></div>
        <div class="card-body">
          <h3 class="form-section-title">一、转移单位信息</h3>
          <div class="form-grid">
            <div class="form-group">
              <label class="form-label">单位名称 <span class="required">*</span></label>
              <input v-model="form.transfer_unit" class="form-input" placeholder="请输入转移单位全称" />
            </div>
            <div class="form-group">
              <label class="form-label">单位地址 <span class="required">*</span></label>
              <input v-model="form.transfer_address" class="form-input" placeholder="请输入转移单位地址" />
            </div>
            <div class="form-group">
              <label class="form-label">联系人 <span class="required">*</span></label>
              <input v-model="form.transfer_contact" class="form-input" placeholder="请输入联系人" />
            </div>
            <div class="form-group">
              <label class="form-label">联系电话 <span class="required">*</span></label>
              <input v-model="form.transfer_phone" class="form-input" placeholder="请输入联系电话" />
            </div>
          </div>

          <h3 class="form-section-title">二、接收单位信息</h3>
          <div class="form-grid">
            <div class="form-group">
              <label class="form-label">单位名称 <span class="required">*</span></label>
              <input v-model="form.receive_unit" class="form-input" placeholder="请输入接收单位全称" />
            </div>
            <div class="form-group">
              <label class="form-label">所在省份 <span class="required">*</span></label>
              <select v-model="form.receive_province" class="form-select">
                <option value="">请选择省份</option>
                <option v-for="p in provinces" :key="p" :value="p">{{ p }}</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">单位地址 <span class="required">*</span></label>
              <input v-model="form.receive_address" class="form-input" placeholder="请输入接收单位详细地址" />
            </div>
            <div class="form-group">
              <label class="form-label">联系人 <span class="required">*</span></label>
              <input v-model="form.receive_contact" class="form-input" placeholder="请输入联系人" />
            </div>
            <div class="form-group">
              <label class="form-label">联系电话 <span class="required">*</span></label>
              <input v-model="form.receive_phone" class="form-input" placeholder="请输入联系电话" />
            </div>
            <div class="form-group">
              <label class="form-label">处置方式 <span class="required">*</span></label>
              <select v-model="form.disposal_method" class="form-select">
                <option value="">请选择</option>
                <option value="填埋">填埋</option>
                <option value="焚烧">焚烧</option>
                <option value="综合利用">综合利用</option>
                <option value="贮存">贮存</option>
                <option value="其他">其他</option>
              </select>
            </div>
          </div>

          <h3 class="form-section-title">三、固体废物信息</h3>
          <div class="form-grid">
            <div class="form-group">
              <label class="form-label">废物名称 <span class="required">*</span></label>
              <input v-model="form.waste_name" class="form-input" placeholder="请输入固体废物名称" />
            </div>
            <div class="form-group">
              <label class="form-label">废物类别 <span class="required">*</span></label>
              <select v-model="form.waste_category" class="form-select">
                <option value="">请选择</option>
                <option value="SW01">SW01 冶炼废渣</option>
                <option value="SW02">SW02 粉煤灰</option>
                <option value="SW03">SW03 炉渣</option>
                <option value="SW04">SW04 煤矸石</option>
                <option value="SW05">SW05 尾矿</option>
                <option value="SW06">SW06 脱硫石膏</option>
                <option value="SW07">SW07 污泥</option>
                <option value="SW99">SW99 其他废物</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">废物代码 <span class="required">*</span></label>
              <input v-model="form.waste_code" class="form-input" placeholder="请输入废物代码" />
            </div>
            <div class="form-group">
              <label class="form-label">转移数量（吨） <span class="required">*</span></label>
              <input v-model="form.transfer_amount" type="number" class="form-input" placeholder="请输入转移数量" />
            </div>
            <div class="form-group">
              <label class="form-label">形态 <span class="required">*</span></label>
              <select v-model="form.waste_form" class="form-select">
                <option value="">请选择</option>
                <option value="固态">固态</option>
                <option value="半固态">半固态</option>
                <option value="粉状">粉状</option>
                <option value="颗粒状">颗粒状</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">包装方式 <span class="required">*</span></label>
              <input v-model="form.packaging" class="form-input" placeholder="请输入包装方式" />
            </div>
            <div class="form-group">
              <label class="form-label">主要成分</label>
              <input v-model="form.main_components" class="form-input" placeholder="请输入主要成分" />
            </div>
            <div class="form-group">
              <label class="form-label">危险特性</label>
              <input v-model="form.hazardous" class="form-input" placeholder="请输入危险特性" />
            </div>
          </div>

          <h3 class="form-section-title">四、运输信息</h3>
          <div class="form-grid">
            <div class="form-group">
              <label class="form-label">运输单位 <span class="required">*</span></label>
              <input v-model="form.transport_unit" class="form-input" placeholder="请输入运输单位名称" />
            </div>
            <div class="form-group">
              <label class="form-label">运输方式 <span class="required">*</span></label>
              <select v-model="form.transport_method" class="form-select">
                <option value="">请选择</option>
                <option value="公路">公路</option>
                <option value="铁路">铁路</option>
                <option value="水路">水路</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">转移期限（起） <span class="required">*</span></label>
              <input v-model="form.transfer_start" type="date" class="form-input" />
            </div>
            <div class="form-group">
              <label class="form-label">转移期限（止） <span class="required">*</span></label>
              <input v-model="form.transfer_end" type="date" class="form-input" />
            </div>
          </div>
        </div>
        <div class="card-footer">
          <span class="text-sm text-muted">请确保填写信息真实准确</span>
          <button class="btn btn-primary" @click="nextStep">下一步：上传材料</button>
        </div>
      </div>

      <!-- 步骤二：上传材料 -->
      <div v-if="currentStep === 2" class="card">
        <div class="card-header"><h2>上传申请材料</h2></div>
        <div class="card-body">
          <p class="text-muted mb-lg">以下材料均需加盖企业公章后扫描上传，支持 PDF、JPG、PNG 格式，单文件不超过 10MB</p>
          <div class="upload-list">
            <div class="upload-item" v-for="item in uploadItems" :key="item.key">
              <div class="upload-item-header">
                <span class="upload-item-num">{{ item.num }}</span>
                <div>
                  <h4 class="upload-item-title">{{ item.title }} <span class="required">*</span></h4>
                  <p class="upload-item-desc">{{ item.desc }}</p>
                </div>
              </div>
              <div class="upload-item-action">
                <label class="upload-btn">
                  <input type="file" :accept="item.accept" @change="(e) => handleFileUpload(e, item.key)" />
                  <span v-if="!files[item.key]">选择文件</span>
                  <span v-else class="file-name">{{ files[item.key].name }}</span>
                </label>
                <button v-if="files[item.key]" class="btn btn-ghost btn-sm" @click="removeFile(item.key)">移除</button>
              </div>
            </div>
          </div>
        </div>
        <div class="card-footer">
          <button class="btn btn-ghost" @click="currentStep = 1">上一步</button>
          <button class="btn btn-primary" @click="nextStep" :disabled="uploading">
            {{ uploading ? '保存中...' : '下一步：确认提交' }}
          </button>
        </div>
      </div>

      <!-- 步骤三：确认提交 -->
      <div v-if="currentStep === 3" class="card">
        <div class="card-header"><h2>确认申请信息</h2></div>
        <div class="card-body">
          <div class="confirm-section">
            <h3 class="form-section-title">申请信息确认</h3>
            <div class="confirm-grid">
              <div class="confirm-item" v-for="item in confirmFields" :key="item.label">
                <span class="confirm-label">{{ item.label }}</span>
                <span class="confirm-value">{{ item.value || '--' }}</span>
              </div>
            </div>
          </div>
          <div class="confirm-section">
            <h3 class="form-section-title">已上传材料</h3>
            <div class="confirm-files">
              <div class="confirm-file" v-for="item in uploadItems" :key="item.key">
                <span class="confirm-file-icon">📄</span>
                <span class="confirm-file-name">{{ files[item.key] ? files[item.key].name : '未上传' }}</span>
                <span class="confirm-file-status" :class="files[item.key] ? 'uploaded' : 'missing'">
                  {{ files[item.key] ? '已上传' : '未上传' }}
                </span>
              </div>
            </div>
          </div>
          <div class="confirm-notice">
            <p>本人/本单位承诺所提交的申请材料真实、准确、完整，如有虚假，愿承担相应法律责任。</p>
          </div>
        </div>
        <div class="card-footer">
          <button class="btn btn-ghost" @click="currentStep = 2">上一步</button>
          <button class="btn btn-accent" @click="handleSubmit" :disabled="submitting">
            {{ submitting ? '提交中...' : '确认提交' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { createApplication, uploadFile, submitApplication } from '../api'

const router = useRouter()
const currentStep = ref(1)
const submitting = ref(false)
const uploading = ref(false)
const files = reactive({})
const applicationId = ref(null)

const provinces = [
  '北京市', '天津市', '河北省', '山西省', '内蒙古自治区', '辽宁省', '吉林省', '黑龙江省',
  '上海市', '江苏省', '浙江省', '安徽省', '福建省', '江西省', '山东省', '河南省',
  '湖北省', '湖南省', '广东省', '广西壮族自治区', '海南省', '重庆市', '四川省',
  '贵州省', '云南省', '西藏自治区', '陕西省', '甘肃省', '青海省', '宁夏回族自治区', '新疆维吾尔自治区'
]

const form = reactive({
  transfer_unit: '',
  transfer_address: '',
  transfer_contact: '',
  transfer_phone: '',
  receive_unit: '',
  receive_province: '',
  receive_address: '',
  receive_contact: '',
  receive_phone: '',
  disposal_method: '',
  waste_name: '',
  waste_category: '',
  waste_code: '',
  transfer_amount: '',
  waste_form: '',
  packaging: '',
  main_components: '',
  hazardous: '',
  transport_unit: '',
  transport_method: '',
  transfer_start: '',
  transfer_end: '',
})

const uploadItems = [
  { num: '01', key: 'contract', title: '委托合同', desc: '与接收单位签订的合同复印件，需明确环保责任条款并加盖公章', accept: '.pdf,.jpg,.png' },
  { num: '02', key: 'receiver_license', title: '接收方营业执照', desc: '接收单位的营业执照复印件，加盖公章', accept: '.pdf,.jpg,.png' },
  { num: '03', key: 'receiver_capacity', title: '接收方处置能力证明', desc: '接收单位的处置能力证明文件，加盖公章', accept: '.pdf,.jpg,.png' },
  { num: '04', key: 'transporter_license', title: '运输方资质证明', desc: '运输单位的资质证明文件，加盖公章', accept: '.pdf,.jpg,.png' },
  { num: '05', key: 'transporter_pledge', title: '运输方污染防治承诺书', desc: '运输单位出具的污染防治承诺书，加盖公章', accept: '.pdf,.jpg,.png' },
  { num: '06', key: 'legal_id', title: '法人身份证明', desc: '转移和接收单位法定代表人的身份证复印件，加盖公章', accept: '.pdf,.jpg,.png' },
  { num: '07', key: 'authorization', title: '授权委托书', desc: '如委托他人办理，需提供载明代理人信息、委托事项和期限的授权委托书', accept: '.pdf,.jpg,.png' },
]

const confirmFields = computed(() => [
  { label: '转移单位', value: form.transfer_unit },
  { label: '转移单位地址', value: form.transfer_address },
  { label: '转移联系人', value: form.transfer_contact },
  { label: '转移联系电话', value: form.transfer_phone },
  { label: '接收单位', value: form.receive_unit },
  { label: '接收省份', value: form.receive_province },
  { label: '接收地址', value: form.receive_address },
  { label: '接收联系人', value: form.receive_contact },
  { label: '接收电话', value: form.receive_phone },
  { label: '处置方式', value: form.disposal_method },
  { label: '废物名称', value: form.waste_name },
  { label: '废物类别', value: form.waste_category },
  { label: '废物代码', value: form.waste_code },
  { label: '转移数量(吨)', value: form.transfer_amount },
  { label: '形态', value: form.waste_form },
  { label: '包装方式', value: form.packaging },
  { label: '运输单位', value: form.transport_unit },
  { label: '运输方式', value: form.transport_method },
  { label: '转移期限', value: form.transfer_start && form.transfer_end ? `${form.transfer_start} 至 ${form.transfer_end}` : '' },
])

function handleFileUpload(e, key) {
  const file = e.target.files[0]
  if (file) files[key] = file
}

function removeFile(key) {
  delete files[key]
}

async function nextStep() {
  if (currentStep.value === 1) {
    const required = ['transfer_unit', 'transfer_address', 'transfer_contact', 'transfer_phone',
      'receive_unit', 'receive_province', 'receive_address', 'receive_contact', 'receive_phone',
      'disposal_method', 'waste_name', 'waste_category', 'waste_code', 'transfer_amount',
      'waste_form', 'packaging', 'transport_unit', 'transport_method', 'transfer_start', 'transfer_end']
    for (const key of required) {
      if (!form[key]) {
        alert('请填写所有必填项')
        return
      }
    }
    // 先创建草稿
    if (!applicationId.value) {
      try {
        const res = await createApplication({ ...form })
        applicationId.value = res.data.id
      } catch (e) {
        return
      }
    }
  }
  if (currentStep.value === 2) {
    // 上传文件
    uploading.value = true
    try {
      for (const item of uploadItems) {
        if (files[item.key] && files[item.key] instanceof File) {
          await uploadFile(applicationId.value, item.key, files[item.key])
        }
      }
    } catch (e) {
      uploading.value = false
      return
    }
    uploading.value = false
  }
  currentStep.value++
}

async function handleSubmit() {
  const requiredUploads = uploadItems.map(i => i.key)
  const missing = requiredUploads.filter(k => !files[k])
  if (missing.length > 0) {
    alert('请上传所有必传材料')
    return
  }
  submitting.value = true
  try {
    await submitApplication(applicationId.value)
    alert('申请已提交成功！AI 预审正在进行中，请等待审核。')
    router.push('/applications')
  } catch (e) {
    // 错误已由拦截器处理
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.form-section-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--primary);
  padding-bottom: var(--space-md);
  border-bottom: 1px solid var(--border-light);
  margin-bottom: var(--space-lg);
  margin-top: var(--space-xl);
}
.form-section-title:first-child { margin-top: 0; }
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0 var(--space-xl); }
.upload-list { display: flex; flex-direction: column; gap: var(--space-md); }
.upload-item { display: flex; align-items: center; justify-content: space-between; gap: var(--space-lg); padding: var(--space-lg); background: var(--bg-gray); border-radius: var(--radius); border: 1px solid var(--border-light); }
.upload-item-header { display: flex; align-items: flex-start; gap: var(--space-md); flex: 1; }
.upload-item-num { font-size: 20px; font-weight: 700; color: var(--primary); opacity: 0.3; flex-shrink: 0; line-height: 1; }
.upload-item-title { font-size: 14px; font-weight: 600; color: var(--text); margin-bottom: 4px; }
.upload-item-desc { font-size: 12px; color: var(--text-light); }
.upload-item-action { display: flex; align-items: center; gap: var(--space-sm); flex-shrink: 0; }
.upload-btn { display: inline-flex; align-items: center; padding: 8px 16px; font-size: 13px; color: var(--primary); border: 1px solid var(--primary); border-radius: var(--radius); cursor: pointer; transition: all 0.2s; white-space: nowrap; }
.upload-btn:hover { background: var(--primary-bg); }
.upload-btn input { display: none; }
.file-name { color: var(--success); max-width: 160px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.confirm-section { margin-bottom: var(--space-xl); }
.confirm-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0; border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; }
.confirm-item { display: flex; border-bottom: 1px solid var(--border-light); }
.confirm-item:nth-last-child(-n+2) { border-bottom: none; }
.confirm-label { width: 160px; padding: 10px 16px; background: var(--bg-gray); font-size: 13px; color: var(--text-secondary); font-weight: 500; flex-shrink: 0; }
.confirm-value { flex: 1; padding: 10px 16px; font-size: 14px; color: var(--text); }
.confirm-files { display: flex; flex-direction: column; gap: var(--space-sm); }
.confirm-file { display: flex; align-items: center; gap: var(--space-md); padding: 10px 16px; background: var(--bg-gray); border-radius: var(--radius); }
.confirm-file-icon { font-size: 18px; }
.confirm-file-name { flex: 1; font-size: 14px; color: var(--text); }
.confirm-file-status { font-size: 12px; padding: 2px 8px; border-radius: 3px; font-weight: 500; }
.confirm-file-status.uploaded { background: var(--success-bg); color: var(--success); }
.confirm-file-status.missing { background: var(--error-bg); color: var(--error); }
.confirm-notice { margin-top: var(--space-lg); padding: var(--space-md); background: var(--accent-bg); border-left: 3px solid var(--accent); border-radius: var(--radius-sm); font-size: 13px; color: var(--text-secondary); line-height: 1.6; }
@media (max-width: 768px) {
  .form-grid { grid-template-columns: 1fr; }
  .upload-item { flex-direction: column; align-items: flex-start; }
  .confirm-grid { grid-template-columns: 1fr; }
  .confirm-item:nth-last-child(2) { border-bottom: 1px solid var(--border-light); }
}
</style>