# Agent 指南 - 一般固废备案系统

## 项目概述
- 一般固废备案管理系统
- Django 后端 + Vue 3 前端前后端分离架构

## 技术栈
- **后端**: Python 3.13 + Django 6.0.6 + Django REST Framework 3.17.1
- **前端**: Vue 3 + Vite 8.1 + Vue Router 4 + Axios
- **后台管理**: simpleui（中文界面）
- **数据库**: SQLite3

## 项目结构
```
x:\AI\
├── venv/                           # Python 虚拟环境
├── yiban_gufei_beian/              # Django 项目配置
│   ├── settings.py                 # 项目配置文件
│   ├── urls.py                     # 主路由配置
│   ├── wsgi.py
│   └── asgi.py
├── gufei_beian/                    # Django 应用
│   ├── admin.py                    # 后台注册
│   ├── models.py                   # 数据模型
│   ├── views.py                    # 视图
│   ├── serializers.py              # 序列化器
│   ├── urls.py                     # 应用路由
│   └── migrations/                 # 数据库迁移
├── frontend/                       # Vue 3 前端
│   ├── src/
│   │   ├── router/index.js         # 前端路由
│   │   ├── views/                  # 页面组件
│   │   ├── components/             # 通用组件
│   │   ├── api/                    # API 请求封装
│   │   ├── App.vue                 # 根组件
│   │   ├── main.js                 # 入口文件
│   │   └── style.css               # 全局样式
│   ├── vite.config.js              # Vite 配置（含 /api 代理到 Django）
│   └── package.json
├── static/                         # 收集的静态文件
├── manage.py                       # Django 管理脚本
├── db.sqlite3                      # SQLite 数据库
└── agent.md                        # 本文件（AI 助手指南）
```

## 常用命令

### 后端 (在 x:\AI 目录下)
- 启动 Django 服务器: `.\venv\Scripts\python.exe manage.py runserver 0.0.0.0:8000`
- 创建迁移: `.\venv\Scripts\python.exe manage.py makemigrations`
- 执行迁移: `.\venv\Scripts\python.exe manage.py migrate`
- 创建应用: `.\venv\Scripts\python.exe manage.py startapp <app_name>`
- 创建超级管理员: `.\venv\Scripts\python.exe manage.py createsuperuser`
- 进入 shell: `.\venv\Scripts\python.exe manage.py shell`

### 前端 (在 x:\AI\frontend 目录下)
- 安装依赖: `npm install`
- 启动开发服务器: `npm run dev`
- 构建生产版本: `npm run build`

## API 约定
- 所有 API 接口以 `/api/` 开头
- 前端通过 Vite 代理将 `/api/*` 请求转发到 Django（localhost:8000）
- REST Framework 默认权限: AllowAny

## 开发规则
1. 新增 Django 应用后记得在 `settings.py` 的 `INSTALLED_APPS` 中注册
2. 新增模型后执行 `makemigrations` + `migrate`
3. 前端 API 请求统一放在 `src/api/` 目录下
4. 新增页面在 `src/router/index.js` 中注册路由
5. 后台管理在对应 app 的 `admin.py` 中注册模型
6. 保持前后端分离架构，Django 不渲染前端模板