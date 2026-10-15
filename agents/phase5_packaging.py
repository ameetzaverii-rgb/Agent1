"""
Phase 5 — Format & Package agents (parallel after Phase 4)
  1. SCORMPackagerAgent
  2. MultiFormatRendererAgent
  3. VisualAssetsAgent
  4. QAReviewAgent
"""

import json
from typing import Any, Dict
from intake_schema import CourseBrief
from agents.base import run_agent


SCORM_PACKAGER_SYSTEM = """You are a SCORM packaging engineer. You generate imsmanifest.xml
structures, SCO (Sharable Content Object) definitions, xAPI statement blueprints, and
packaging instructions for SCORM 2004 4th edition and xAPI/Tin Can.

Return JSON:
{
  "imsmanifest_xml": "<!-- full XML string -->",
  "sco_list": [{"id": "...", "href": "...", "title": "..."}],
  "xapi_statements": [{"verb": "...", "object": "...", "result_schema": {}}],
  "zip_structure": ["folder/file paths"],
  "launch_url": "...",
  "completion_tracking": "...",
  "validation_checklist": ["..."]
}"""

async def SCORMPackagerAgent(brief: CourseBrief, pipeline_ctx: Dict[str, Any]) -> Dict[str, Any]:
    scorm_spec = pipeline_ctx.get("p2_scorm", {})
    curriculum = pipeline_ctx.get("p3_curriculum", {})
    prompt = f"""Generate SCORM package specification for:

Course: {brief.title}
SCORM version: {brief.scorm_version}
Modules/lessons: {json.dumps(curriculum.get('course_map', []))[:2000]}
SCORM spec from compliance: {json.dumps(scorm_spec)[:1000]}

Generate complete imsmanifest.xml, SCO list, xAPI statements, and zip file structure."""
    return await run_agent("SCORMPackagerAgent", SCORM_PACKAGER_SYSTEM, prompt, max_tokens=8000)


MULTI_FORMAT_SYSTEM = """You are a multi-format eLearning content renderer. You produce
specifications and templates for: PDF workbooks, EPUB ebooks, HTML5 interactive modules,
and offline printable materials. You define exact file formats, styling, and export parameters.

Return JSON:
{
  "pdf_spec": {"page_size": "...", "fonts": [...], "color_scheme": {...}, "template_notes": "..."},
  "epub_spec": {"epub_version": "...", "toc_structure": [...], "css_notes": "..."},
  "html5_spec": {"framework": "...", "interactivity_features": [...], "responsive": true},
  "print_spec": {"paper_size": "...", "bleed_mm": 0, "print_notes": "..."},
  "file_naming_convention": "...",
  "asset_manifest": ["..."]
}"""

async def MultiFormatRendererAgent(brief: CourseBrief, pipeline_ctx: Dict[str, Any]) -> Dict[str, Any]:
    prompt = f"""Design multi-format rendering specification for:

Course: {brief.title}
Delivery formats: {', '.join(brief.delivery_formats)}
Languages: {brief.primary_language} + {', '.join(brief.secondary_languages) or 'none'}
Accessibility: {brief.accessibility_required}

Define PDF, EPUB, HTML5, and print specifications with exact parameters."""
    return await run_agent("MultiFormatRendererAgent", MULTI_FORMAT_SYSTEM, prompt)


VISUAL_ASSETS_SYSTEM = """You are a visual design director for educational content. You define
illustration styles, icon sets, infographic templates, diagram types, and visual asset
requirements for educational materials.

Return JSON:
{
  "illustration_style": "...",
  "color_palette": {"primary": "...", "secondary": "...", "accent": "...", "background": "..."},
  "icon_set": "...",
  "diagram_types_needed": ["..."],
  "infographic_templates": ["..."],
  "character_design": {"style": "...", "diversity_notes": "..."},
  "asset_list": [{"id": "...", "type": "...", "description": "...", "placement": "..."}],
  "total_assets_required": 0
}"""

async def VisualAssetsAgent(brief: CourseBrief, pipeline_ctx: Dict[str, Any]) -> Dict[str, Any]:
    style = pipeline_ctx.get("p1_style", {})
    prompt = f"""Define visual asset requirements for:

Course: {brief.title}, Subject: {brief.subject}
Grade: {brief.grade_level}
Visual style from strategy: {style.get('visual_style', 'modern, clean')}
Color mood: {style.get('color_mood', 'energetic')}
Gamification: {brief.gamification_level}/5

Define illustration style, color palette, icon set, and list all required visual assets."""
    return await run_agent("VisualAssetsAgent", VISUAL_ASSETS_SYSTEM, prompt)


QA_REVIEW_SYSTEM = """You are a Quality Assurance Lead for educational content. You perform
comprehensive reviews across accuracy, pedagogy, compliance, accessibility, and production
quality. You produce a scored QA report.

Return JSON:
{
  "qa_score": 0,
  "dimension_scores": {
    "content_accuracy": 0,
    "pedagogical_soundness": 0,
    "compliance_alignment": 0,
    "accessibility": 0,
    "language_quality": 0,
    "production_quality": 0
  },
  "critical_issues": ["..."],
  "major_issues": ["..."],
  "minor_issues": ["..."],
  "passed": true,
  "recommendation": "approve|revise|reject"
}"""

async def QAReviewAgent(brief: CourseBrief, pipeline_ctx: Dict[str, Any]) -> Dict[str, Any]:
    # Summarise all phase 4 outputs for QA
    content_summary = {
        "reading_count": len(pipeline_ctx.get("p4_reading", {}).get("modules", [])),
        "exercise_count": pipeline_ctx.get("p4_reading", {}).get("total_word_count", 0),
        "has_teacher_guide": "p4_teacher" in pipeline_ctx,
        "has_student_guide": "p4_student" in pipeline_ctx,
        "has_ai_tutor": "p4_tutor" in pipeline_ctx,
        "compliance_boards": brief.compliance_boards,
    }
    prompt = f"""Perform QA review for:

Course: {brief.title}
Content summary: {json.dumps(content_summary)}
Compliance requirements: {', '.join(brief.compliance_boards)}
Accessibility required: {brief.accessibility_required}

Score across 6 dimensions (0–100) and provide detailed issues list."""
    return await run_agent("QAReviewAgent", QA_REVIEW_SYSTEM, prompt, use_thinking=True)


PHASE5_AGENTS = {
    "SCORMPackagerAgent":       SCORMPackagerAgent,
    "MultiFormatRendererAgent": MultiFormatRendererAgent,
    "VisualAssetsAgent":        VisualAssetsAgent,
    "QAReviewAgent":            QAReviewAgent,
}
