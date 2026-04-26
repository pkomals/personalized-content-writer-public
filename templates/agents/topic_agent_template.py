"""
Topic Agent Template

Generates blog topic ideas by clustering existing content and finding gaps.
"""

import logging
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class Topic(BaseModel):
    """A single topic suggestion."""
    title: str
    angle: str
    outline: list[str]
    target_benchmark_persona: str


def generate_topics(
    company_context: dict,
    founder_feedback: dict | None = None,
    num_clusters: int = 5,
    existing_topics: list[str] | None = None,
) -> list[dict]:
    """
    Generate 1-3 blog topic ideas by analyzing content gaps.

    IMPORTANT: Pass company_context to Topic Agent (prevents misaligned topics).

    TODO: Implement with your LLM provider
    See templates/IMPLEMENTATION_GUIDE.md for detailed steps
    """
    logger.info("Generating blog topics...")
    raise NotImplementedError("Implement generate_topics with your LLM provider")


def retrieve_context_for_topic(
    topic: dict,
    n_results: int = 4,
) -> list[str]:
    """
    Retrieve relevant blog excerpts for a given topic.

    TODO: Implement with your vector DB
    """
    logger.info(f"Retrieving context for topic: {topic.get('title')}")
    raise NotImplementedError("Implement retrieve_context_for_topic with your vector DB")
