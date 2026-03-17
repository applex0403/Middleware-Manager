#!/usr/bin/env python3
import os
import sys
import shutil
import zipfile
import subprocess
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
# 安装包输出目录
OUTPUT_DIR = PROJECT_ROOT / "install" / "dist"

# 确保输出目录存在
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def run_command(cmd, cwd=None):
    """运行命令并返回结果"""
    print(f"执行命令: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"命令执行失败: {result.stderr}")
        sys.exit(1)
    return result.stdout

def install_dependencies():
    """安装依赖"""
    print("安装依赖...")
    run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], cwd=PROJECT_ROOT)
    # 安装 PyInstaller
    run_command([sys.executable, "-m", "pip", "install", "pyinstaller"])

def build_executable():
    """构建可执行文件"""
    print("构建可执行文件...")
    # 使用 PyInstaller 构建可执行文件
    cmd = [
        "pyinstaller",
        "--onefile",
        "--name", "middleware-manager",
        "--add-data", "index.html:.",
        "--add-data", "frontend:frontend",
        "--add-data", "api:api",
        "--add-data", "database.py:.",
        "--add-data", "requirements.txt:.",
        "main.py"
    ]
    run_command(cmd, cwd=PROJECT_ROOT)

def create_zip_package():
    """创建 ZIP 安装包"""
    print("创建 ZIP 安装包...")
    zip_path = OUTPUT_DIR / "middleware-manager-1.0.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        # 添加可执行文件
        exe_path = PROJECT_ROOT / "dist" / "middleware-manager"
        if exe_path.exists():
            zf.write(exe_path, "middleware-manager")
        # 添加其他必要文件
        for file in ["index.html", "requirements.txt"]:
            file_path = PROJECT_ROOT / file
            if file_path.exists():
                zf.write(file_path, file)
        # 添加目录
        for dir_name in ["api", "frontend"]:
            dir_path = PROJECT_ROOT / dir_name
            if dir_path.exists():
                for root, _, files in os.walk(dir_path):
                    for file in files:
                        file_path = Path(root) / file
                        arcname = str(file_path.relative_to(PROJECT_ROOT))
                        zf.write(file_path, arcname)
    print(f"ZIP 安装包创建成功: {zip_path}")

def create_install_scripts():
    """创建安装脚本"""
    print("创建安装脚本...")
    
    # 创建 Windows 安装脚本
    win_script = OUTPUT_DIR / "install.bat"
    win_script.write_text("""
@echo off
echo 安装中间件管理平台...
echo 正在安装依赖...
pip install -r requirements.txt
echo 安装完成！
echo 运行: middleware-manager
pause
""")
    
    # 创建 Linux/Mac 安装脚本
    unix_script = OUTPUT_DIR / "install.sh"
    unix_script.write_text("""
#!/bin/bash
echo "安装中间件管理平台..."
echo "正在安装依赖..."
pip3 install -r requirements.txt
echo "安装完成！"
echo "运行: ./middleware-manager"
""")
    unix_script.chmod(0o755)

def main():
    """主函数"""
    try:
        install_dependencies()
        build_executable()
        create_zip_package()
        create_install_scripts()
        print("\n打包完成！安装包已生成到 install/dist 目录")
    except Exception as e:
        print(f"打包过程中出错: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
