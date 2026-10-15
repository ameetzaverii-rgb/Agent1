"""
Phase 6 — Publish & Deploy agents (parallel after Phase 5)
  1. PortalPublisherAgent
  2. LMSDistributionAgent
  3. AIBotDeployerAgent
"""

import json
from typing import Any, Dict
from intake_schema import CourseBrief
from agents.base import run_agent


PORTAL_SYSTEM = """You are a digital portal content manager for an educational platform.
You write course listing pages, SEO metadata, pricing configurations, and launch checklists.

Return JSON:
{
  "listing": {
    "title": "...",
    "subtitle": "...",
    "description_short": "...",
    "description_long": "...",
    "what_youll_learn": ["..."],
    "requirements": ["..."],
    "who_is_this_for": "...",
    "instructor_bio": "..."
  },
  "seo_metadata": {
    "meta_title": "...",
    "meta_description": "...",
    "keywords": ["..."],
    "og_image_description": "..."
  },
  "pricing_config": {
    "price_inr": 0,
    "discount_percent": 0,
    "free_preview_lessons": ["..."]
  },
  "launch_checklist": ["..."],
  "portal_api_payload": {}
}"""

async def PortalPublisherAgent(brief: CourseBrief, pipeline_ctx: Dict[str, Any]) -> Dict[str, Any]:
    pricing = pipeline_ctx.get("p1_pricing", {})
    prompt = f"""Write the portal listing and launch configuration for:

Course: {brief.title}
Subject: {brief.subject}, Grade: {brief.grade_level}
USPs: {', '.join(brief.unique_selling_points)}
Recommended price: ₹{pricing.get('recommended_b2c_price_inr', brief.target_price_inr)}
Languages: {brief.primary_language}

Write the full portal listing, SEO metadata, and pricing config."""
    return await run_agent("PortalPublisherAgent", PORTAL_SYSTEM, prompt)


LMS_SYSTEM = """You are an LMS integration specialist. You write LTI launch configurations,
SCORM upload instructions, Moodle/Canvas/Schoology/DIKSHA import procedures, and
API integration payloads for each platform.

Return JSON:
{
  "lms_integrations": [
    {
      "platform": "Moodle|Canvas|Schoology|DIKSHA|...",
      "method": "SCORM|LTI|API|IMS_CC",
      "steps": ["..."],
      "config": {},
      "test_checklist": ["..."]
    }
  ],
  "diksha_etb_metadata": {},
  "lti_consumer_key": "PLACEHOLDER",
  "notes": "..."
}"""

async def LMSDistributionAgent(brief: CourseBrief, pipeline_ctx: Dict[str, Any]) -> Dict[str, Any]:
    scorm = pipeline_ctx.get("p5_scorm_pkg", {})
    prompt = f"""Write LMS distribution plan for:

Course: {brief.title}
SCORM package: {json.dumps(scorm.get('sco_list', []))[:500]}
LMS targets: {scorm.get('lms_targets', ['Moodle', 'Canvas', 'DIKSHA'])}
Boards: {', '.join(brief.compliance_boards)}

Write integration steps, configs, and test checklists for each LMS platform."""
    return await run_agent("LMSDistributionAgent", LMS_SYSTEM, prompt)


BOT_DEPLOY_SYSTEM = """You are an AI chatbot deployment engineer. You write deployment
specifications for AI tutor bots across platforms: web widget, WhatsApp (via WATI/Twilio),
Telegram, and mobile app integration.

Return JSON:
{
  "bot_platforms": [
    {
      "platform": "web_widget|whatsapp|telegram|mobile_sdk",
      "deployment_method": "...",
      "webhook_url_placeholder": "...",
      "auth_config": {},
      "handoff_logic": "...",
      "deployment_steps": ["..."]
    }
  ],
  "bot_knowledge_base_size": "...",
  "fallback_to_human": true,
  "analytics_config": {},
  "monitoring_checklist": ["..."]
}"""

async def AIBotDeployerAgent(brief: CourseBrief, pipeline_ctx: Dict[str, Any]) -> Dict[str, Any]:
    tutor = pipeline_ctx.get("p4_tutor", {})
    prompt = f"""Design AI tutor bot deployment for:

Course: {brief.title}
Channels: {', '.join(brief.marketing_channels)}
Bot persona: {tutor.get('tutor_persona', {}).get('name', 'TutorBot')}
FAQ count: {len(tutor.get('faq_scripts', []))}
Language: {brief.primary_language}

Write deployment specs for web widget, WhatsApp, and Telegram."""
    return await run_agent("AIBotDeployerAgent", BOT_DEPLOY_SYSTEM, prompt)


PHASE6_AGENTS = {
    "PortalPublisherAgent":  PortalPublisherAgent,
    "LMSDistributionAgent":  LMSDistributionAgent,
    "AIBotDeployerAgent":    AIBotDeployerAgent,
}
