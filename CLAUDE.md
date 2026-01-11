# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Open-AutoGLM is an AI-powered phone automation framework that controls Android, HarmonyOS, and iOS devices using natural language commands. It uses vision-language models (AutoGLM-Phone-9B) to understand screen content and automatically perform tasks through device automation tools (ADB/HDC/XCTest).

**Core Architecture:**
- **PhoneAgent** (`phone_agent/agent.py`) - Main agent orchestrating automation for Android/HarmonyOS
- **IOSPhoneAgent** (`phone_agent/agent_ios.py`) - Specialized agent for iOS devices
- **ModelClient** (`phone_agent/model/client.py`) - Handles AI model communication via OpenAI-compatible API
- **ActionHandler** (`phone_agent/actions/handler.py`) - Executes device operations (tap, swipe, type, launch, etc.)
- **DeviceFactory** (`phone_agent/device_factory.py`) - Manages connections to ADB/HDC/iOS devices

The agent operates in a loop:
1. Capture device screenshot
2. Send screen + task to vision-language model
3. Parse model response for actions
4. Execute actions on device
5. Repeat until task completion or max steps reached

## Development Setup

### Initial Environment Setup

```bash
# Initialize virtual environment (creates .venv with Python 3.10+)
bash init_venv.sh

# Activate the virtual environment
source .venv/bin/activate
```

The `init_venv.sh` script automatically:
- Finds Python 3.10+ (checks python3.12, python3.11, python3.10, python3)
- Creates `.venv` virtual environment
- Installs project in development mode via `pip install -e .`

### Device Connection Setup

**Android devices (ADB):**
```bash
# Check ADB connection
./check_adb_connection.sh

# Restart ADB service if needed
./restart_adb.sh

# Install ADB Keyboard for text input
./install_adb_keyboard.sh
```

**HarmonyOS devices (HDC):** Similar setup, using `hdc` instead of `adb`

**iOS devices:** Requires WebDriverAgent (WDA) running at specified URL

### Running the Application

**Interactive mode (recommended for development):**
```bash
# Set required environment variables
export ZHIPU_API_KEY=your-api-key

# Run interactive script (supports multiline input)
python run_autoglm.py
```

**Single task execution:**
```bash
# Using Zhipu BigModel service
python main.py \
  --base-url https://open.bigmodel.cn/api/paas/v4 \
  --model "autoglm-phone" \
  --apikey "$ZHIPU_API_KEY" \
  "打开微信搜索美食"

# Using custom model endpoint
python main.py \
  --base-url http://localhost:8000/v1 \
  --model "autoglm-phone-9b" \
  "your task here"
```

**List supported applications:**
```bash
python main.py --list-apps
```

## Code Architecture Details

### Action Types

The framework defines several action types in `phone_agent/actions/handler.py`:

- **Launch** - Start applications by package name or app name
- **Tap** - Click at specific coordinates
- **Type** - Input text (requires ADB Keyboard on Android)
- **Swipe** - Screen gestures with direction and distance
- **Back/Home/Recents** - System navigation
- **Wait** - Pause execution for specified time
- **Take_over** - Request human intervention for sensitive operations (login, captcha)

Each action returns an `ActionResult` with success status, completion flag, and optional message.

### Configuration

**Agent configuration** (`phone_agent/agent.py`):
```python
@dataclass
class AgentConfig:
    max_steps: int = 100          # Maximum steps before timeout
    device_id: str | None = None  # Specific device for multi-device setups
    lang: str = "cn"              # "cn" or "en" for system prompt
    system_prompt: str | None = None
    verbose: bool = True
```

**Model configuration** (`phone_agent/model/client.py`):
```python
@dataclass
class ModelConfig:
    base_url: str = "http://localhost:8000/v1"
    api_key: str = ""
    model_name: str = "autoglm-phone-9b"
    temperature: float = 0.5
    max_tokens: int = 2048
```

### Package Structure

```
phone_agent/
├── __init__.py
├── agent.py              # PhoneAgent for Android/HarmonyOS
├── agent_ios.py          # IOSPhoneAgent
├── model/
│   ├── __init__.py
│   ├── client.py         # ModelClient for API communication
│   └── ...
├── actions/
│   ├── __init__.py
│   ├── handler.py        # ActionHandler and action implementations
│   └── ...
├── adb/                  # Android device tools (screenshot, input, etc.)
├── hdc/                  # HarmonyOS device tools
├── xctest/               # iOS testing tools
├── config/
│   ├── apps.py           # App name to package name mapping
│   └── ...
└── device_factory.py     # Get device connection based on type
```

### Callbacks

The agent supports two important callbacks:

1. **confirmation_callback** - For sensitive actions (e.g., "Call mom"). Should return `True` to proceed, `False` to cancel.

2. **takeover_callback** - When agent encounters login/captcha scenarios and needs human help. Allows human to intervene, then agent continues.

Example:
```python
def confirm_sensitive(action_description: str) -> bool:
    response = input(f"Confirm action: {action_description}? (y/n) ")
    return response.lower() == 'y'

def handle_takeover(reason: str) -> None:
    print(f"Human takeover needed: {reason}")
    input("Press Enter when ready to continue...")

agent = PhoneAgent(
    model_config=config,
    confirmation_callback=confirm_sensitive,
    takeover_callback=handle_takeover
)
```

## Model Deployment

The project requires AutoGLM-Phone-9B model, which can be:

1. **Deployed locally** (~20GB VRAM required) using sglang or vllm
2. **Accessed via APIs** - Zhipu AI (BigModel), ModelScope

Model downloads:
- [AutoGLM-Phone-9B](https://huggingface.co/zai-org/AutoGLM-Phone-9B) - Optimized for Chinese apps
- [AutoGLM-Phone-9B-Multilingual](https://huggingface.co/zai-org/AutoGLM-Phone-9B-Multilingual) - Supports English

## Important Notes

- **Python version:** Requires Python 3.10+ (check setup.py)
- **Type hints:** Code uses modern Python type hints (`str | None` syntax requires 3.10+)
- **Device connection:** Always verify device connection before running tasks
- **ADB Keyboard:** Required for text input on Android devices
- **Remote devices:** Supports WiFi ADB (`adb connect IP:PORT`) and network iOS devices
- **Language support:** System prompts available in Chinese ("cn") and English ("en")

## Utility Scripts

- `init_venv.sh` - Initialize .venv virtual environment
- `check_adb_connection.sh` - Verify ADB device connection
- `restart_adb.sh` - Restart ADB service
- `install_adb_keyboard.sh` - Install ADB Keyboard for text input
- `run_zhipu.sh` - Quick run using Zhipu BigModel API
- `run_autoglm.py` - Interactive mode with multiline input support
