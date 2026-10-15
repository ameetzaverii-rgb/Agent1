"""
Phase 3 — Pedagogy & Framework agents (parallel after Phase 2)
  1. CurriculumArchitectAgent
  2. LearningScientistAgent
  3. AssessmentFrameworkAgent
"""

from typing import Any, Dict
from intake_schema import CourseBrief
from agents.base import run_agent


CURRICULUM_SYSTEM = """You are a senior Curriculum Architect with deep expertise in K-12 and
higher education curriculum design. You build detailed course maps: modules, units, lessons,
learning objectives, and content sequencing based on cognitive scaffolding principles.

Return JSON:
{
  "course_map": [
    {
      "module_id": "M1",
      "module_title": "...",
      "duration_hours": 0,
      "units": [
        {
          "unit_id": "M1U1",
          "title": "...",
          "lessons": [
            {"lesson_id": "M1U1L1", "title": "...", "duration_min": 0, "type": "concept|practice|project|assessment"}
          ]
        }
      ]
    }
  ],
  "total_modules": 0,
  "total_lessons": 0,
  "prerequisite_map": {"lesson_id": ["prerequisite_ids"]},
  "spiral_curriculum_notes": "..."
}"""

async def CurriculumArchitectAgent(brief: CourseBrief, pipeline_ctx: Dict[str, Any]) -> Dict[str, Any]:
    # Pull compliance outputs for reference
    cbse_data = pipeline_ctx.get("p2_cbse", {})
    nep_data = pipeline_ctx.get("p2_nep", {})

    prompt = f"""Design the complete curriculum map for:

Course: {brief.title}
Subject: {brief.subject} — {brief.topic_focus}
Grade: {brief.grade_level}
Duration: {brief.estimated_duration_hours} hours total
Assessment style: {brief.assessment_style}
Gamification: {brief.gamification_level}/5

CBSE topics to cover: {cbse_data.get('cbse_syllabus_coverage', 'see brief')}
NEP goals to embed: {nep_data.get('aligned_nep_goals', [])}

Build a complete module → unit → lesson map with timing and lesson types."""
    return await run_agent("CurriculumArchitectAgent", CURRICULUM_SYSTEM, prompt, use_thinking=True, max_tokens=12000)


LEARNING_SCIENCE_SYSTEM = """You are a Learning Scientist specialising in cognitive load theory,
spaced repetition, retrieval practice, and evidence-based instructional design. You prescribe
pedagogical techniques that maximise retention and transfer.

Return JSON:
{
  "pedagogical_model": "...",
  "bloom_taxonomy_distribution": {"remember": 0, "understand": 0, "apply": 0, "analyse": 0, "evaluate": 0, "create": 0},
  "spaced_repetition_schedule": "...",
  "retrieval_practice_strategy": "...",
  "worked_example_ratio": "...",
  "interleaving_plan": "...",
  "cognitive_load_guidelines": ["..."],
  "engagement_techniques": ["..."],
  "motivation_framework": "...",
  "feedback_design": "..."
}"""

async def LearningScientistAgent(brief: CourseBrief, pipeline_ctx: Dict[str, Any]) -> Dict[str, Any]:
    curriculum = pipeline_ctx.get("p3_curriculum", {})
    prompt = f"""Design the learning science framework for:

Course: {brief.title}, Grade: {brief.grade_level}
Assessment: {brief.assessment_style}
Tone: {brief.content_tone}
Gamification level: {brief.gamification_level}/5
Total lessons: {curriculum.get('total_lessons', 'TBD')}
Learner: {brief.learner_persona}

Prescribe pedagogical model, Bloom's distribution, spaced repetition, and engagement techniques."""
    return await run_agent("LearningScientistAgent", LEARNING_SCIENCE_SYSTEM, prompt)


ASSESSMENT_SYSTEM = """You are an Assessment Design expert specialising in competency-based
education, formative/summative assessment, and rubric design for Indian educational contexts.

Return JSON:
{
  "assessment_philosophy": "...",
  "formative_assessment_types": ["..."],
  "summative_assessment_types": ["..."],
  "question_type_mix": {"mcq": 0, "short_answer": 0, "project": 0, "oral": 0},
  "rubric_template": {"criterion": {"excellent": "...", "good": "...", "needs_work": "..."}},
  "passing_criteria": "...",
  "adaptive_assessment_notes": "...",
  "portfolio_requirements": "...",
  "anti_cheating_measures": ["..."],
  "certification_pathway": "..."
}"""

async def AssessmentFrameworkAgent(brief: CourseBrief, pipeline_ctx: Dict[str, Any]) -> Dict[str, Any]:
    learning = pipeline_ctx.get("p3_learning", {})
    prompt = f"""Design the assessment framework for:

Course: {brief.title}
Grade: {brief.grade_level}, Assessment style: {brief.assessment_style}
Bloom's distribution target: {learning.get('bloom_taxonomy_distribution', {})}
SCORM mastery score required: see compliance data
Board exam alignment needed: {', '.join(brief.compliance_boards)}

Design full assessment framework with question types, rubrics, and certification pathway."""
    return await run_agent("AssessmentFrameworkAgent", ASSESSMENT_SYSTEM, prompt)


PHASE3_AGENTS = {
    "CurriculumArchitectAgent":  CurriculumArchitectAgent,
    "LearningScientistAgent":    LearningScientistAgent,
    "AssessmentFrameworkAgent":  AssessmentFrameworkAgent,
}
