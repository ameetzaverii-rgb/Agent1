"""
Intake schema for the Educational Content Multi-Agent System.
Defines the course brief that triggers the entire pipeline.
"""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date


class DeliveryFormat(str, Enum):
    OFFLINE_COURSE = "offline_course"
    HYBRID_PROGRAM = "hybrid_program"
    FULL_ONLINE = "full_online"
    SCORM_PACKAGE = "scorm_package"
    BOOTCAMP = "bootcamp"
    AI_TUTOR_BOT = "ai_tutor_bot"
    MARKETING_COLLATERAL = "marketing_collateral"


class ComplianceBoard(str, Enum):
    NEP_2020 = "NEP_2020"
    CBSE = "CBSE"
    NCF = "NCF"
    ICSE = "ICSE"
    IB = "IB"
    CAMBRIDGE = "Cambridge"
    STATE_BOARD = "State_Board"


class GradeLevel(str, Enum):
    PRE_PRIMARY = "Pre-Primary (3-5)"
    PRIMARY_1_5 = "Primary (1-5)"
    MIDDLE_6_8 = "Middle (6-8)"
    SECONDARY_9_10 = "Secondary (9-10)"
    SENIOR_SECONDARY_11_12 = "Senior Secondary (11-12)"
    UNDERGRADUATE = "Undergraduate"
    POSTGRADUATE = "Postgraduate"
    PROFESSIONAL = "Professional"


class Language(str, Enum):
    ENGLISH = "English"
    HINDI = "Hindi"
    TAMIL = "Tamil"
    TELUGU = "Telugu"
    KANNADA = "Kannada"
    MARATHI = "Marathi"
    BENGALI = "Bengali"
    GUJARATI = "Gujarati"
    BILINGUAL_EN_HI = "Bilingual_EN_HI"


class ContentTone(str, Enum):
    FORMAL_ACADEMIC = "formal_academic"
    CONVERSATIONAL = "conversational"
    STORYTELLING = "storytelling"
    SOCRATIC = "socratic"
    GAMIFIED = "gamified"


class AssessmentStyle(str, Enum):
    MCQ_HEAVY = "mcq_heavy"
    OPEN_ENDED = "open_ended"
    PROJECT_BASED = "project_based"
    COMPETENCY_BASED = "competency_based"
    MIXED = "mixed"


class CourseBrief(BaseModel):
    """Master intake form — this triggers the entire 21-agent pipeline."""

    # Identity
    brief_id: str = Field(..., description="Unique ID for this content request")
    title: str = Field(..., description="Working title of the course/module")
    subject: str = Field(..., description="Subject area (e.g. Mathematics, Science, Coding)")
    topic_focus: str = Field(..., description="Specific topic within subject")

    # Audience
    grade_level: GradeLevel
    target_age_min: int = Field(..., ge=3, le=25)
    target_age_max: int = Field(..., ge=3, le=25)
    learner_persona: str = Field(..., description="Brief description of target learner")
    prior_knowledge_assumed: str = Field(default="None", description="What learners already know")

    # Delivery & Format
    delivery_formats: List[DeliveryFormat] = Field(..., min_items=1)
    primary_language: Language = Language.ENGLISH
    secondary_languages: List[Language] = Field(default_factory=list)
    estimated_duration_hours: float = Field(..., gt=0, description="Total content hours")

    # Compliance & Standards
    compliance_boards: List[ComplianceBoard] = Field(..., min_items=1)
    accessibility_required: bool = Field(default=True, description="WCAG 2.1 AA compliance")
    scorm_version: str = Field(default="SCORM_2004_4th", description="SCORM or xAPI")

    # Pedagogical Preferences
    content_tone: ContentTone = ContentTone.CONVERSATIONAL
    assessment_style: AssessmentStyle = AssessmentStyle.MIXED
    include_teacher_guide: bool = True
    include_parent_guide: bool = False
    gamification_level: int = Field(default=2, ge=0, le=5, description="0=none, 5=full gamification")

    # Business & Marketing
    target_price_inr: Optional[float] = Field(None, description="Target retail price in INR")
    competitor_products: List[str] = Field(default_factory=list)
    unique_selling_points: List[str] = Field(default_factory=list, min_items=1)
    marketing_channels: List[str] = Field(default_factory=list)

    # Timeline
    deadline: Optional[date] = None
    priority: int = Field(default=2, ge=1, le=5, description="1=low, 5=urgent")

    # Additional context
    special_instructions: Optional[str] = None
    reference_materials: List[str] = Field(default_factory=list, description="URLs or file paths")

    class Config:
        use_enum_values = True


def sample_brief() -> CourseBrief:
    """Returns a sample brief for testing the pipeline."""
    return CourseBrief(
        brief_id="BRIEF-001",
        title="Python Programming for Class 9-10",
        subject="Computer Science",
        topic_focus="Python fundamentals: variables, loops, functions, file I/O",
        grade_level=GradeLevel.SECONDARY_9_10,
        target_age_min=14,
        target_age_max=16,
        learner_persona="Urban/semi-urban students in CBSE schools, basic computer literacy",
        prior_knowledge_assumed="Basic computer operations, Scratch or Logo programming",
        delivery_formats=[
            DeliveryFormat.FULL_ONLINE,
            DeliveryFormat.SCORM_PACKAGE,
            DeliveryFormat.AI_TUTOR_BOT,
            DeliveryFormat.OFFLINE_COURSE,
        ],
        primary_language=Language.ENGLISH,
        secondary_languages=[Language.HINDI],
        estimated_duration_hours=40.0,
        compliance_boards=[ComplianceBoard.CBSE, ComplianceBoard.NEP_2020, ComplianceBoard.NCF],
        accessibility_required=True,
        content_tone=ContentTone.CONVERSATIONAL,
        assessment_style=AssessmentStyle.PROJECT_BASED,
        include_teacher_guide=True,
        gamification_level=3,
        target_price_inr=2999.0,
        unique_selling_points=[
            "Real-world projects from Indian context",
            "Bilingual support (EN/HI)",
            "Aligned to CBSE Class 9-10 syllabus",
            "AI tutor available 24/7",
        ],
        marketing_channels=["WhatsApp", "YouTube", "School partnerships", "Google Ads"],
        priority=3,
    )


if __name__ == "__main__":
    brief = sample_brief()
    print(brief.model_dump_json(indent=2))
