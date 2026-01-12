#!/bin/bash

set -e

echo "================================"
echo "初始化 .venv 虚拟环境"
echo "================================"
echo ""

# 检查Python 3.10+是否可用
PYTHON_CMD=""
for cmd in python3.12 python3.11 python3.10 python3; do
    if command -v $cmd &> /dev/null; then
        PYTHON_VERSION=$($cmd --version 2>&1 | awk '{print $2}')
        PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
        PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

        if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 9 ]; then
            PYTHON_CMD=$cmd
            echo "✓ 找到 Python $PYTHON_VERSION: $cmd"
            break
        fi
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo "错误: 未找到 Python 3.10 或更高版本"
    echo "请先安装 Python 3.10+"
    exit 1
fi

echo ""

# 创建虚拟环境
echo "创建 .venv 虚拟环境..."
$PYTHON_CMD -m venv .venv

echo ""
echo "安装项目到开发模式..."
source .venv/bin/activate
pip install -e .

echo ""
echo "================================"
echo "✓ 初始化完成！"
echo "================================"
echo ""
echo "使用方式:"
echo "  source .venv/bin/activate"
echo "  python run_autoglm.py"
echo ""
