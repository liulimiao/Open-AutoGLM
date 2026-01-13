#!/usr/bin/env python3
"""
Thinking Output Demo for Coding Agents / 编程代理的 thinking 输出示例

This script demonstrates how the Agent outputs structured JSON in verbose mode,
optimized for coding agents like Claude Code.
这个脚本展示了在 verbose 模式下，Agent 输出结构化 JSON，专为 Claude Code 等编程代理优化。

Output format: Structured JSON (no emoji, no separators)
输出格式：结构化 JSON（无 emoji，无分隔线）
"""

from phone_agent.agent_for_coding_agent import PhoneAgent
from phone_agent.agent import AgentConfig
from phone_agent.config import get_messages
from phone_agent.model import ModelConfig


def main(lang: str = "cn"):
    msgs = get_messages(lang)

    print("=" * 60)
    print("Phone Agent - Coding Agent Version")
    print("Output: Structured JSON (no emoji, no separators)")
    print("=" * 60)

    # Configure model
    model_config = ModelConfig(
        base_url="http://localhost:8000/v1",
        model_name="autoglm-phone-9b",
        temperature=0.1,
    )

    # Configure Agent (verbose=True enables detailed output)
    agent_config = AgentConfig(
        max_steps=10,
        verbose=True,
        lang=lang,
    )

    # Create Agent (coding agent version)
    agent = PhoneAgent(
        model_config=model_config,
        agent_config=agent_config,
    )

    # Execute task
    print(f"\n{msgs['starting_task']}...\n")
    result = agent.run("打开小红书搜索美食攻略")

    print("\n" + "=" * 60)
    print(f"{msgs['final_result']}: {result}")
    print("=" * 60)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Phone Agent Demo - Coding Agent Version"
    )
    parser.add_argument(
        "--lang",
        type=str,
        default="cn",
        choices=["cn", "en"],
        help="Language for UI messages (cn=Chinese, en=English)",
    )
    args = parser.parse_args()

    main(lang=args.lang)
