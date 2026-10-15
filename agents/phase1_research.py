"""
Phase 1 — Market Research agents (run in parallel)
  1. MarketIntelAgent
  2. AudienceProfilerAgent
  3. StyleStrategistAgent
  4. PricingAgent
"""

import json
from typing import Any, Dict
from intake_schema import CourseBrief
from agents.base import run_agent


# ── 1. Market Intelligence ─────────────────────────────────────────────────────

MARKET_INTEL_SYSTEM = """You are a Market Intelligence analyst specialising in the Indian K-12 and
edtech sector. You analyse trends, competition, and demand signals for educational products.

Always return valid JSON matching this schema:
{
  "market_size_estimate": "...",
  "key_competitors": [{"name": "...", "price": "...", "strengths": [...], "weaknesses": [...]}],
  "demand_signals": ["..."],
  "market_gaps": ["..."],
  "recommended_differentiation": ["..."],
  "regional_hotspots": ["..."],
  "growth_trend": "rising|stable|declining",
  "confidence": 0.0
}"""

async def MarketIntelAgent(brief: CourseBrief, pipeline_ctx: Dict[str, Any]) -> Dict[str, Any]:
    prompt = f"""Analyse market opportunity for this course:

Subject: {brief.subject} — {brief.topic_focus}
Grade: {brief.grade_level}
Boards: {', '.join(brief.compliance_boards)}
Formats: {', '.join(brief.delivery_formats)}
Competitor products mentioned: {', '.join(brief.competitor_products) or 'None specified'}

Provide a thorough market intelligence report."""

    return await run_agent("MarketIntelAgent", MARKET_INTEL_SYSTEM, prompt, use_thinking=True)


# ── 2. Audience Profiler ───────────────────────────────────────────────────────

AUDIENCE_PROFILER_SYSTEM = """You are an expert in learning psychology and audience segmentation
for Indian educational contexts. You build rich learner personas including motivation drivers,
pain points, digital access patterns, and language preferences.

Always return valid JSON matching this schema:
{
  "primary_persona": {
    "name": "...",
    "age_range": "...",
    "motivation": "...",
    "pain_points": ["..."],
    "device_access": "...",
    "internet_quality": "...",
    "language_comfort": "...",
    "learning_style": "...",
    "parent_involvement": "..."
  },
  "secondary_personas": [...],
  "accessibility_needs": ["..."],
  "recommended_scaffolding": ["..."],
  "engagement_hooks": ["..."]
}"""

async def AudienceProfilerAgent(brief: CourseBrief, pipeline_ctx: Dict[str, Any]) -> Dict[str, Any]:
    prompt = f"""Build a detailed learner persona for:

Subject: {brief.subject}
Grade: {brief.grade_level} (ages {brief.target_age_min}–{brief.target_age_max})
Languages: {brief.primary_language} + {', '.join(brief.secondary_languages) or 'none'}
Learner description: {brief.learner_persona}
Prior knowledge: {brief.prior_knowledge_assumed}
Gamification level desired: {brief.gamification_level}/5

Build primary and secondary personas with actionable design implications."""

    return await run_agent("AudienceProfilerAgent", AUDIENCE_PROFILER_SYSTEM, prompt)


# ── 3. Style Strategist ────────────────────────────────────────────────────────

STYLE_STRATEGIST_SYSTEM = """You are a content style and brand strategist for educational products.
You define the voice, tone, visual language, and interaction patterns that make content resonate
with the target audience. You understand Indian cultural contexts deeply.

Always return valid JSON matching this schema:
{
  "brand_voice": "...",
  "tone_guidelines": ["..."],
  "vocabulary_level": "...",
  "cultural_references": ["..."],
  "example_opening_sentence": "...",
  "example_explanation_style": "...",
  "forbidden_patterns": ["..."],
  "visual_style": "...",
  "icon_style": "...",
  "color_mood": "..."
}"""

async def StyleStrategistAgent(brief: CourseBrief, pipeline_ctx: Dict[str, Any]) -> Dict[str, Any]:
    prompt = f"""Define the content style strategy for:

Subject: {brief.subject} for grade {brief.grade_level}
Tone requested: {brief.content_tone}
Primary language: {brief.primary_language}
Gamification: {brief.gamification_level}/5
USPs: {', '.join(brief.unique_selling_points)}

Define voice, tone, vocabulary, cultural hooks, and visual style guidelines."""

    return await run_agent("StyleStrategistAgent", STYLE_STRATEGIST_SYSTEM, prompt)


# ── 4. Pricing Agent ───────────────────────────────────────────────────────────

PRICING_SYSTEM = """You are a pricing strategist for Indian edtech products. You analyse willingness
to pay, competitive benchmarks, bundle structures, and B2B school pricing models.

Always return valid JSON matching this schema:
{
  "recommended_b2c_price_inr": 0,
  "recommended_b2b_school_price_inr": 0,
  "freemium_free_tier": "...",
  "bundle_suggestions": ["..."],
  "payment_model": "one-time|subscription|freemium|institutional",
  "price_anchors": ["..."],
  "discount_strategy": "...",
  "revenue_forecast_12m_inr": 0,
  "rationale": "..."
}"""

async def PricingAgent(brief: CourseBrief, pipeline_ctx: Dict[str, Any]) -> Dict[str, Any]:
    prompt = f"""Recommend a pricing strategy for:

Course: {brief.title}
Subject: {brief.subject}, Grade: {brief.grade_level}
Delivery formats: {', '.join(brief.delivery_formats)}
Target price (input): ₹{brief.target_price_inr or 'Not specified'}
Marketing channels: {', '.join(brief.marketing_channels)}
Competitors: {', '.join(brief.competitor_products) or 'none specified'}

Recommend B2C price, B2B/school price, bundle options, and 12-month revenue forecast."""

    return await run_agent("PricingAgent", PRICING_SYSTEM, prompt)


# ── Registry ───────────────────────────────────────────────────────────────────

PHASE1_AGENTS = {
    "MarketIntelAgent":     MarketIntelAgent,
    "AudienceProfilerAgent": AudienceProfilerAgent,
    "StyleStrategistAgent": StyleStrategistAgent,
    "PricingAgent":         PricingAgent,
}
