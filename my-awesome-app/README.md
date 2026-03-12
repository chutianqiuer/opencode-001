# RBAC Admin System

企业级 FastAPI + Vue 通用后台管理系统（RBAC权限管理）

## 技术栈

### 后端
- FastAPI + Python 3.11+
- SQLAlchemy 2.0 (async)
- Alembic (数据库迁移)
- Pydantic v2 (数据验证)
- PyJWT (认证)
- MySQL 8
- Redis

### 前端
- Vue 3 + TypeScript
- Vite
- Element Plus
- Pinia
- Vue Router

## 快速开始

### 使用 Docker Compose

```bash
# 复制环境变量
cp .env.example .env

# 启动所有服务
docker-compose up -d

# 访问应用
# 前端: http://localhost:3000
# 后端 API: http://localhost:8000
# API 文档: http://localhost:8000/docs
```

### 本地开发

#### 后端

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 运行数据库迁移
alembic upgrade head

# 启动服务
uvicorn app.main:app --reload
```

#### 前端

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

## 默认账户

- 用户名: `admin`
- 密码: `Admin@123`

## 功能特性

- 用户登录 + 图形验证码 + JWT 鉴权
- 部门管理（树形结构）
- 岗位管理
- 菜单管理（权限分配）
- 角色管理
- 用户管理
- 操作日志 + 登录日志
- 权限控制精准到按钮级别

## 项目结构

```
backend/
├── app/
│   ├── models/         # 数据库模型
│   ├── schemas/        # Pydantic 模式
│   ├── crud/           # CRUD 操作
│   ├── routers/        # API 路由
│   ├── middleware/     # 中间件
│   └── utils/          # 工具函数
└── alembic/            # 数据库迁移

frontend/
├── src/
│   ├── views/          # 页面组件
│   ├── api/            # API 服务
│   ├── store/          # Pinia 状态
│   ├── components/     # 公共组件
│   └── router/         # 路由配置
└── public/
```

## License

MIT