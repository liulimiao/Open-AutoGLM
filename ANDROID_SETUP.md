# Android设备配置指南

## 启用开发者选项和USB调试

### 1. 启用开发者选项
1. 打开手机"设置"
2. 滑动到底部找到"关于手机"或"关于设备"
3. 找到"版本号"或"内部版本号"
4. 连续点击版本号7次
5. 看到"您现在是开发者"的提示后返回设置主菜单

### 2. 启用USB调试
1. 在设置中找到"开发者选项"（通常在"系统"或"更多设置"下）
2. 启用"USB调试"开关
3. 部分手机还需要启用"USB调试(安全设置)"

### 3. 连接设备
1. 使用原装或高质量的数据传输USB线连接手机和电脑
2. 手机上会弹出授权提示，选择"允许"或"始终允许"
3. 部分手机可能需要选择连接方式为"文件传输"或"MTP"

## ADB连接故障排除

### 常见问题及解决方案

#### 问题1: 设备显示为"unauthorized"
**解决方案:**
1. 在手机上确认授权弹窗，选择"允许"或"始终允许"
2. 如果没有弹窗，尝试重新插拔USB线
3. 在开发者选项中关闭并重新打开USB调试
4. 重启手机和电脑

#### 问题2: 设备显示为"offline"
**解决方案:**
1. 更换USB线缆（确保是数据线而非仅充电线）
2. 更换USB接口
3. 重启ADB服务:
   ```bash
   adb kill-server
   adb start-server
   ```

#### 问题3: 设备不显示
**解决方案:**
1. 确保已正确启用开发者选项和USB调试
2. 检查手机的通知栏，可能有USB调试授权请求
3. 在电脑上安装相应的手机驱动程序
4. 尝试在不同的USB端口之间切换

## 安装ADB Keyboard

为了使AutoGLM能够输入中文，需要安装ADB Keyboard：

1. 下载ADB Keyboard APK:
   - GitHub地址: https://github.com/senzhk/ADBKeyBoard/blob/master/ADBKeyboard.apk
2. 在手机上安装APK
3. 启用ADB Keyboard:
   - 打开"设置"
   - 进入"系统" > "语言和输入法" > "虚拟键盘"或"键盘列表"
   - 启用"ADB Keyboard"
   - 设置为默认输入法（可选，AutoGLM会自动切换）

## 验证连接

使用以下命令验证一切是否正常工作:

```bash
# 检查设备连接
adb devices

# 获取设备信息
adb shell getprop ro.product.model
adb shell getprop ro.build.version.release

# 测试截图功能
adb exec-out screencap -p > screenshot.png
```

连接成功后，您就可以开始使用AutoGLM了！