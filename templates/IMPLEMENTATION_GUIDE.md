# Implementation Guide: Multi-Agent Content Generation Framework

This directory contains **templates** for a production-grade multi-agent content generation system. Fork this repo and implement these templates to build your own AI-powered blog writing engine.

## Overview

This is not a plug-and-play tool. It's a **framework and reference architecture**. You'll implement:

1. **5 core agents** (topic, writer, critic, editor, SEO)
2. **LLM wrappers** (API calls to your preferred provider)
3. **Pipeline orchestration** (weekly scheduling)
4. **Feedback loop** (human review → auto-edits → rule extraction)

---

## Quick Start

### 1. Prerequisites

- Python 3.11+
- LLM API access (Claude, OpenAI, etc.)
- Vector DB (ChromaDB, Pinecone, Weaviate)
- Notion API (optional, for review layer)

### 2. Installation

```bash
# Clone this repo
git clone https://github.com/YOUR_USERNAME/personalized-content-writer-public.git
cd personalized-content-writer-public

# Install dependencies
uv sync

# Create .env
cp .env.example .env
# Fill in: ANTHROPIC_API_KEY, GOOGLE_DRIVE_FOLDER_ID, etc.
```

### 3. Implement Templates

Start with this order:

1. **`templates/utils/llm_template.py`** — LLM API wrapper
2. **`templates/agents/topic_agent_template.py`** — Topic generation
3. **`templates/agents/writer_agent_template.py`** — Blog drafting
4. **`templates/agents/critic_agent_template.py`** — Quality evaluation
5. **`templates/agents/editor_agent_template.py`** — Human feedback loop

---

## Implementation Walkthrough

### Step 1: LLM Wrapper (`utils/llm_template.py`)

This is foundational. Choose your LLM provider and implement:

**`generate_text(prompt, system_prompt)`**
- Call your LLM
- Return markdown/text

**`generate_structured(prompt, schema)`**
- Call your LLM requesting JSON
- Validate against schema
- Return parsed dict

**Example with Claude:**

```python
from anthropic import Anthropic

def generate_text(prompt, system_prompt, ...):
    client = Anthropic()
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2000,
        system=system_prompt,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text

def generate_structured(prompt, schema, ...):
    # Use tool_use or native JSON mode
    # Return parsed JSON dict
```

### Step 2: Topic Agent (`agents/topic_agent_template.py`)

Generates blog topic ideas by analyzing content gaps.

**Key functions:**

```python
def generate_topics(company_context, founder_feedback, num_clusters=5, existing_topics=None):
    """
    Return: list[dict] with:
    {
        "title": "Blog Title",
        "angle": "Unique perspective",
        "outline": ["point 1", "point 2", ...],
        "target_benchmark_persona": "persona name"
    }
    """
```

**Implementation approach:**

1. Retrieve all docs from your vector DB (ChromaDB, Pinecone, etc.)
2. Cluster embeddings using K-means (num_clusters param)
3. Sample representative docs per cluster
4. Call LLM: "Given these content samples, what underexplored angles exist?"
5. Include company_context and founder_feedback as constraints
6. Request structured JSON output
7. Validate against existing_topics

**Critical:** Pass company context to Topic Agent (this prevents misaligned topic generation).

### Step 3: Writer Agent (`agents/writer_agent_template.py`)

Drafts blog posts with style consistency and company alignment.

**Key function:**

```python
def draft_blog(topic, style_profile, context_docs, company_context, founder_feedback, feedback=None):
    """
    Return: Markdown blog post with:
    - H1 title (once at top)
    - H2/H3 sections
    - CTA in <!-- FOOTNOTE_START/END --> tags
    """
```

**Implementation approach:**

1. Build comprehensive system prompt (ghostwriter role, context)
2. Construct user prompt with:
   - Topic (title, angle, outline)
   - Style profile (enforce tone, sentence length, vocabulary)
   - Company context (target audience, guardrails)
   - Founder global rules (marked as immutable)
   - Context docs (for grounding, not copying)
3. If `feedback` param: include critic feedback for revision
4. Call LLM, request markdown
5. Validate structure (H1/H2/H3, CTA tags)

**Key insight:** Company rules should be treated as hard constraints, not suggestions.

### Step 4: Critic Agent (`agents/critic_agent_template.py`)

Evaluates blog quality across 10 dimensions.

**Key function:**

