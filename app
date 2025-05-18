app/
├── client/                  # 前端代码（React/Vue/Angular 等）
│   ├── public/             # 静态资源（HTML模板、图片等）
│   │   ├── favicon.ico
│   │   └── robots.txt
│   ├── src/                # 前端核心源码
│   │   ├── assets/        # 静态资源（图片、字体、样式等）
│   │   ├── components/    # 可复用的 UI 组件（按钮、卡片等）
│   │   ├── pages/         # 页面级组件（如 HomePage、LoginPage）
│   │   ├── services/      # API 请求封装（axios 实例、接口定义）
│   │   ├── utils/         # 工具函数（日期处理、字符串格式化）
│   │   ├── App.jsx        # 根组件
│   │   └── index.jsx      # 入口文件
│   ├── .eslintrc          # ESLint 配置（代码风格检查）
│   ├── .prettierrc        # Prettier 配置（代码格式化）
│   └── package.json       # 前端依赖管理
│
├── server/                # 后端代码（Node.js/Python/Go 等）
│   ├── src/              # 后端源码
│   │   ├── controllers/  # 控制器（处理请求逻辑）
│   │   ├── models/       # 数据模型（ORM 定义）
│   │   ├── routes/       # API 路由定义
│   │   └── app.js        # 服务入口
│   ├── config/           # 配置文件（数据库、环境变量）
│   └── package.json      # 后端依赖管理（Node.js 项目）
│
├── docs/                  # 项目文档
│   ├── API.md            # API 接口文档
│   └── ARCHITECTURE.md    # 架构设计说明
│
├── tests/                 # 测试代码
│   ├── unit/             # 单元测试
│   └── e2e/              # 端到端测试（Cypress/Selenium）
│
├── scripts/               # 自动化脚本
│   ├── deploy.sh         # 部署脚本
│   └── setup.sh          # 环境初始化脚本
│
├── .github/               # GitHub 配置
│   └── workflows/        # CI/CD 流水线（GitHub Actions）
│
├── .gitignore             # Git 忽略规则（已配置）
├── README.md              # 项目说明（必填！）
└── package.json           # 根目录（若为 monorepo 管理）
