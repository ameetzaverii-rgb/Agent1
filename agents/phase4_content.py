"""
Phase 4 — Content Generation agents (parallel after Phase 3)
  1. ReadingMaterialAgent
  2. ExerciseDesignerAgent
  3. TeacherMaterialAgent
  4. StudentMaterialAgent
  5. BootcampChallengeAgent
  6. AITutorScriptAgent
"""

from typing import Any, Dict
from intake_schema import CourseBrief
from agents.base import run_agent


READING_SYSTEM = """You are a master educational content writer for Indian K-12 and higher
education. You write clear, engaging, culturally-relevant explanations, definitions, and
narrative text. You adapt vocabulary and examples to the learner's context.

Return JSON:
{
  "modules": [
    {
      "module_id": "...",
      "content_blocks": [
        {
          "lesson_id": "...",
          "type": "explanation|definition|example|analogy|summary",
          "text": "...",
          "word_count": 0,
          "reading_level": "..."
        }
      ]
    }
  ],
  "glossary": [{"term": "...", "definition": "..."}],
  "key_concepts_count": 0,
  "total_word_count": 0
}"""

async def ReadingMaterialAgent(brief: CourseBrief, pipeline_ctx: Dict[str, Any]) -> Dict[str, Any]:
    curriculum = pipeline_ctx.get("p3_curriculum", {})
    style = pipeline_ctx.get("p1_style", {})
    prompt = f"""Write the reading material for the first 2 modules of:

Course: {brief.title}
Subject: {brief.subject} — {brief.topic_focus}
Grade: {brief.grade_level}, Ages: {brief.target_age_min}–{brief.target_age_max}
Language: {brief.primary_language}
Tone: {style.get('brand_voice', brief.content_tone)}
Vocabulary level: {style.get('vocabulary_level', 'grade-appropriate')}

Curriculum (first 2 modules): {str(curriculum.get('course_map', []))[:2000]}

Write explanations, definitions, examples, and analogies using Indian cultural context."""
    return await run_agent("ReadingMaterialAgent", READING_SYSTEM, prompt, max_tokens=16000)


EXERCISE_SYSTEM = """You are an educational exercise and practice problem designer. You create
varied, scaffolded exercises aligned to Bloom's taxonomy levels: from recall to creation.
You write MCQs, fill-in-the-blanks, matching, short-answer, and project prompts.

Return JSON:
{
  "exercise_sets": [
    {
      "lesson_id": "...",
      "exercises": [
        {
          "id": "...",
          "type": "mcq|fill_blank|matching|short_answer|project|coding",
          "bloom_level": "remember|understand|apply|analyse|evaluate|create",
          "question": "...",
          "options": ["..."],
          "correct_answer": "...",
          "explanation": "...",
          "difficulty": "easy|medium|hard",
          "hint": "..."
        }
      ]
    }
  ],
  "total_exercises": 0
}"""

async def ExerciseDesignerAgent(brief: CourseBrief, pipeline_ctx: Dict[str, Any]) -> Dict[str, Any]:
    curriculum = pipeline_ctx.get("p3_curriculum", {})
    assessment = pipeline_ctx.get("p3_assessment", {})
    prompt = f"""Design exercises for the first 2 modules of:

Course: {brief.title}, Subject: {brief.subject}
Grade: {brief.grade_level}
Assessment style: {brief.assessment_style}
Question mix target: {assessment.get('question_type_mix', {})}

Include 5 exercises per lesson across varying Bloom's levels and difficulties."""
    return await run_agent("ExerciseDesignerAgent", EXERCISE_SYSTEM, prompt, max_tokens=12000)


TEACHER_SYSTEM = """You are an expert in teacher professional development and pedagogical guides.
You write detailed teacher manuals with lesson plans, discussion prompts, common misconceptions,
differentiation strategies, and formative assessment checkpoints.

Return JSON:
{
  "teacher_guide": {
    "overview": "...",
    "lesson_plans": [
      {
        "lesson_id": "...",
        "duration_min": 0,
        "learning_objectives": ["..."],
        "materials_needed": ["..."],
        "warm_up": "...",
        "main_activity": "...",
        "discussion_prompts": ["..."],
        "common_misconceptions": [{"misconception": "...", "correction": "..."}],
        "differentiation": {"struggling": "...", "advanced": "..."},
        "exit_ticket": "..."
      }
    ],
    "assessment_guidance": "...",
    "parent_communication_template": "..."
  }
}"""

async def TeacherMaterialAgent(brief: CourseBrief, pipeline_ctx: Dict[str, Any]) -> Dict[str, Any]:
    curriculum = pipeline_ctx.get("p3_curriculum", {})
    prompt = f"""Create the teacher guide for first 2 modules of:

Course: {brief.title}
Subject: {brief.subject}, Grade: {brief.grade_level}
Include teacher guide: {brief.include_teacher_guide}
Include parent guide: {brief.include_parent_guide}

Write detailed lesson plans, discussion prompts, misconceptions, and differentiation strategies."""
    return await run_agent("TeacherMaterialAgent", TEACHER_SYSTEM, prompt, max_tokens=12000)


