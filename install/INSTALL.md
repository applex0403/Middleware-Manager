# 中间件管理平台安装说明

## 版本信息

当前版本: 1.0

## 安装包类型

- **Windows**: `.exe` 可执行文件
- **macOS**: `.dmg` 安装包
- **Linux**: `.zip`、`.deb`、`.rpm` 安装包

## 安装步骤

### 1. 系统要求

- Python 3.7 或更高版本
- 网络连接（用于安装依赖）
- 至少 100MB 可用磁盘空间

### 2. Windows 安装

1. 下载 `middleware-manager-1.0.exe` 安装包
2. 双击运行安装包
3. 按照安装向导完成安装
4. 安装完成后，可从开始菜单或桌面快捷方式启动应用

### 3. macOS 安装

1. 下载 `middleware-manager-1.0.dmg` 安装包
2. 双击打开 DMG 文件
3. 将 "Middleware Manager" 拖拽到 Applications 文件夹
4. 从 Applications 文件夹启动应用

### 4. Linux 安装

#### 使用 .deb 包（Debian/Ubuntu）

```bash
sudo dpkg -i middleware-manager-1.0.deb
sudo apt-get install -f
```

#### 使用 .rpm 包（Red Hat/CentOS）

```bash
sudo rpm -ivh middleware-manager-1.0.rpm
```

#### 使用 .zip 包（通用）

```bash
unzip middleware-manager-1.0.zip
cd middleware-manager-1.0
chmod +x install.sh
./install.sh
```

## 运行应用

### 启动服务

1. **Windows**: 从开始菜单或桌面快捷方式启动
2. **macOS**: 从 Applications 文件夹启动
3. **Linux**: 在终端中运行 `middleware-manager`

### 访问 Web 界面

打开浏览器，访问以下地址：

```
http://localhost:8000
```

## 卸载应用

### Windows

1. 打开 "控制面板" → "程序和功能"
2. 找到 "Middleware Manager"
3. 点击 "卸载"

### macOS

1. 打开 Applications 文件夹
2. 将 "Middleware Manager" 拖拽到废纸篓
3. 清空废纸篓

### Linux

#### 使用 .deb 包安装的

```bash
sudo dpkg -r middleware-manager
```

#### 使用 .rpm 包安装的

```bash
sudo rpm -e middleware-manager
```

#### 使用 .zip 包安装的

```bash
# 删除安装目录
rm -rf middleware-manager-1.0
```

## 常见问题

### 端口被占用

如果 8000 端口被占用，可以修改 `main.py` 文件中的端口配置：

```python
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)  # 修改这里的端口
```

### 依赖安装失败

如果依赖安装失败，请确保网络连接正常，或使用国内镜像源：

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 联系支持

如果遇到安装问题，请联系：
- GitHub Issues: https://github.com/applex0403/Middleware-Manager/issues
