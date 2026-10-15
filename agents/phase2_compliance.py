"""
Phase 2 — Compliance Mapping agents (parallel)
  1. NEP2020MapperAgent
  2. CBSENCFAgent
  3. SCORMComplianceAgent
  4. AccessibilityAgent
"""

from typing import Any, Dict
from intake_schema import CourseBrief
from agents.base import run_agent


NEP2020_SYSTEM = """You are an expert in India's National Education Policy 2020 and its
implementation guidelines. You map educational content to NEP 2020 competencies, FLN goals,
multidisciplinary frameworks, and the spirit of holistic learning.

Return JSON:
{
  "nep_alignment_score": 0.0,
  "aligned_nep_goals": ["..."],
  "fln_components": ["..."],
  "multidisciplinary_links": ["..."],
  "life_skills_addressed": ["..."],
  "indianknowledge_system_hooks": ["..."],
  "gaps": ["..."],
  "recommendations": ["..."]
}"""

async def NEP2020MapperAgent(brief: CourseBrief, pipeline_ctx: Dict[str, Any]) -> Dict[str, Any]:
    prompt = f"""Map this course to NEP 2020 framework:

Subject: {brief.subject} — {brief.topic_focus}
Grade: {brief.grade_level}
Content tone: {brief.content_tone}
Assessment style: {brief.assessment_style}

Identify NEP 2020 goals, FLN components, and multidisciplinary links."""
    return await run_agent("NEP2020MapperAgent", NEP2020_SYSTEM, prompt, use_thinking=True)


CBSE_NCF_SYSTEM = """You are a curriculum expert specialising in CBSE, NCF (National Curriculum
Framework), NCERT patterns, and state board syllabi in India. You perform detailed topic-by-topic
cross-walks between proposed content and official syllabi.

Return JSON:
{
  "cbse_syllabus_coverage": {"topic": "covered|partial|missing"},
  "ncf_alignment": {"strand": "alignment_notes"},
  "ncert_chapter_mapping": ["..."],
  "learning_outcomes_mapped": ["..."],
  "syllabus_gaps": ["..."],
  "extra_topics_beyond_syllabus": ["..."],
  "board_exam_alignment_score": 0.0
}"""

async def CBSENCFAgent(brief: CourseBrief, pipeline_ctx: Dict[str, Any]) -> Dict[str, Any]:
    prompt = f"""Perform CBSE/NCF compliance mapping for:

Subject: {brief.subject}
Topic: {brief.topic_focus}
Grade: {brief.grade_level}
Boards: {', '.join(brief.compliance_boards)}

Map topics to CBSE syllabus, NCF strands, and NCERT chapters. Identify gaps."""
    return await run_agent("CBSENCFAgent", CBSE_NCF_SYSTEM, prompt, use_thinking=True)


SCORM_SYSTEM = """You are a technical eLearning standards expert specialising in SCORM 2004,
xAPI (Tin Can), IMS Common Cartridge, and LTI 1.3. You produce SCORM manifest structures,
xAPI statement templates, and LMS integration specifications.

Return JSON:
{
  "scorm_version": "...",
  "manifest_structure": {"item_id": {"title": "...", "type": "sco|asset"}},
  "xapi_verbs": ["..."],
  "completion_criteria": "...",
  "mastery_score": 0,
  "lms_targets": ["Moodle", "Canvas", "Schoology", "DIKSHA"],
  "lti_version": "...",
  "packaging_notes": ["..."],
  "file_structure": ["..."]
}"""

async def SCORMComplianceAgent(brief: CourseBrief, pipeline_ctx: Dict[str, Any]) -> Dict[str, Any]:
    prompt = f"""Design SCORM/xAPI compliance specification for:

Course: {brief.title}
Formats: {', '.join(brief.delivery_formats)}
Duration: {brief.estimated_duration_hours}h
SCORM version: {brief.scorm_version}
Assessment: {brief.assessment_style}

Design manifest structure, xAPI verbs, completion criteria, and LMS targets."""
    return await run_agent("SCORMComplianceAgent", SCORM_SYSTEM, prompt)


ACCESSIBILITY_SYSTEM = """You are a digital accessibility expert specialising in WCAG 2.1 AA
for educational content in multilingual Indian contexts. You audit content plans and produce
detailed accessibility requirement specifications.

Return JSON:
{
  "wcag_checklist": {"criterion": "requirement"},
  "alt_text_guidelines": "...",
  "color_contrast_requirements": "...",
  "keyboard_navigation_notes": "...",
  "screen_reader_notes": "...",
  "multilingual_accessibility": ["..."],
  "video_caption_requirement": true,
  "audio_description_requirement": true,
  "cognitive_load_guidelines": ["..."],
  "compliance_score_target": 0.0
}"""

async def AccessibilityAgent(brief: CourseBrief, pipeline_ctx: Dict[str, Any]) -> Dict[str, Any]:
    prompt = f"""Produce WCAG 2.1 AA accessibility specification for:

Course: {brief.title}
Languages: {brief.primary_language} + {', '.join(brief.secondary_languages) or 'none'}
Formats: {', '.join(brief.delivery_formats)}
Age group: {brief.target_age_min}–{brief.target_age_max}
Gamification: {brief.gamification_level}/5

Define complete accessibility requirements for all output formats."""
    return await run_agent("AccessibilityAgent", ACCESSIBILITY_SYSTEM, prompt)


PHASE2_AGENTS = {
    "NEP2020MapperAgent":    NEP2020MapperAgent,
    "CBSENCFAgent":          CBSENCFAgent,
    "SCORMComplianceAgent":  SCORMComplianceAgent,
    "AccessibilityAgent":    AccessibilityAgent,
}
