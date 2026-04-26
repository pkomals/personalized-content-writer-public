"""
Editor Agent Template

Applies precise micro-edits from human reviewer feedback.
Also extracts reusable rules from feedback (self-improving system).
"""

import logging
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class EditResult(BaseModel):
    """Result of a micro-edit attempt."""
    is_clear: bool
    rewritten_paragraph: str
    reasoning: str


class RuleEvaluationResult(BaseModel):
    """Result of rule extraction evaluation."""
    is_reusable_rule: bool
    extracted_rule: str
    reasoning: str


def get_micro_edit(
    original_text: str,
    current_comment: str,
    all_comments_context: str,
    company_context: dict,
    founder_feedback: dict,
) -> dict:
    """
    Apply a precise micro-edit to a paragraph based on reviewer feedback.

    CRITICAL: Does NOT hallucinate. If ambiguous, mark is_clear=False.

    TODO: Implement with your LLM provider
    See templates/IMPLEMENTATION_GUIDE.md for detailed steps
    """
    logger.info("Applying micro-edit to paragraph...")
    raise NotImplementedError("Implement get_micro_edit with your LLM provider")


def evaluate_reusability(
    current_comment: str,
    all_comments_context: str,
    existing_global_rules: list[str],
) -> dict:
    """
    Determine if a reviewer comment should become a reusable global rule.

    TODO: Implement with your LLM provider
    See templates/IMPLEMENTATION_GUIDE.md for detailed steps
    """
    logger.info("Evaluating if comment should become a global rule...")
    raise NotImplementedError("Implement evaluate_reusability with your LLM provider")
