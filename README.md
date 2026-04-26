# AI-Powered Personalized Content Engine

A production-grade multi-agent system that generates ghostwritten, SEO-ready blog content at scale—with style consistency, fact alignment, and self-improving feedback loops.

**Built for a production fintech startup · Full implementation available for serious candidates**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-proprietary-red)](#)
[![Status](https://img.shields.io/badge/status-production-green)](#)

---

## Problem

Most ghostwriting solutions fall into two camps:
1. **Manual**: Sustainable but unscalable (a single writer bottleneck)
2. **Fully Automated**: Cheap but generic (no brand voice, no strategic angles)

What if you could have both? Scalable output **and** founder-authentic voice **and** strategic narrative control.

This system generates 8-12 long-form blog posts per week—each one:
- ✅ Matches the founder's writing voice and tone (style-matched ghostwriting)
- ✅ Addresses underexplored topic angles (topic discovery from content gaps)
- ✅ Aligns with business strategy (company values, target audience, CTAs)
- ✅ Gets better each cycle (human feedback → auto-edits → reusable rules)
- ✅ Ready for multiple channels (website markdown, newsletter variant, SEO metadata)

---

## How It Works: The Pipeline

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CONTENT GENERATION LOOP                      │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────┐
│ Ingest Docs  │  Read from Google Docs/Drive → chunk & embed
└──────┬───────┘
       ↓
┌──────────────────────┐
│ Style Profiler (1x)  │  Analyze corpus → extract tone, voice, patterns
└──────┬───────────────┘
       ↓
┌──────────────────────┐
│ Benchmark Analysis   │  Analyze 5-10 top articles → structure insights
└──────┬───────────────┘
       ↓
┌──────────────────────┐
│ WEEKLY CYCLE BEGINS  │
└──────┬───────────────┘
       ↓
┌──────────────────────┐
│ Topic Agent          │  Cluster embeddings → find underexplored angles
│ (Multi-Agent)        │  + benchmark personas + hooks
└──────┬───────────────┘
       ↓
┌──────────────────────┐
│ Writer Agent         │  Draft blog: topic + style + context + company rules
└──────┬───────────────┘
       ↓
┌──────────────────────┐
│ Critic Agent         │  Score (1-10 on 10 dimensions) + revision feedback
└──────┬───────────────┘
       ↓
┌──────────────────────┐
│ Human Review         │  Notion → reviewer leaves block-level comments
│ (Editor on Deck)     │
└──────┬───────────────┘
       ↓
┌──────────────────────┐
│ Editor Agent         │  Apply micro-edits + extract reusable rules
└──────┬───────────────┘
       ↓
┌──────────────────────┐
│ SEO Agent            │  Extract WordPress metadata (H1, meta desc, etc.)
└──────┬───────────────┘
       ↓
┌──────────────────────┐
│ Publisher            │  Output variants (website, newsletter)
└──────────────────────┘
```

### Core Agents

**Ingestion Agent**
- Fetches Google Docs/Drive, chunks text intelligently
- Upserts embeddings to ChromaDB (persistent, reusable)
- Avoids reprocessing on future runs

**Style Profiler**
- One-time run: analyzes all prior posts
- Extracts: tone, sentence length, opening patterns, vocabulary tendencies
- Saved as `style_profile.json` for reuse by Writer Agent

**Benchmark Agent**
- Analyzes 5-10 external top-performing articles in the space
- Extracts: headline hooks, outline structure, pacing, engagement tactics
- Creates `benchmark_insights.json`

**Topic Agent** (Cluster + Generate)
- Uses K-means clustering on embeddings to find content theme groups
- Generates 3-5 underexplored angles per cluster
- **Key innovation**: Also generates target "benchmark persona" for each topic (e.g., specific investors or operators to model writing toward)
- Returns: `{title, angle, outline[], target_benchmark_persona}`

**Writer Agent** (Multi-Input)
- Reads topic + style profile + company context + founder global rules
- Generates long-form draft (800-2000 words, markdown)
- **Context sources**: 
  - Topic structure (from Topic Agent)
  - Writing voice (from Style Profiler)
  - Business guardrails (from `company_context.json`)
  - Author preferences (from `founder_feedback.json`)

**Critic Agent** (10-Dimension Scorer)
- Evaluates draft across: style match, depth, hook strength, genericness, outline adherence, structure, CTA effectiveness, SEO structure, company alignment, rule compliance
- Returns: numeric score (1-10) per dimension + overall score + actionable feedback
- Also suggests new global rules if recurring issues detected

**Editor Agent** (Micro-Edit + Rule Extraction)
- Reads Notion reviewer comments (block-level)
- Applies surgical edits (rewrite only the paragraph, not the whole article)
- **Smart context handling**: If comment is vague (e.g., "check"), reads chronological comment chain to infer intent
- **Non-hallucination**: If it can't confidently determine intent, marks as ambiguous and asks for clarification instead of guessing
- Evaluates each comment: "Is this a one-off fix or a systemic rule?" → promotes systemic rules to global rules file

**SEO Agent**
- Extracts WordPress-ready metadata: H1, meta description, internal link anchors, alt text
- Generates from approved draft

**Publisher**
- Outputs multiple variants:
  - Website markdown (with inline CTAs per strategy)
  - Newsletter variant (with footnote CTAs)
- Stages in Notion for final review

---

## Why This Architecture?

### Why Multi-Agent Over Single LLM Prompt?

**Single Prompt Problems:**
- 10KB+ prompts become unwieldy and conflict-prone
- Different tasks have different requirements (topic generation ≠ copyediting)
- Debugging failures is a black box (which part of the mega-prompt failed?)
- Reusing components is hard

**Multi-Agent Solution:**
- Each agent is a **single responsibility**: Topic Agent finds angles, Writer drafts, Critic scores
- Failures are isolated and debuggable (we know exactly which agent needs tuning)
- Context is explicit and versioned (we can trace what went wrong)
- Agents can be swapped (improve Writer without retraining Topic Agent)
- Asynchronous improvement: upgrade one agent, the others keep working

### Why ChromaDB for Context Retrieval?

We tested three approaches:

| Approach | Pros | Cons |
|---|---|---|
| **In-memory embeddings** | Fast | Lose embeddings on restart; recompute each run |
| **Re-embed each run** | Always fresh | 2-5 min latency; burns API tokens |
| **ChromaDB (chosen)** | Fast local retrieval; persistent; zero recompute; queryable | Requires vector DB |

**Decision**: ChromaDB wins for production. Embeddings cost pennies but latency matters for weekly runs. Persistence is non-negotiable for scaling.

### Why Notion as the Review Layer?

The team already lives in Notion. We could have built a custom review UI, but:
- Editors already comment on Notion pages
- Block-level comments are structured data (not free-text Slack)
- Notion API is stable and fast
- No new tool to learn = higher adoption

---

## The Case Study: The Agent Context Misalignment Problem

### The Problem We Hit

After the first month of automated generation, human reviewers noticed something odd: **the blog posts were consistently targeting the wrong audience cohort**.

The system generates content for a niche, high-net-worth segment. But the generated topics kept drifting toward mass-market angles. The feedback loop—which should have corrected this—was useless. We'd ask the Critic Agent to flag audience misalignment, but the edits went into a void.

**Example**: A topic generated was "Crypto investment tips for young traders" when the target audience is wealth-preservation-focused family office managers. The Critic Agent scored it low. But when the Writer Agent drafted content, it just pivoted the narrative to fit the crypto-focused topic anyway. The feedback didn't stick.

### Why It Failed: The Prompt Conflict

Here's what we were doing:
- **Topic Agent**: ❌ **No company context** → Generated topics freely
- **Writer Agent**: ✅ Had company context + global rules, **BUT** prioritized topic input (made sense—the topic is authoritative, right?)
- **Critic Agent**: ✅ Had company context + benchmarks, but was evaluating a draft built on the wrong topic

The invisible assumption: *"Topic Agent is responsible for topic generation. Writing Agent is responsible for tone. Critic is responsible for quality. Each agent has its lane."*

But the Topic Agent's "lane" leaked into audience selection. And the Writer Agent's priority order (topic input > company context) made sense locally but broke globally.

### Root Cause: Hidden Assumptions

We assumed Topic Agent would only generate **neutral topic titles/outlines**. We were wrong.

The Topic Agent was generating:
- Topic titles ✅ (right)
- Angles ✅ (right) 
- **Implicit cohort/persona** (wrong—we didn't pass company context, so it guessed)

One agent's assumption became another agent's ground truth. The system propagated wrong premises through the pipeline.

### The Fix

**Single solution: Propagate company context + global rules to ALL agents.**

Not optional context. Not buried in a section. **Immutable constraints** that every agent respects:

```python
# Before:
topic_agent.generate_topics(corpus)  # ❌ No rules

# After:
topic_agent.generate_topics(corpus, company_context, global_rules)
writer_agent.draft(topic, style, company_context, global_rules)  # context is now immutable
critic_agent.evaluate(draft, company_context, global_rules)      # treats rules as constraints, not suggestions
```

And we changed the Writer Agent's priority:
```
Priority order:
1. Company global rules (immutable)
2. Topic structure (outline, angle)
3. Style profile (tone)
4. Benchmark insights (pacing)
```

Global rules are no longer "nice to have." They're hard constraints, checked first.

### Proof It Works

**Metric**: The feedback loop went from "mostly ignored" to "precise and targeted."

The clearest evidence: the Editor Agent logs show precise, context-aware edits. Here are anonymized examples illustrating the capabilities:

#### Example 1: Narrative Enhancement (Understanding Intent)

**Reviewer Comment:**
> "Add a specific failure mode - situation where the main risk materializes and creates compounding problems for the user"

**System Reasoning:**
> "The reviewer wants to add a concrete consequence scenario. This is a clear, additive edit that strengthens the narrative by showing cascading effects."

**Before:**
> During a period of market volatility, the system encountered several simultaneous issues. A scheduled rebalance was skipped. A notification failed to send. The user spent considerable time reconciling account statements.

**After:**
> During a period of market volatility, the system encountered several simultaneous issues. A scheduled rebalance was skipped. A notification failed to send. When the user finally discovered the mismatch, they had missed the optimal window to adjust positions. The user spent considerable time reconciling account statements and realizing the opportunity cost.

**Why This Matters**: The system understood the multi-step consequence (rebalance missed → notification failed → delay in discovery → opportunity cost) and threaded it seamlessly into existing narrative without hallucinating details.

---

#### Example 2: Pattern Recognition (Vague Comment + Context Chain)

**Reviewer Comments (chronological):**
1. Comment 1: "The definition changed from 'segment X' to 'segment Y' here. Should be consistent throughout as 'segment X'"
2. Comment 3: "Keep consistent" (vague, appearing on a different paragraph)

**System Reasoning** (for Comment 3):
> "Comment 1 explicitly flags that 'segment X' is the correct standard term. Comment 3 ('Keep consistent') appears on a paragraph that also uses 'segment Y'. The intent is clearly to apply the same terminology fix."

**Before:**
> The segment Y customer base represents a specific market opportunity that requires dedicated solutions.

**After:**
> The segment X customer base represents a specific market opportunity that requires dedicated solutions.

**Why This Matters**: A two-word vague comment could have caused hallucination. Instead, the system traced the chronological context, found the pattern, and applied the correct fix. It's transparent about its reasoning—no magic.

---

#### Example 3: Explicit Rule Extraction (One-Off → Systemic Rule)

**Reviewer Comment:**
> "Can we reference case studies from companies I've worked with? Include: how Company A solved integration challenges, how Company B unified their product ecosystem, how Company C improved customer retention through platform design"

**System Classification:**
> "This is not a one-off narrative edit. The reviewer is establishing a standing preference for which reference cases should be used across articles."

**Extracted Rule (Systemic):**
> "When providing case study examples, prefer drawing from these specific companies: Company A (integration challenges), Company B (product ecosystem unification), Company C (retention through design). These are founder-vetted examples."

**Applied to Next Blog:**
> Generic case study example → Company A's integration approach is a perfect model for...
> Third-party reference → Company B's unified product strategy shows...
> Hypothetical scenario → Company C's approach to retention demonstrates...

**Systemic Impact**: This rule is now saved to `global_rules.json`. Every future blog will prefer these founder-vetted references. The system learned and improved without needing to be told again.

---

## Key Features

✅ **Style-Matched Ghostwriting**
- Extracts voice profile from past corpus (tone, sentence length, opening patterns, vocabulary)
- Writer Agent enforces these patterns in every draft

✅ **Automated Topic Discovery**
- Clusters content embeddings to find theme groups
- Generates 3-5 underexplored angles per cluster
- Assigns benchmark personas to target writing

✅ **Self-Improving Feedback Loop**
- Human review → automated micro-edits → rule extraction
- One-off fixes stay one-off; systemic patterns become reusable rules
- No regression (rules are versioned)

✅ **Anti-Hallucination in Editing**
- If a reviewer comment is ambiguous, the system asks for clarification
- Doesn't make up intent; marks as "needs human judgment"
- Transparent reasoning for every edit

✅ **Scheduled Execution**
- APScheduler: runs pipeline weekly on Sunday 10 AM
- Manual trigger also available (`--run` flag)
- Logs all operations for debugging

✅ **Multi-Channel Output**
- Website markdown with inline CTAs
- Newsletter/Substack variant with footnote CTAs
- SEO metadata (H1, meta description, internal link anchors)

---

## Tech Stack

| Component | Tool | Why |
|---|---|---|
| **LLM** | Anthropic Claude (haiku-4-5) | Fast, cost-effective, excellent structured output |
| **Embeddings & Clustering** | scikit-learn + numpy | Fast local clustering; no API dependency |
| **Vector DB** | ChromaDB | Persistent embeddings; fast local retrieval |
| **Scheduling** | APScheduler | Lightweight; background scheduling |
| **Content Source** | Google Drive / Docs API | Team already uses Docs; structured collaboration |
| **Review Layer** | Notion API | Team already lives in Notion; structured comments |
| **PDF Parsing** | pypdf | Extract text from research PDFs |
| **Data Validation** | Pydantic | Type safety for agent inputs/outputs |
| **Package Mgmt** | uv | Fast, deterministic Python environment |

---

## Project Structure

```
personalized-content-writer/
├── main.py                          # Entry point: CLI for --run, --schedule, --profile-style
├── pipeline.py                      # Main weekly pipeline orchestration
├── apply_micro_edits.py             # Notion review loop: fetch comments → apply edits → extract rules
│
├── agents/
│   ├── __init__.py
│   ├── ingestion.py                 # Fetch Google Docs → chunk → embed → ChromaDB
│   ├── style_profiler.py            # Analyze corpus → extract voice profile
│   ├── benchmark.py                 # Analyze external top articles → insights
│   ├── topic_agent.py               # Cluster embeddings → generate angles + personas
│   ├── writer_agent.py              # Draft blog from topic + style + context + rules
│   ├── critic_agent.py              # Score draft on 10 dimensions + feedback
│   ├── editor_agent.py              # Micro-edit from comments + extract rules
│   └── seo_agent.py                 # Extract WordPress metadata
│
├── blog_agent/
│   ├── context/
│   │   ├── company_context.json     # Your positioning, target audience, values
│   │   └── founder_feedback.json    # Stylistic preferences + global rules
│   └── publisher.py                 # Notion staging → output publishing
│
├── utils/
│   ├── config.py                    # Paths, env vars, output directories
│   ├── llm.py                       # Anthropic API wrapper (structured generation)
│   ├── chroma_store.py              # ChromaDB interface (query, upsert)
│   ├── pdf_parser.py                # PDF → text extraction
│   ├── gdocs_parser.py              # Google Docs API interface
│   ├── notion_publisher.py          # Notion API: publish blogs
│   └── notion_editor.py             # Notion API: read comments, update blocks
│
├── outputs/                         # Generated blogs + metadata
│   ├── style_profile.json           # Voice profile (one-time output)
│   ├── benchmark_insights.json      # External article insights
│   ├── [topic]_website.md           # Generated blog (website variant)
│   ├── [topic]_substack.md          # Generated blog (newsletter variant)
│   ├── [topic]_seo_metadata.json    # WordPress metadata
│   ├── micro_edits_log.md           # Audit trail of all auto-edits applied
│   └── *_proposed_rules.json        # Extracted systemic rules per run
│
├── pipeline_config.json             # CTA strategies per channel
├── .env.example                     # Required: ANTHROPIC_API_KEY, GOOGLE_DRIVE_FOLDER_ID
├── .python-version                  # Python version lock
├── pyproject.toml                   # Dependencies
└── README.md                        # This file
```

---

## Getting Started

### Prerequisites
- Python 3.11+
- `uv` package manager ([install](https://docs.astral.sh/uv/))
- Anthropic API key (get from [console.anthropic.com](https://console.anthropic.com))
- Google Drive folder with source Docs

### Installation

```bash
# Clone the repo
git clone <repo-url>
cd personalized-content-writer

# Install dependencies
uv sync

# Create .env file
cp .env.example .env

# Fill in required API keys
# ANTHROPIC_API_KEY=sk-ant-...
# GOOGLE_DRIVE_FOLDER_ID=<your-folder-id>
```

### Quick Start

**One-Time Setup: Profile Your Writing Style**
```bash
python main.py --profile-style
```
Reads all Docs in your Google Drive folder, extracts voice profile, saves to `outputs/style_profile.json`.

**Run Pipeline Once**
```bash
python main.py --run
```
Generates 1 topic, drafts, critiques, stages in Notion. Outputs go to `outputs/`.

**Start Weekly Automation**
```bash
python main.py --schedule
```
Runs every Sunday at 10 AM. Keep this process running (e.g., in a tmux session or systemd service).

**Process Reviewer Feedback & Apply Edits**
```bash
python apply_micro_edits.py
```
Fetches Notion comments, applies micro-edits, extracts rules, updates pages.

---

## Configuration

### `blog_agent/context/company_context.json`

Describes your target audience, positioning, and guardrails:

```json
{
  "company_name": "[FinApp]",
  "mission": "Empower a niche, high-net-worth segment to manage wealth holistically.",
  "target_audience": "Urban professionals with family net worth in a specific segment",
  "tone": "Authoritative, conversational, never patronizing",
  "topics_to_avoid": ["mass market investing", "crypto speculation"],
  "values": ["transparency", "long-term thinking", "family-centric"]
}
```

### `blog_agent/context/founder_feedback.json`

Stylistic preferences and reusable rules extracted from feedback:

```json
{
  "global_rules": [
    "Define target segment clearly at the start of articles",
    "When illustrating concepts, reference founder's personal product experiences",
    "Never use hypothetical examples; prefer real-world stories"
  ],
  "tone_preferences": {
    "sentence_length": "Mix of short 5-word and longer 20+ word sentences",
    "opening_patterns": "Start with a sharp observation or story, not a definition"
  }
}
```

### `pipeline_config.json`

CTA strategies per channel:

```json
{
  "cta_rules": {
    "website": {
      "inline_cta": true,
      "placement": "mid-blog only"
    },
    "substack": {
      "footnote_cta": true,
      "footnote_text": "Custom CTA here"
    }
  }
}
```

### Environment Variables

```bash
ANTHROPIC_API_KEY=sk-ant-...                      # Required: Claude API key
GOOGLE_DRIVE_FOLDER_ID=<folder-id>               # Required: Folder ID with your Docs
NOTION_DATABASE_ID=<database-id>                 # Required: Notion page to stage blogs
NOTION_API_KEY=<notion-api-key>                  # Required: Notion integration token
BENCHMARK_ARTICLES_URL=<url-to-csv>              # Optional: External articles to analyze
```

---

## How Feedback Works

### The Feedback Loop

1. **Pipeline runs** → generates blog, stages in Notion
2. **Human reviewer** opens Notion page, highlights paragraphs, leaves comments
3. **`apply_micro_edits.py` runs** → reads comments, applies targeted edits
4. **Editor Agent evaluates** → "Is this a one-off fix or a systemic rule?"
5. **Systemic rules** → saved to `founder_feedback.json` global rules
6. **Next pipeline run** → all agents use updated rules

### When the Editor Agent Asks for Clarification

If a comment is too vague (e.g., "check this" with no context, or "fix it" with no detail), the Editor Agent **will not hallucinate**. Instead, it:

1. Marks the comment as `is_clear: false`
2. Logs it to the micro_edits_log as "Needs human judgment"
3. Waits for the reviewer to clarify

This prevents garbage-in-garbage-out. The system admits uncertainty rather than inventing intent.

---

## System Design Highlights

### Structured Output from LLM

Every agent uses Pydantic schemas + Claude's structured output mode:

```python
TOPIC_SCHEMA = {
    "properties": {
        "title": {"type": "string"},
        "angle": {"type": "string"},
        "outline": {"type": "array", "items": {"type": "string"}},
        "target_benchmark_persona": {"type": "string"}
    }
}
# Claude returns JSON matching this schema—100% parseable
```

No regex parsing. No "extract the JSON from markdown." Guaranteed valid output.

### Embedding-Based Context Retrieval

Instead of hardcoding context:
- Every post is chunked and embedded
- Queries find semantically similar posts
- Writer Agent gets relevant excerpts for tone matching
- Scales with corpus size (more posts = better examples)

### Immutable Global Rules

Rules are **not suggestions**:
```python
# Hard constraint checked first
if any(rule violates draft for rule in global_rules):
    draft = apply_fix(draft, rule)
```

Prevents regression. New rules automatically enforced on future content.

---

## Monitoring & Debugging

### Logs

- `pipeline.py` logs to stdout (timestamps, agent completions)
- `apply_micro_edits.py` logs all comment processing
- Each agent logs its reasoning (useful for debugging)

### Audit Trails

- `outputs/micro_edits_log.md` → every edit, before/after, reasoning
- `outputs/*_proposed_rules.json` → rules extracted per run
- Notion page update history → tracking who changed what

### Common Issues

**"Topic Agent generated wrong cohort"**
- Check: Is `company_context` being passed to Topic Agent?
- Check: Are `global_rules` present and being enforced?

**"Critic Agent gave low score but Writer didn't change"**
- Writer Agent got feedback but the topic was off (Topic Agent bug)
- Solution: See "The Case Study" section above

**"Editor asked for clarification instead of editing"**
- This is correct behavior (anti-hallucination)
- Reviewer needs to clarify comment intent

---

## Roadmap

### Core Features
- [ ] Multi-model support (Claude 3.5 Sonnet for harder tasks)
- [ ] A/B testing framework (compare multiple generated topics per week)
- [ ] Style transfer (clone voice from competitor content)
- [ ] Automatic fact-checking (cross-reference claims with source docs)
- [ ] Analytics dashboard (track which topics drive engagement)

### Observability & Evals (In Progress)
- [ ] **Output Quality Evals**: Automated scoring of generated content across style adherence, fact consistency, audience alignment, outline compliance
- [ ] **Agent Performance Monitoring**: Track latency, token usage, and error rates per agent; identify bottlenecks
- [ ] **Feedback Loop Health Metrics**: Monitor clarity of reviewer comments, edit acceptance rate, rule promotion frequency
- [ ] **Fact Consistency Checks**: Cross-reference claims in generated content against source documents; flag inconsistencies
- [ ] **Style Adherence Scoring**: Quantify how well each draft matches the extracted style profile
- [ ] **Regression Detection**: Alert when new blogs score lower on historical metrics; prevent silent quality drift
- [ ] **Observability Dashboard**: Real-time view of pipeline health, agent performance, and content quality trends

---

## Acknowledgments

This system was built by iterating through real failures. The biggest learning: **distributed systems need shared constraints**. When agents don't have explicit company guardrails, they drift. When feedback loops don't propagate learning, they become useless. When editors don't ask for clarification, they hallucinate.

The architecture reflects these hard-won lessons.

---

## Contact

**Full proprietary implementation** (with real output examples, Notion integration, and active monitoring) **available for serious candidates interested in:**
- Multi-agent system design
- LLM product engineering
- Prompt engineering at scale
- Content automation + distribution

Email: [pkomals94@gmail.com](mailto:pkomals94@gmail.com)

---

**License**: Proprietary · **Status**: Production-active
