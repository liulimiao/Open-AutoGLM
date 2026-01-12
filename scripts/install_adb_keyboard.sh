#!/bin/bash

echo "下载并安装ADB Keyboard..."
echo "========================="

# 创建临时目录
TEMP_DIR="/tmp/adb_keyboard"
mkdir -p "$TEMP_DIR"
cd "$TEMP_DIR"

echo "正在下载ADB Keyboard..."
curl -L -o ADBKeyboard.apk "https://github.com/senzhk/ADBKeyBoard/blob/master/ADBKeyboard.apk?raw=true"

if [ $? -eq 0 ]; then
    echo "下载完成，正在安装到设备..."
    
    # 检查是否有设备连接
    DEVICES=$(adb devices | grep -v "List of devices" | grep -v "^$")
    
    if [ -n "$DEVICES" ] && ! echo "$DEVICES" | grep -q "unauthorized"; then
        adb install ADBKeyboard.apk
        
        if [ $? -eq 0 ]; then
            echo "✅ ADB Keyboard安装成功！"
            echo ""
            echo "请在手机上手动启用ADB Keyboard："
            echo "1. 打开'设置'"
            echo "2. 进入'系统' > '语言和输入法' > '虚拟键盘'或'键盘列表'"
            echo "3. 启用'ADB Keyboard'"
            echo ""
            echo "注意：AutoGLM会在需要时自动切换到ADB Keyboard，您无需将其设为默认输入法。"
        else
            echo "❌ 安装失败，请检查设备连接状态"
        fi
    else
        echo "❌ 未检测到已授权的设备，请先确保设备正确连接"
        echo "运行 ./check_adb_connection.sh 检查连接状态"
    fi
else
    echo "❌ 下载失败，请检查网络连接"
fi

# 清理临时文件
cd -
rm -rf "$TEMP_DIR"