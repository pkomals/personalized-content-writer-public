"""
Writer Agent Template

Responsible for drafting long-form blog posts based on topic, style profile,
and company constraints. This agent receives guidance from Topic Agent and
must strictly adhere to company global rules.

This is a TEMPLATE. Implement your own LLM logic here.
"""

import logging
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class WriterConfig(BaseModel):
    """Configuration for Writer Agent."""
    model: str = "claude-3-5-sonnet"
    max_tokens: int = 2000
    temperature: float = 0.7


def draft_blog(
    topic: dict,
    style_profile: dict,
    context_docs: list,
    company_context: dict,
    founder_feedback: dict,
    feedback: str | None = None,
) -> str:
    """
    Draft a long-form blog post using topic, style profile, and company constraints.

    Args:
        topic: {"title": str, "angle": str, "outline": list[str], "target_benchmark_persona": str}
        style_profile: {"tone": str, "avg_sentence_length": str, ...}
        context_docs: list[str] - Relevant passages from corpus
        company_context: {"target_audience": str, "tone_guardrails": str, ...}
        founder_feedback: {"global_rules": list[str], ...}
        feedback: Optional critic feedback for revision

    Returns:
        str: Markdown blog post with H1 title, H2/H3 sections, CTA in tags

    TODO: Implement with your LLM provider
    See templates/IMPLEMENTATION_GUIDE.md for detailed steps
    """
    logger.info(f"Drafting blog: {topic.get('title')}")
    raise NotImplementedError("Implement draft_blog with your LLM provider")
