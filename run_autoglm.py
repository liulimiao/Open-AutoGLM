#!/usr/bin/env python3
import os
from phone_agent import PhoneAgent
from phone_agent.model import ModelConfig

def main():
    # 从环境变量读取配置 (智谱 BigModel)
    api_key = os.getenv('ZHIPU_API_KEY', 'your-zhipu-api-key')
    base_url = os.getenv('ZHIPU_BASE_URL', 'https://open.bigmodel.cn/api/paas/v4')
    model_name = os.getenv('ZHIPU_MODEL_NAME', 'autoglm-phone')
    
    # 配置模型 (智谱 BigModel)
    model_config = ModelConfig(
        base_url=base_url,
        api_key=api_key,
        model_name=model_name,
    )

    # 创建 Agent
    agent = PhoneAgent(model_config=model_config)

    # 执行任务示例
    task = "打开微信，对文件传输助手发送消息：你好，AutoGLM！"
    print(f"执行任务: {task}")
    result = agent.run(task)
    print(f"任务结果: {result}")

if __name__ == "__main__":
    main()