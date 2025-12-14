#!/bin/bash

# 检查是否提供了API Key
if [ -z "$1" ]; then
    echo "使用方式: ./run_zhipu.sh <your-zhipu-api-key> [task]"
    echo "示例: ./run_zhipu.sh your-api-key-here \"打开微信，对文件传输助手发送消息：你好，AutoGLM！\""
    exit 1
fi

API_KEY=$1
TASK=${2:-"打开美团搜索附近的火锅店"}

# 检查虚拟环境是否存在
if [ ! -f "venv/bin/activate" ]; then
    echo "错误: 找不到虚拟环境，请先运行安装脚本"
    exit 1
fi

# 激活虚拟环境
source venv/bin/activate

# 验证依赖是否已安装
if ! venv/bin/python3.10 -c "import openai" 2>/dev/null; then
    echo "错误: 缺少必要的依赖，请确保已在虚拟环境中正确安装依赖"
    exit 1
fi

# 使用智谱 BigModel 运行AutoGLM
echo "使用智谱 BigModel 平台"
venv/bin/python3.10 main.py \
  --base-url https://open.bigmodel.cn/api/paas/v4 \
  --model "autoglm-phone" \
  --apikey "$API_KEY" \
  "$TASK"