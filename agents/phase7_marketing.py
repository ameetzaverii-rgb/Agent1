"""
Phase 7 — Marketing agents (parallel after Phase 6)
  1. SchoolOutreachAgent
  2. SocialAdAgent
  3. EmailCampaignAgent
  4. AnalyticsSEOAgent
"""

from typing import Any, Dict
from intake_schema import CourseBrief
from agents.base import run_agent


SCHOOL_OUTREACH_SYSTEM = """You are a B2B school sales and outreach strategist for edtech.
You write proposal decks, pricing tiers for schools, outreach email sequences, and
partnership pitch scripts.

Return JSON:
{
  "school_pitch": {
    "subject_line": "...",
    "value_proposition": "...",
    "key_benefits": ["..."],
    "pilot_offer": "..."
  },
  "pricing_tiers": [
    {"tier": "...", "students": "...", "price_per_student_inr": 0, "includes": ["..."]}
  ],
  "outreach_sequence": [
    {"day": 0, "channel": "...", "message_summary": "..."}
  ],
  "target_school_profile": "...",
  "partnership_models": ["..."]
}"""

async def SchoolOutreachAgent(brief: CourseBrief, pipeline_ctx: Dict[str, Any]) -> Dict[str, Any]:
    pricing = pipeline_ctx.get("p1_pricing", {})
    portal = pipeline_ctx.get("p6_portal", {})
    prompt = f"""Design school outreach strategy for:

Course: {brief.title}
Subject: {brief.subject}, Grade: {brief.grade_level}
B2B school price: ₹{pricing.get('recommended_b2b_school_price_inr', 'TBD')}
Compliance boards: {', '.join(brief.compliance_boards)}
Listing subtitle: {portal.get('listing', {}).get('subtitle', '')}

Write pitch, pricing tiers, and 30-day outreach sequence."""
    return await run_agent("SchoolOutreachAgent", SCHOOL_OUTREACH_SYSTEM, prompt)


SOCIAL_AD_SYSTEM = """You are a performance marketing specialist for Indian edtech.
You write Meta (Facebook/Instagram) and Google Ads copy, targeting configurations,
and YouTube ad scripts.

Return JSON:
{
  "meta_ads": [
    {"format": "feed|story|reel", "headline": "...", "body": "...", "cta": "...", "targeting_notes": "..."}
  ],
  "google_ads": [
    {"type": "search|display|pmax", "headlines": ["..."], "descriptions": ["..."], "keywords": ["..."]}
  ],
  "youtube_ad": {
    "type": "skippable|bumper",
    "duration_sec": 0,
    "script": "...",
    "thumbnail_description": "..."
  },
  "budget_allocation": {"meta_percent": 0, "google_percent": 0, "youtube_percent": 0},
  "ab_test_variants": ["..."]
}"""

async def SocialAdAgent(brief: CourseBrief, pipeline_ctx: Dict[str, Any]) -> Dict[str, Any]:
    audience = pipeline_ctx.get("p1_audience", {})
    portal = pipeline_ctx.get("p6_portal", {})
    prompt = f"""Write paid social and search ad campaigns for:

Course: {brief.title}
Subject: {brief.subject}, Grade: {brief.grade_level}
Primary persona: {audience.get('primary_persona', {}).get('name', 'student/parent')}
Channels: {', '.join(brief.marketing_channels)}
USPs: {', '.join(brief.unique_selling_points)}
Price: ₹{brief.target_price_inr or 'TBD'}

Write 3 Meta ad variants, 2 Google ad groups, and 1 YouTube script."""
    return await run_agent("SocialAdAgent", SOCIAL_AD_SYSTEM, prompt)


EMAIL_SYSTEM = """You are an email marketing strategist for edtech. You design drip sequences,
launch campaigns, and WhatsApp broadcast scripts targeting parents, students, and teachers.

Return JSON:
{
  "welcome_sequence": [
    {"day": 0, "subject": "...", "preview": "...", "body_outline": "...", "cta": "..."}
  ],
  "launch_campaign": [
    {"email_num": 1, "subject": "...", "send_time": "...", "body_outline": "...", "segment": "..."}
  ],
  "whatsapp_broadcasts": [
    {"day": 0, "message": "...", "media": "..."}
  ],
  "re_engagement_sequence": [
    {"trigger": "...", "subject": "...", "body_outline": "..."}
  ],
  "estimated_open_rate": "...",
  "estimated_conversion_rate": "..."
}"""

async def EmailCampaignAgent(brief: CourseBrief, pipeline_ctx: Dict[str, Any]) -> Dict[str, Any]:
    audience = pipeline_ctx.get("p1_audience", {})
    prompt = f"""Design email and WhatsApp campaign for:

Course: {brief.title}
Subject: {brief.subject}, Grade: {brief.grade_level}
Target: parents and students ages {brief.target_age_min}–{brief.target_age_max}
Channels: {', '.join(brief.marketing_channels)}
Language: {brief.primary_language}

Write 5-email welcome sequence, 3-email launch campaign, and 3 WhatsApp broadcasts."""
    return await run_agent("EmailCampaignAgent", EMAIL_SYSTEM, prompt)


ANALYTICS_SEO_SYSTEM = """You are an analytics and SEO strategist for edtech platforms.
You design tracking plans, SEO content strategies, keyword maps, and performance dashboards.

Return JSON:
{
  "seo_keywords": [{"keyword": "...", "volume_estimate": "...", "intent": "..."}],
  "content_seo_plan": [{"content_type": "...", "topic": "...", "target_keyword": "..."}],
  "tracking_plan": {
    "events": [{"event_name": "...", "trigger": "...", "properties": {}}],
    "goals": ["..."],
    "dashboards": ["..."]
  },
  "performance_kpis": ["..."],
  "ab_test_roadmap": ["..."]
}"""

async def AnalyticsSEOAgent(brief: CourseBrief, pipeline_ctx: Dict[str, Any]) -> Dict[str, Any]:
    portal = pipeline_ctx.get("p6_portal", {})
    prompt = f"""Design analytics and SEO strategy for:

Course: {brief.title}
Subject: {brief.subject}, Grade: {brief.grade_level}
Portal keywords: {portal.get('seo_metadata', {}).get('keywords', [])}
Boards: {', '.join(brief.compliance_boards)}

Identify 20 target keywords, design tracking plan, and define KPI dashboard."""
    return await run_agent("AnalyticsSEOAgent", ANALYTICS_SEO_SYSTEM, prompt)


PHASE7_AGENTS = {
    "SchoolOutreachAgent":  SchoolOutreachAgent,
    "SocialAdAgent":        SocialAdAgent,
    "EmailCampaignAgent":   EmailCampaignAgent,
    "AnalyticsSEOAgent":    AnalyticsSEOAgent,
}
