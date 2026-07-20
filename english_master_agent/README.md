# Professor Lex — Master English Teaching Agent

A single agent (no multi-agent orchestration) that teaches English through
one continuous conversation. It moves fluidly between four modes based on
what you ask for:

1. **Conversational practice** — chat naturally, get gently corrected.
2. **Grammar & writing feedback** — paste a sentence, paragraph, or essay.
3. **Curriculum & lesson generation** — ask for a lesson plan, worksheet,
   or vocabulary list at a given CEFR level.
4. **Exam preparation** — IELTS, TOEFL, Cambridge (KET–CPE), scored against
   real rubrics.

The agent's full teaching behavior is defined in [`system_prompt.md`](./system_prompt.md).

## Setup

```bash
cd english_master_agent
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-...
```

## Run

```bash
python agent.py
```

Then just talk to it — e.g.:

- "Let's just chat about my weekend."
- "Can you check this paragraph for my IELTS essay?"
- "Give me a B1-level lesson plan on phrasal verbs for travel."
- "I have my Cambridge FCE speaking exam in two weeks, help me prepare."

Type `exit` or `quit` to end the session.

## Configuration

- `ANTHROPIC_API_KEY` (required) — your Anthropic API key.
- `ENGLISH_AGENT_MODEL` (optional) — override the model, defaults to
  `claude-sonnet-4-5`.

## Design notes

This is intentionally a single agent with one system prompt rather than a
multi-agent pipeline (contrast with `content_agent_system.html` elsewhere
in this repo, which is a 26-agent *content production* architecture for a
different purpose). A single well-specified teacher persona is simpler to
run, cheaper, and sufficient because all four teaching modes share the same
underlying skill (assessing a learner's English and responding at the right
level) — they don't need separate specialized agents or handoffs.
