#!/usr/bin/env python3
import os
from phone_agent import PhoneAgent
from phone_agent.model import ModelConfig

def get_multiline_input():
    """获取多行输入，以空行结束"""
    print("请输入任务 (输入空行结束):")
    lines = []
    while True:
        try:
            line = input()
            if line == "":
                break
            lines.append(line)
        except EOFError:
            break
    return "\n".join(lines)

def main():
    # 从环境变量读取配置 (智谱 BigModel)
    api_key = os.getenv('ZHIPU_API_KEY')
    if not api_key:
        print("错误: 请设置ZHIPU_API_KEY环境变量")
        print("示例: export ZHIPU_API_KEY=your-actual-api-key")
        return

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

    print("=" * 50)
    print("AutoGLM 交互模式")
    print("=" * 50)

    while True:
        print("\n" + "-" * 50)
        task = get_multiline_input()

        if not task.strip():
            print("任务为空，跳过...")
            continue

        print(f"\n执行任务: {task}")
        print("-" * 50)
        try:
            result = agent.run(task)
            print(f"\n任务结果: {result}")
        except Exception as e:
            print(f"\n执行出错: {e}")

if __name__ == "__main__":
    main()