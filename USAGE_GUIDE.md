# AutoGLM完整配置和使用指南

## 1. 环境配置检查清单

- [ ] Python 3.10+ 已安装
- [ ] 项目依赖已安装
- [ ] ADB已安装
- [ ] Android设备已连接并授权
- [ ] ADB Keyboard已安装并启用

## 2. 环境验证脚本

### 检查ADB连接状态
```bash
./check_adb_connection.sh
```

### 重启ADB服务
```bash
./restart_adb.sh
```

### 安装ADB Keyboard
```bash
./install_adb_keyboard.sh
```

## 3. 运行AutoGLM

### 使用智谱 BigModel 服务运行
```bash
# 方式1: 使用专用脚本
./run_zhipu.sh your-zhipu-api-key "你的任务指令"

# 方式2: 直接使用Python命令
python main.py \
  --base-url https://open.bigmodel.cn/api/paas/v4 \
  --model "autoglm-phone" \
  --apikey "your-zhipu-api-key" \
  "打开美团搜索附近的火锅店"
```

## 4. 常见问题解决

### ADB连接问题
1. 确保手机已启用开发者选项和USB调试
2. 确保在手机上授权了调试请求
3. 尝试更换USB线缆或接口
4. 使用`./restart_adb.sh`重启ADB服务

### ADB Keyboard问题
1. 确保已安装ADB Keyboard
2. 在设置中启用ADB Keyboard
3. AutoGLM会自动切换输入法，无需手动设置为默认

### 模型服务问题
1. 确保智谱 API Key正确
2. 检查网络连接
3. 确认智谱账户有足够额度

## 5. 示例任务

```bash
# 使用智谱 BigModel
./run_zhipu.sh your-zhipu-api-key "打开微信"

# 使用命令行
python main.py \
  --base-url https://open.bigmodel.cn/api/paas/v4 \
  --model "autoglm-phone" \
  --apikey "your-zhipu-api-key" \
  "打开微信"

# 复杂任务
python main.py \
  --base-url https://open.bigmodel.cn/api/paas/v4 \
  --model "autoglm-phone" \
  --apikey "your-zhipu-api-key" \
  "打开美团搜索附近的火锅店，并选择评分最高的"
```

## 6. 高级配置

### 配置文件 (.env)
编辑`.env`文件来保存常用配置：
```
# 智谱 BigModel 配置
ZHIPU_API_KEY=your-zhipu-api-key
ZHIPU_BASE_URL=https://open.bigmodel.cn/api/paas/v4
ZHIPU_MODEL_NAME=autoglm-phone
```

### Python API使用
```python
from phone_agent import PhoneAgent
from phone_agent.model import ModelConfig

# 配置模型 (智谱 BigModel)
model_config = ModelConfig(
    base_url="https://open.bigmodel.cn/api/paas/v4",
    api_key="your-zhipu-api-key",
    model_name="autoglm-phone",
)

# 创建 Agent
agent = PhoneAgent(model_config=model_config)

# 执行任务
result = agent.run("打开美团搜索附近的火锅店")
```

### 使用 run_autoglm.py 脚本

该项目包含一个预配置的脚本 [run_autoglm.py](file:///Users/chenlijun/dev/Open-AutoGLM/run_autoglm.py)，它默认使用智谱 BigModel 平台：

```bash
# 设置环境变量
export ZHIPU_API_KEY=your-zhipu-api-key

# 运行脚本
python run_autoglm.py
```

## 7. 开发和调试

### 运行测试
```bash
pytest tests/
```

### 启用Verbose模式查看详细过程
```bash
python main.py --verbose \
  --base-url https://open.bigmodel.cn/api/paas/v4 \
  --model "autoglm-phone" \
  --apikey "your-zhipu-api-key" \
  "打开微信"
```

## 8. 远程调试

AutoGLM也支持通过WiFi进行远程调试：

1. 在手机上启用无线调试
2. 使用`adb connect IP:PORT`连接设备
3. 指定设备ID运行：
   ```bash
   # 使用智谱 BigModel
   python main.py --device-id IP:PORT \
     --base-url https://open.bigmodel.cn/api/paas/v4 \
     --model "autoglm-phone" \
     --apikey "your-zhipu-api-key" \
     "打开抖音刷视频"
   ```

---
如需更多帮助，请参考项目根目录下的以下文档：
- [README.md](README.md) - 项目详细介绍
- [README_en.md](README_en.md) - 英文文档
- [ANDROID_SETUP.md](ANDROID_SETUP.md) - Android设备配置指南