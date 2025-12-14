#!/bin/bash

echo "检查ADB连接状态..."
echo "===================="

# 检查ADB是否已安装
if ! command -v adb &> /dev/null
then
    echo "错误: 未找到ADB命令，请先安装ADB"
    exit 1
fi

echo "ADB版本信息:"
adb version
echo ""

# 检查已连接的设备
echo "正在检查已连接的设备..."
echo "如果设备未显示，请确保："
echo "1. USB数据线已正确连接手机和电脑"
echo "2. 手机已启用开发者选项和USB调试"
echo ""

echo "已连接的设备:"
echo "-------------"
adb devices
echo ""

# 如果有设备连接，获取设备信息
DEVICES=$(adb devices | grep -v "List of devices" | grep -v "^$")

if [ -n "$DEVICES" ]; then
    echo "设备详细信息:"
    echo "-------------"
    MODEL=$(adb shell getprop ro.product.model 2>/dev/null)
    ANDROID_VERSION=$(adb shell getprop ro.build.version.release 2>/dev/null)
    
    if [ -n "$MODEL" ]; then
        echo "$MODEL (设备型号)"
    fi
    
    if [ -n "$ANDROID_VERSION" ]; then
        echo "Android $ANDROID_VERSION (Android版本)"
    fi
    
    echo ""
    echo "连接状态说明:"
    echo "-------------"
    if echo "$DEVICES" | grep -q "unauthorized"; then
        echo "⚠️  设备未授权: 请在手机上确认USB调试授权弹窗，选择'允许'或'始终允许'"
    elif echo "$DEVICES" | grep -q "offline"; then
        echo "⚠️  设备离线: 尝试更换USB线缆或USB端口"
    else
        echo "✅ 设备已正确连接并授权"
        echo ""
        echo "测试截图功能..."
        if adb exec-out screencap -p > /tmp/test_screenshot.png 2>/dev/null; then
            echo "✅ 截图功能正常"
            rm /tmp/test_screenshot.png
        else
            echo "❌ 截图功能异常，请检查权限设置"
        fi
    fi
else
    echo "未检测到设备，请按照以下步骤操作："
    echo ""
    echo "Android设备配置步骤："
    echo "====================="
    echo "1. 在手机上启用开发者选项："
    echo "   - 打开'设置'"
    echo "   - 找到'关于手机'或'关于设备'"
    echo "   - 连续点击'版本号'7次，直到提示'您现在是开发者'"
    echo ""
    echo "2. 启用USB调试："
    echo "   - 返回'设置'主界面"
    echo "   - 找到并进入'开发者选项'"
    echo "   - 启用'USB调试'开关"
    echo "   - 部分手机还需要启用'USB调试(安全设置)'"
    echo ""
    echo "3. 连接设备："
    echo "   - 使用原装或数据传输USB线连接手机和电脑"
    echo "   - 手机上会弹出授权提示，选择'允许'或'始终允许'"
    echo ""
    echo "4. 重新运行此脚本检查连接状态"
    echo ""
    echo "如果仍有问题，可以尝试运行 ./restart_adb.sh 重启ADB服务"
fi