```python
def evaluate_blog(draft, style_profile, benchmark_insights, topic, company_context, founder_feedback):
    """
    Return: {
        "score": 1-10,
        "feedback": "revision instructions",
        "sub_scores": {
            "style_match": 7,
            "depth": 8,
            ...
        },
        "proposed_new_rules": ["rule1"]
    }
    """
```

**The 10 dimensions:**

1. **style_match**: Does it match the voice profile?
2. **depth**: Is it specific and insightful?
3. **hook_strength**: Compelling opening?
4. **generic_content**: Avoids AI fluff?
5. **outline_adherence**: Covers all points?
6. **structure**: Proper H1/H2/H3?
7. **cta_effectiveness**: Strong call-to-action?
8. **seo_structure**: SEO-friendly headings?
9. **company_alignment**: Serves company goals?
10. **feedback_compliance**: Adheres to global rules?

**Scoring:**
- 1-3: Major revision needed
- 4-6: Significant gaps
- 7-8: Good, minor tweaks
- 9-10: Ready for review

**Implementation:**
1. Build evaluation prompt describing each dimension
2. Include all context (draft, style, company constraints, rules)
3. Call LLM with structured output
4. Return 1-10 score + feedback + sub_scores

### Step 5: Editor Agent (`agents/editor_agent_template.py`)

Applies human reviewer feedback as precise edits.

**Two key functions:**

**`get_micro_edit(original_text, comment, context, ...)`**

```python
def get_micro_edit(...):
    """
    Return: {
        "is_clear": bool,  # Can intent be determined?
        "rewritten_paragraph": str,  # Edited text (empty if unclear)
        "reasoning": str
    }
    """
```

**Key behavior:**
- If comment is CLEAR: Rewrite the paragraph
- If comment is AMBIGUOUS: Mark `is_clear=False`, do NOT hallucinate
- Use chronological comment context to resolve vague comments
- Only rewrite the specific paragraph (preserve tone)

**`evaluate_reusability(comment, context, existing_rules)`**

```python
def evaluate_reusability(...):
    """
    Return: {
        "is_reusable_rule": bool,
        "extracted_rule": str,
        "reasoning": str
    }
    """
```

**Classification:**

Bucket A (One-off → False):
- Formatting requests
- Narrative shifts for this blog
- Comments already covered by existing rules

Bucket B (Reusable → True):
- Terminology/vocabulary rules
- Factual definitions
- Target audience constraints
- Systemic guardrails

---

## Architecture Patterns

### 1. Context Propagation (Critical)

Every agent that makes decisions should receive:
- Company context (target audience, guardrails, goals)
- Founder global rules (non-negotiable constraints)

This prevents agents from drifting into misaligned output.

**Example:**
```python
# Topic Agent MUST receive company_context
topic_agent.generate_topics(corpus, company_context, founder_feedback)

# Writer Agent MUST receive company_context + rules
writer_agent.draft_blog(topic, style, docs, company_context, founder_feedback)
```

### 2. Global Rules as Immutable Constraints

Don't treat rules as "nice to have." Treat them as hard constraints.

```python
# Wrong: Rules are suggestions
prompt += f"Prefer to follow these rules: {rules}"

# Right: Rules are immutable
prompt += f"You MUST strictly adhere to these non-negotiable global rules:\n{rules}"
```

### 3. Structured Output

Use JSON schemas for all LLM outputs. This ensures:
- Reliable parsing
- Type safety
- Easy validation

```python
schema = {
    "type": "object",
    "properties": {
        "topics": {"type": "array", "items": {...}}
    },
    "required": ["topics"]
}
result = generate_structured(prompt, schema)
```

### 4. Self-Improving Feedback Loop

Extract systemic rules from human feedback:

```
Human comment → Editor applies fix → Evaluator classifies
→ If systemic → Save to global_rules.json
→ All future blogs enforce rule automatically
```

### 5. Anti-Hallucination Pattern

When ambiguous, ask for clarification instead of guessing:

```python
# Wrong: Invent intent when unclear
rewritten = llm.rewrite(ambiguous_comment)  # Hallucination risk

# Right: Admit uncertainty
is_clear = llm.evaluate_clarity(comment, context)
if not is_clear:
    return {"is_clear": False, "rewritten": "", "reasoning": "Comment too vague"}
```

---

## Pipeline Flow