STUDENT_SYSTEM = """You are a student-facing content designer. You create workbooks, study guides,
quick reference cards, and visual summaries that students actually use and enjoy.

Return JSON:
{
  "student_workbook": {
    "modules": [
      {
        "module_id": "...",
        "study_guide": "...",
        "key_formulas_or_rules": ["..."],
        "mnemonics": ["..."],
        "self_check_questions": ["..."],
        "project_prompts": ["..."],
        "further_reading": ["..."]
      }
    ]
  },
  "quick_reference_cards": [{"title": "...", "content": "..."}],
  "revision_checklist": ["..."]
}"""

async def StudentMaterialAgent(brief: CourseBrief, pipeline_ctx: Dict[str, Any]) -> Dict[str, Any]:
    reading = pipeline_ctx.get("p4_reading", {})
    prompt = f"""Create student-facing materials for first 2 modules of:

Course: {brief.title}, Subject: {brief.subject}
Grade: {brief.grade_level}
Language: {brief.primary_language}
Gamification: {brief.gamification_level}/5

Create workbook pages, study guides, mnemonics, and self-check questions."""
    return await run_agent("StudentMaterialAgent", STUDENT_SYSTEM, prompt, max_tokens=10000)


BOOTCAMP_SYSTEM = """You are a challenge and bootcamp designer for intensive learning programs.
You design multi-day challenges, hackathons, coding sprints, and competitive learning events
that build deep skills and community.

Return JSON:
{
  "bootcamp": {
    "title": "...",
    "duration_days": 0,
    "theme": "...",
    "daily_schedule": [
      {"day": 1, "theme": "...", "activities": ["..."], "challenge": "...", "deliverable": "..."}
    ],
    "judging_criteria": ["..."],
    "prizes_or_badges": ["..."],
    "community_component": "..."
  },
  "micro_challenges": [
    {"id": "...", "title": "...", "description": "...", "difficulty": "easy|medium|hard", "time_limit_min": 0}
  ]
}"""

async def BootcampChallengeAgent(brief: CourseBrief, pipeline_ctx: Dict[str, Any]) -> Dict[str, Any]:
    prompt = f"""Design a bootcamp and micro-challenges for:

Course: {brief.title}, Subject: {brief.subject}
Grade: {brief.grade_level}, Ages: {brief.target_age_min}–{brief.target_age_max}
Gamification: {brief.gamification_level}/5

Design a 3-day bootcamp and 10 micro-challenges of varying difficulty."""
    return await run_agent("BootcampChallengeAgent", BOOTCAMP_SYSTEM, prompt)


AI_TUTOR_SYSTEM = """You are an AI tutor dialogue designer. You write conversational scripts,
FAQ responses, Socratic dialogue flows, and hint sequences for AI tutoring bots that help
learners 24/7.

Return JSON:
{
  "tutor_persona": {"name": "...", "personality": "...", "greeting": "..."},
  "faq_scripts": [
    {"question": "...", "answer": "...", "follow_up_prompts": ["..."]}
  ],
  "socratic_dialogues": [
    {
      "topic": "...",
      "opening_question": "...",
      "dialogue_tree": [{"student_response_type": "...", "tutor_response": "...", "next_question": "..."}]
    }
  ],
  "hint_sequences": [
    {"problem_id": "...", "hints": ["level_1_hint", "level_2_hint", "level_3_hint"]}
  ],
  "encouragement_phrases": ["..."],
  "escalation_trigger": "..."
}"""

async def AITutorScriptAgent(brief: CourseBrief, pipeline_ctx: Dict[str, Any]) -> Dict[str, Any]:
    prompt = f"""Write AI tutor scripts for:

Course: {brief.title}, Subject: {brief.subject}
Grade: {brief.grade_level}
Language: {brief.primary_language}
Tone: {brief.content_tone}

Write 20 FAQ responses, 3 Socratic dialogue trees, and hint sequences for top 10 hard problems."""
    return await run_agent("AITutorScriptAgent", AI_TUTOR_SYSTEM, prompt, max_tokens=12000)


PHASE4_AGENTS = {
    "ReadingMaterialAgent":   ReadingMaterialAgent,
    "ExerciseDesignerAgent":  ExerciseDesignerAgent,
    "TeacherMaterialAgent":   TeacherMaterialAgent,
    "StudentMaterialAgent":   StudentMaterialAgent,
    "BootcampChallengeAgent": BootcampChallengeAgent,
    "AITutorScriptAgent":     AITutorScriptAgent,
}
