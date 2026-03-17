# 中间件管理平台

一个统一管理中间件的平台，支持配置管理、拓扑显示等功能。

## 功能特点

- **中间件管理**：添加、编辑、删除中间件
- **配置文件管理**：上传、下载、更新配置文件
- **更新策略**：支持立即更新、定时更新、滚动更新
- **拓扑显示**：展示中间件之间的逻辑关系
- **仪表盘**：显示系统概览信息

## 技术栈

- **后端**：FastAPI + SQLite
- **前端**：HTML/CSS/JavaScript + Bootstrap + ECharts

## 快速开始

### 1. 安装依赖

```bash
pip3 install -r requirements.txt
```

### 2. 启动后端服务

```bash
python3 -m uvicorn main:app --reload
```

后端服务将运行在 http://127.0.0.1:8000

### 3. 启动前端服务

```bash
cd frontend
python3 -m http.server 8080
```

前端服务将运行在 http://localhost:8080

## API 文档

后端 API 文档可访问：http://127.0.0.1:8000/docs

## 项目结构

```
Middleware-Manager/
├── main.py                 # FastAPI 后端入口
├── database.py             # 数据库模型
├── api/                    # API 模块
│   ├── middleware.py       # 中间件管理 API
│   └── config.py           # 配置文件管理 API
├── frontend/               # 前端文件
│   └── index.html         # 前端 Web 界面
├── requirements.txt        # Python 依赖
└── middleware.db           # SQLite 数据库
```

## GitHub Pages

前端页面也可以通过 GitHub Pages 访问：
[https://applex0403.github.io/Middleware-Manager/](https://applex0403.github.io/Middleware-Manager/)

## 配置 GitHub Pages

1. 登录 GitHub 账号
2. 进入仓库：[https://github.com/applex0403/Middleware-Manager](https://github.com/applex0403/Middleware-Manager)
3. 点击 "Settings" 选项卡
4. 在左侧菜单中选择 "Pages"
5. 在 "Branch" 下拉菜单中选择 "master"
6. 在 "Folder" 下拉菜单中选择 "/ (root)"
7. 点击 "Save"
8. 等待几分钟后，GitHub Pages 将会部署完成

## 注意事项

- GitHub Pages 版本只能访问前端界面，无法连接到后端 API
- 要使用完整功能，请按照快速开始步骤本地启动服务
