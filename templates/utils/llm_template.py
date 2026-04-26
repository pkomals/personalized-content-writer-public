"""
LLM Utilities Template

Wrapper functions for LLM API calls with structured output support.
Implement with your LLM provider of choice (Claude, OpenAI, etc.)
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


def generate_text(
    prompt: str,
    system_prompt: str | None = None,
    model: str = "claude-3-5-sonnet-20241022",
    max_tokens: int = 2000,
    temperature: float = 0.7,
) -> str:
    """
    Call LLM for free-form text generation.

    TODO: Implement with your LLM provider
    Example: from anthropic import Anthropic
    """
    logger.info(f"Generating text with {model}...")
    raise NotImplementedError("Implement generate_text with your LLM provider")


def generate_structured(
    prompt: str,
    schema: dict,
    system_prompt: str | None = None,
    model: str = "claude-3-5-sonnet-20241022",
    max_tokens: int = 2000,
) -> dict:
    """
    Call LLM requesting JSON output matching a schema.

    Essential for getting structured, parseable responses from agents.

    TODO: Implement with your LLM provider (use tool_use or JSON mode)
    """
    logger.info(f"Generating structured output with {model}...")
    raise NotImplementedError("Implement generate_structured with your LLM provider")


def batch_generate_structured(
    prompts: list[tuple[str, dict]],
    system_prompt: str | None = None,
    model: str = "claude-3-5-sonnet-20241022",
) -> list[dict]:
    """
    Call LLM multiple times efficiently.

    TODO: Implement with batch API or sequential calls
    """
    logger.info(f"Generating {len(prompts)} structured outputs...")
    raise NotImplementedError("Implement batch_generate_structured")
