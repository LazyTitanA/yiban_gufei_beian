<template>
  <footer class="app-footer">
    <div class="footer-links">
      <div class="container footer-links-inner">
        <div class="footer-col">
          <h4>关于我们</h4>
          <a href="#">系统简介</a>
          <a href="#">联系方式</a>
          <a href="#">法律声明</a>
        </div>
        <div class="footer-col">
          <h4>办事指南</h4>
          <a href="#">备案流程</a>
          <a href="#">材料清单</a>
          <a href="#">常见问题</a>
        </div>
        <div class="footer-col">
          <h4>政策法规</h4>
          <a href="#">《固体废物污染环境防治法》</a>
          <a href="#">青海省固废管理办法</a>
          <a href="#">跨省转移管理规定</a>
        </div>
        <div class="footer-col">
          <h4>联系我们</h4>
          <p>青海省生态环境厅</p>
          <p>电话：0971-1234567</p>
          <p>地址：青海省西宁市</p>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <div class="container">
        <p>主办单位：青海省生态环境厅&nbsp;&nbsp;|&nbsp;&nbsp;承办单位：青海省固体废物管理中心</p>
        <p>备案号：青ICP备XXXXXXXX号&nbsp;&nbsp;|&nbsp;&nbsp;政府网站标识码：XXXXXXXX</p>
        <p class="copyright">Copyright &copy; 2024 青海省生态环境厅 版权所有</p>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.app-footer {
  background: var(--primary-dark);
  color: rgba(255,255,255,0.7);
  margin-top: var(--space-3xl);
}

.footer-links {
  padding: var(--space-2xl) 0 var(--space-xl);
  border-bottom: 1px solid rgba(255,255,255,0.1);
}

.footer-links-inner {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-xl);
}

.footer-col h4 {
  color: #FFFFFF;
  font-size: 16px;
  font-weight: 500;
  margin-bottom: var(--space-lg);
}

.footer-col a {
  display: block;
  color: rgba(255,255,255,0.6);
  font-size: 13px;
  margin-bottom: var(--space-sm);
  text-decoration: none;
}

.footer-col a:hover {
  color: #FFFFFF;
}

.footer-col p {
  font-size: 13px;
  margin-bottom: var(--space-xs);
  color: rgba(255,255,255,0.6);
}

.footer-bottom {
  padding: var(--space-lg) 0;
  text-align: center;
  font-size: 12px;
  line-height: 2;
  color: rgba(255,255,255,0.4);
}

.copyright {
  margin-top: var(--space-sm);
}

@media (max-width: 768px) {
  .footer-links-inner {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>