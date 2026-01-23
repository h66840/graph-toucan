#!/bin/bash

# Dataset Viewer启动脚本

echo "======================================"
echo "   Dataset Viewer - Startup Script"
echo "======================================"
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 is not installed"
    exit 1
fi

# 检查是否在正确的目录
if [ ! -f "app.py" ]; then
    echo "Error: app.py not found. Please run this script from the dataset_viewer directory"
    exit 1
fi

# 检查并安装依赖
echo "Checking dependencies..."
pip install -q -r requirements.txt

echo ""
echo "Starting Dataset Viewer..."
echo ""
echo "Access the viewer at: http://localhost:5001"
echo "Press Ctrl+C to stop the server"
echo ""

# 启动应用
python3 app.py