```
1. Setup (One-time)
   - Ingest Docs → ChromaDB embeddings
   - Style Profiler → extract_voice.json
   - Benchmark Agent → benchmark_insights.json

2. Weekly Cycle
   - Topic Agent → generate 3-5 topics
   - Writer Agent → draft blogs (with feedback loop)
   - Critic Agent → evaluate (score >= 7 to proceed)
   - Human Review → Notion comments
   - Editor Agent → apply micro-edits + extract rules
   - SEO Agent → extract metadata
   - Publisher → output variants

3. Feedback Loop
   - Human comments → Editor applies fixes
   - Systemic patterns → Saved as global rules
   - Next week: All agents enforce new rules
```

---

## Testing Your Implementation

### Unit Tests

Test each agent independently:

```python
# Test topic generation
topics = generate_topics(
    company_context=sample_context,
    existing_topics=[],
)
assert len(topics) >= 1
assert "title" in topics[0]
assert "angle" in topics[0]

# Test writing
draft = draft_blog(
    topic=sample_topic,
    style_profile=sample_style,
    ...
)
assert "# " in draft  # Has H1
assert "<!-- FOOTNOTE_START -->" in draft  # Has CTA tag

# Test criticism
evaluation = evaluate_blog(draft, ...)
assert "score" in evaluation
assert 1 <= evaluation["score"] <= 10
```

### Integration Tests

Test the full pipeline:

```python
# One-time setup
ingest_docs()
style_profile = profile_style()
benchmark = analyze_benchmarks()

# Weekly run
topics = generate_topics(company_context, founder_feedback)
for topic in topics:
    draft = draft_blog(topic, style_profile, ...)
    evaluation = evaluate_blog(draft, ...)
    
    if evaluation["score"] >= 7:
        # Ready for review
        save_to_notion(draft)
    else:
        # Revise
        feedback = evaluation["feedback"]
        draft = draft_blog(..., feedback=feedback)
```

---

## Common Implementation Decisions

### Which LLM Provider?

- **Claude (Recommended)**: Best structured output via tool_use
- **OpenAI**: GPT-4 works well, JSON mode available
- **Open source**: LLaMA, Mistral (higher latency, lower cost)

### Which Vector DB?

- **ChromaDB**: Simple, local, good for small corpus
- **Pinecone**: Managed, scales easily
- **Weaviate**: Open-source, production-ready
- **Milvus**: High-performance, self-hosted

### Scheduling

- **APScheduler**: Background jobs (weekly runs)
- **Cron**: Linux/Mac scheduling
- **GitHub Actions**: Cloud-based, event-triggered
- **Cloud Workflows**: GCP/AWS equivalent

### Human Review Layer

- **Notion**: Comments as structured data
- **Custom UI**: Build your own review interface
- **Email**: Simple but less structured
- **Slack**: Comment in Slack, sync to DB

---

## Troubleshooting

### Topic Agent generating misaligned topics

**Check:** Is `company_context` being passed to Topic Agent?

```python
# Wrong
topics = generate_topics(corpus)

# Right
topics = generate_topics(corpus, company_context, founder_feedback)
```

### Writer Agent ignoring global rules

**Check:** Are rules being passed AND prioritized?

```python
# Build prompt with rules FIRST, before other constraints
prompt = f"""MANDATORY RULES (NON-NEGOTIABLE):
{rules}

Topic: {topic}
Style: {style}
...
"""
```

### Critic Agent scores low even though draft looks good

**Check:** Are all 10 sub_scores present in evaluation?

Some dimensions (like `feedback_compliance`) weigh heavily if rules aren't met.

### Editor Agent hallucinating when comment is ambiguous

**Check:** Is `is_clear` evaluation working?

```python
# Should return is_clear=False for ambiguous comments
result = get_micro_edit(text, "check this", ...)
assert result["is_clear"] == False
assert result["rewritten_paragraph"] == ""
```

---

## Next Steps

1. **Fork this repo**
2. **Implement LLM wrapper** (utils/llm_template.py)
3. **Test with a single agent** (start with Topic Agent)
4. **Build out remaining agents**
5. **Create your own company_context.json** and founder_feedback.json
6. **Run the full weekly pipeline**
7. **Set up human review loop** (Notion, email, etc.)
8. **Monitor and iterate**

---

## Questions?

This is a framework, not a finished product. You'll need to:
- Choose your LLM provider
- Set up your vector DB
- Configure your review layer
- Customize prompts for your use case

**The architecture is battle-tested.** The implementation is yours to build.

Good luck! 🚀
