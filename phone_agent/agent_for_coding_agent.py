"""PhoneAgent optimized for coding agents like Claude Code.

This version provides structured, parseable output without visual decorations
(emoji, separators) that are unnecessary for programmatic consumption.

Usage:
    from phone_agent.agent_for_coding_agent import PhoneAgent
    # Use exactly the same as original PhoneAgent
"""

import json
import traceback
from typing import Any

from phone_agent.model.client import MessageBuilder
from phone_agent.actions.handler import finish, parse_action
from phone_agent.agent import PhoneAgent as BasePhoneAgent, StepResult


class PhoneAgent(BasePhoneAgent):
    """
    PhoneAgent optimized for coding agents.

    Inherits all functionality from base PhoneAgent but overrides
    _execute_step to output structured JSON instead of decorated text.
    """

    def _execute_step(self, user_prompt: str | None = None, is_first: bool = False):
        """Execute a single step with structured JSON output."""
        from phone_agent.device_factory import get_device_factory

        # Increment step counter
        self._step_count += 1

        # Capture current screen state
        device_factory = get_device_factory()
        screenshot = device_factory.get_screenshot(self.agent_config.device_id)
        current_app = device_factory.get_current_app(self.agent_config.device_id)

        # Build messages
        if is_first:
            self._context.append(
                MessageBuilder.create_system_message(self.agent_config.system_prompt)
            )

            screen_info = MessageBuilder.build_screen_info(current_app)
            text_content = f"{user_prompt}\n\n{screen_info}"

            self._context.append(
                MessageBuilder.create_user_message(
                    text=text_content, image_base64=screenshot.base64_data
                )
            )
        else:
            screen_info = MessageBuilder.build_screen_info(current_app)
            text_content = f"** Screen Info **\n\n{screen_info}"

            self._context.append(
                MessageBuilder.create_user_message(
                    text=text_content, image_base64=screenshot.base64_data
                )
            )

        # Get model response
        try:
            response = self.model_client.request(self._context)
        except Exception as e:
            if self.agent_config.verbose:
                print(json.dumps({
                    "error": str(e),
                    "type": "model_error"
                }, ensure_ascii=False))
            if self.agent_config.verbose:
                traceback.print_exc()
            return StepResult(
                success=False,
                finished=True,
                action=None,
                thinking="",
                message=f"Model error: {e}",
            )

        # Parse action from response
        try:
            action = parse_action(response.action)
        except ValueError:
            if self.agent_config.verbose:
                traceback.print_exc()
            action = finish(message=response.action)

        # Output structured JSON for coding agent (no emoji, no separators)
        if self.agent_config.verbose:
            output = {
                "step": self._step_count,
                "thinking": response.thinking,
                "action": action,
            }

            # Only add finished flag if actually finished
            is_finished = action.get("_metadata") == "finish"
            if is_finished:
                output["finished"] = True
                output["message"] = action.get("message", "")

            print(json.dumps(output, ensure_ascii=False, indent=2))

        # Remove image from context to save space
        self._context[-1] = MessageBuilder.remove_images_from_message(self._context[-1])

        # Execute action
        try:
            result = self.action_handler.execute(
                action, screenshot.width, screenshot.height
            )
        except Exception as e:
            if self.agent_config.verbose:
                traceback.print_exc()
            result = self.action_handler.execute(
                finish(message=str(e)), screenshot.width, screenshot.height
            )

        # Add assistant response to context
        self._context.append(
            MessageBuilder.create_assistant_message(
                f"<thinking>{response.thinking}</thinking>\n<answer>{response.action}</answer>"
            )
        )

        # Check if finished
        finished = action.get("_metadata") == "finish" or result.should_finish

        return StepResult(
            success=result.success,
            finished=finished,
            action=action,
            thinking=response.thinking,
            message=result.message or action.get("message"),
        )