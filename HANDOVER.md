# Handover — EduForge Multi-Agent Content Development System

## Update (2026-07-20) — added a working single agent

Added `english_master_agent/`: a standalone, single-agent (not multi-agent)
English teacher, "Professor Lex". Unlike `content_agent_system.html` below,
this one is actually runnable, not just a diagram:

- `system_prompt.md` — the full teaching persona/instructions (conversational
  practice, grammar & writing feedback, curriculum/lesson generation, exam
  prep for IELTS/TOEFL/Cambridge), with CEFR-level calibration.
- `agent.py` — a CLI chat loop using the Anthropic Python SDK
  (`client.messages.stream`) that loads the system prompt and holds a
  running conversation.
- `requirements.txt`, `README.md` — setup/run instructions.

Run with `pip install -r english_master_agent/requirements.txt`,
`export ANTHROPIC_API_KEY=...`, `python english_master_agent/agent.py`.

Not yet done: no automated tests, no web UI, no persistence of conversation
history across sessions, no evaluation harness for teaching quality.

## Current state (as of 2026-07-10)

This repo contains a single deliverable: `content_agent_system.html`, a static,
self-contained architecture diagram (no build step, no dependencies) that
visualizes the intended design of a 26-agent content pipeline called
**EduForge**. It is a design artifact, not a running system — no agent code,
orchestration, or backend exists in this repo yet.

Last commit: `21ce415` — "Add multi-agent content development system visual
architecture" (2026-06-25).

## What the diagram documents

The page lays out agents in 7 sequential phases (color-coded, with a legend):

1. **Research & Market Strategy** — Market Intel Agent, Audience Profiler,
   Style & Design Strategist, Pricing & Format Agent
2. **Compliance & Standards Mapping** — NEP 2020 Mapper, CBSE / NCF Agent,
   SCORM / xAPI Compliance Agent, Accessibility Agent
3. **Pedagogy & Framework Design** — Curriculum Architect, Learning Science
   Agent, Assessment Framework Agent
4. **Content Generation** (parallel sub-agents) — Reading Material Agent,
   Exercise Designer, Teacher Material Agent, Student Material Agent,
   Challenges & Bootcamp Agent, AI Tutor Script Agent
5. **Format, Package & QA** — SCORM Packager, Multi-Format Renderer, QA &
   Review Agent, Visual Assets Agent
6. **Publish & Deploy** — Portal Publisher Agent, LMS Distribution Agent, AI
   Bot Deployer
7. **Marketing & Outreach** — School Outreach Agent, Social & Ad Agent, Email
   Campaign Agent, Analytics & SEO Agent

Each agent is rendered as a card (name + implied role); phases run left-to-right
top-to-bottom, with Phase 4 explicitly marked as parallelizable.

## Open questions / not yet decided

- No agent implementation, orchestration framework, or inter-agent
  communication protocol has been chosen or built.
- No data contracts (inputs/outputs) between phases are defined anywhere
  outside the visual.
- No repo structure exists yet for actual agent code (this is purely a
  planning/diagram repo so far).

## Suggested next steps

1. Decide on an orchestration approach (e.g. sequential handoff files,
   a shared state store, or a framework like the Claude Agent SDK) for
   turning the diagram into working agents.
2. Define per-agent input/output schemas, starting with Phase 1 → Phase 2
   handoff, since that's the first cross-phase boundary.
3. Stand up one vertical slice first (e.g. one agent per phase for a single
   content type) before building out all 26 agents.
4. Keep this file updated incrementally as work progresses, rather than
   regenerating it from scratch — append a dated entry per session instead
   of rewriting history, to avoid hitting context-window limits when asking
   an agent to produce a handover summary late in a long session.

## How to keep this doc from going stale

Update it in small increments right after finishing a chunk of work, in the
same session that did the work (context is available then). If starting a
new session to write/update this doc, feed it concrete artifacts (`git log`,
`git diff`, file tree) rather than asking it to reconstruct history from a
long prior conversation — that's what triggers the "context window full"
failure mode.
