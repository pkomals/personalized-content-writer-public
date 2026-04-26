"""
Critic Agent Template

Evaluates drafted blog posts across 10 dimensions and provides revision feedback.
"""

import logging
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class CriticEvaluation(BaseModel):
    """Structured output from Critic Agent."""
    score: int
    feedback: str
    sub_scores: dict
    proposed_new_rules: list[str] = []


CRITIC_SCHEMA = {
    "type": "object",
    "properties": {
        "score": {"type": "integer", "description": "1-10 overall score"},
        "feedback": {"type": "string"},
        "sub_scores": {
            "type": "object",
            "properties": {
                "style_match": {"type": "integer"},
                "depth": {"type": "integer"},
                "hook_strength": {"type": "integer"},
                "generic_content": {"type": "integer"},
                "outline_adherence": {"type": "integer"},
                "structure": {"type": "integer"},
                "cta_effectiveness": {"type": "integer"},
                "seo_structure": {"type": "integer"},
                "company_alignment": {"type": "integer"},
                "feedback_compliance": {"type": "integer"},
            },
            "required": ["style_match", "depth", "hook_strength", "generic_content",
                        "outline_adherence", "structure", "cta_effectiveness",
                        "seo_structure", "company_alignment", "feedback_compliance"]
        },
        "proposed_new_rules": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["score", "feedback", "sub_scores"]
}


def evaluate_blog(
    draft: str,
    style_profile: dict,
    benchmark_insights: dict,
    topic: dict,
    company_context: dict,
    founder_feedback: dict,
) -> dict:
    """
    Score blog draft across 10 dimensions.

    TODO: Implement with your LLM provider
    See templates/IMPLEMENTATION_GUIDE.md for detailed steps
    """
    logger.info("Evaluating blog draft...")
    raise NotImplementedError("Implement evaluate_blog with your LLM provider")
