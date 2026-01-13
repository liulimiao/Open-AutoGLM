#!/bin/bash

echo "重启ADB服务..."
echo "=============="

echo "停止ADB服务..."
adb kill-server
sleep 2

echo "启动ADB服务..."
adb start-server
sleep 2

echo "检查设备连接..."
echo "==============="
adb devices

echo ""
echo "如果设备仍显示为'unauthorized'，请:"
echo "1. 检查手机上是否有授权弹窗并点击'允许'"
echo "2. 在开发者选项中关闭并重新打开USB调试"
echo "3. 重新插拔USB线"