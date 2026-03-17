# 中间件管理平台

一个统一管理中间件的平台，支持配置管理、拓扑显示等功能。

## 版本信息

当前版本: 1.0

## 功能特点

- **中间件管理**：添加、编辑、删除中间件
- **配置文件管理**：上传、下载、更新配置文件
- **更新策略**：支持立即更新、定时更新、滚动更新
- **拓扑显示**：展示中间件之间的逻辑关系
- **仪表盘**：显示系统概览信息
- **多平台支持**：支持 Windows、macOS、Linux，提供多种格式安装包

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
├── install/                # 安装包配置
│   ├── dist/               # 编译输出目录
│   ├── package.py          # 打包脚本
│   ├── INSTALL.md          # 安装说明
│   └── version.txt         # 版本信息
├── requirements.txt        # Python 依赖
├── README.md               # 项目说明
├── index.html              # 前端入口（用于 GitHub Pages）
└── middleware.db           # SQLite 数据库
```

## GitHub Pages

前端页面也可以通过 GitHub Pages 访问：
[https://applex0403.github.io/Middleware-Manager/](https://applex0403.github.io/Middleware-Manager/)

## 安装包下载

项目提供多种格式的安装包，方便在不同操作系统上安装：

- **Windows**: `.exe` 可执行文件
- **macOS**: `.dmg` 安装包
- **Linux**: `.zip`、`.deb`、`.rpm` 安装包

详细安装说明请参考 [INSTALL.md](install/INSTALL.md)。

## 配置 GitHub Pages

1. 登录 GitHub 账号
2. 进入仓库：[https://github.com/applex0403/Middleware-Manager](https://github.com/applex0403/Middleware-Manager)
3. 点击 "Settings" 选项卡
4. 在左侧菜单中选择 "Pages"
5. 在 "Branch" 下拉菜单中选择 "main"
6. 在 "Folder" 下拉菜单中选择 "/ (root)"
7. 点击 "Save"
8. 等待几分钟后，GitHub Pages 将会部署完成

## 注意事项

- GitHub Pages 版本只能访问前端界面，无法连接到后端 API
- 要使用完整功能，请按照快速开始步骤本地启动服务
