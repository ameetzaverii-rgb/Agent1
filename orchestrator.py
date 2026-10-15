"""
Master Orchestrator — reads the intake brief, builds the task DAG,
executes quality gates, and drives all 21 specialist agents.
"""

import asyncio
import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

import anthropic

from intake_schema import CourseBrief


# ── Pipeline phases ────────────────────────────────────────────────────────────

class Phase(str, Enum):
    MARKET_RESEARCH = "phase_1_market_research"
    COMPLIANCE_MAPPING = "phase_2_compliance_mapping"
    PEDAGOGY_FRAMEWORK = "phase_3_pedagogy_framework"
    CONTENT_GENERATION = "phase_4_content_generation"
    FORMAT_PACKAGE = "phase_5_format_package"
    PUBLISH_DEPLOY = "phase_6_publish_deploy"
    MARKETING = "phase_7_marketing"


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"
    BLOCKED = "blocked"   # quality gate not passed


# ── Task graph node ────────────────────────────────────────────────────────────

@dataclass
class AgentTask:
    task_id: str
    agent_name: str
    phase: Phase
    depends_on: List[str] = field(default_factory=list)  # task_ids
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None

    def duration_seconds(self) -> Optional[float]:
        if self.started_at and self.finished_at:
            return (self.finished_at - self.started_at).total_seconds()
        return None


# ── Quality gate ───────────────────────────────────────────────────────────────

@dataclass
class QualityGate:
    gate_id: str
    after_phase: Phase
    checks: List[str]          # human-readable checks
    min_pass_score: float = 0.7
    passed: Optional[bool] = None
    score: Optional[float] = None
    notes: str = ""


# ── Master Orchestrator ────────────────────────────────────────────────────────

class MasterOrchestrator:
    """
    Drives the entire 7-phase educational content pipeline.
    Uses Claude claude-opus-4-8 with extended thinking for high-stakes decisions.
    """

    MODEL = "claude-opus-4-8"

    def __init__(self, brief: CourseBrief, dry_run: bool = False):
        self.brief = brief
        self.dry_run = dry_run
        self.client = anthropic.Anthropic()
        self.run_id = str(uuid.uuid4())[:8]
        self.tasks: Dict[str, AgentTask] = {}
        self.gates: Dict[str, QualityGate] = {}
        self.pipeline_output: Dict[str, Any] = {}
        self._build_task_graph()
        self._register_gates()

    # ── Task graph ─────────────────────────────────────────────────────────────

    def _build_task_graph(self):
        """Defines all 21 agent tasks and their dependency edges."""

        def t(task_id, agent, phase, deps=None):
            self.tasks[task_id] = AgentTask(
                task_id=task_id,
                agent_name=agent,
                phase=phase,
                depends_on=deps or [],
            )

        # Phase 1 — Market Research (parallel)
        t("p1_market",    "MarketIntelAgent",     Phase.MARKET_RESEARCH)
        t("p1_audience",  "AudienceProfilerAgent", Phase.MARKET_RESEARCH)
        t("p1_style",     "StyleStrategistAgent",  Phase.MARKET_RESEARCH)
        t("p1_pricing",   "PricingAgent",          Phase.MARKET_RESEARCH)

        # Phase 2 — Compliance (parallel, after phase 1)
        p1 = ["p1_market", "p1_audience", "p1_style", "p1_pricing"]
        t("p2_nep",       "NEP2020MapperAgent",    Phase.COMPLIANCE_MAPPING, p1)
        t("p2_cbse",      "CBSENCFAgent",          Phase.COMPLIANCE_MAPPING, p1)
        t("p2_scorm",     "SCORMComplianceAgent",  Phase.COMPLIANCE_MAPPING, p1)
        t("p2_access",    "AccessibilityAgent",    Phase.COMPLIANCE_MAPPING, p1)

        # Phase 3 — Pedagogy (after phase 2)
        p2 = ["p2_nep", "p2_cbse", "p2_scorm", "p2_access"]
        t("p3_curriculum","CurriculumArchitectAgent", Phase.PEDAGOGY_FRAMEWORK, p2)
        t("p3_learning",  "LearningScientistAgent",   Phase.PEDAGOGY_FRAMEWORK, p2)
        t("p3_assessment","AssessmentFrameworkAgent",  Phase.PEDAGOGY_FRAMEWORK, p2)

        # Phase 4 — Content Generation (parallel, after phase 3)
        p3 = ["p3_curriculum", "p3_learning", "p3_assessment"]
        t("p4_reading",   "ReadingMaterialAgent",  Phase.CONTENT_GENERATION, p3)
        t("p4_exercises", "ExerciseDesignerAgent", Phase.CONTENT_GENERATION, p3)
        t("p4_teacher",   "TeacherMaterialAgent",  Phase.CONTENT_GENERATION, p3)
        t("p4_student",   "StudentMaterialAgent",  Phase.CONTENT_GENERATION, p3)
        t("p4_bootcamp",  "BootcampChallengeAgent",Phase.CONTENT_GENERATION, p3)
        t("p4_tutor",     "AITutorScriptAgent",    Phase.CONTENT_GENERATION, p3)

        # Phase 5 — Format & Package (after all content)
        p4 = ["p4_reading","p4_exercises","p4_teacher","p4_student","p4_bootcamp","p4_tutor"]
        t("p5_scorm_pkg", "SCORMPackagerAgent",    Phase.FORMAT_PACKAGE, p4)
        t("p5_renderer",  "MultiFormatRendererAgent", Phase.FORMAT_PACKAGE, p4)
        t("p5_visual",    "VisualAssetsAgent",     Phase.FORMAT_PACKAGE, p4)
        t("p5_qa",        "QAReviewAgent",         Phase.FORMAT_PACKAGE, p4)

        # Phase 6 — Publish & Deploy (after packaging)
        p5 = ["p5_scorm_pkg", "p5_renderer", "p5_visual", "p5_qa"]
        t("p6_portal",    "PortalPublisherAgent",  Phase.PUBLISH_DEPLOY, p5)
        t("p6_lms",       "LMSDistributionAgent",  Phase.PUBLISH_DEPLOY, p5)
        t("p6_bot",       "AIBotDeployerAgent",    Phase.PUBLISH_DEPLOY, p5)

        # Phase 7 — Marketing (after publish)
        p6 = ["p6_portal", "p6_lms", "p6_bot"]
        t("p7_school",    "SchoolOutreachAgent",   Phase.MARKETING, p6)
        t("p7_social",    "SocialAdAgent",         Phase.MARKETING, p6)
        t("p7_email",     "EmailCampaignAgent",    Phase.MARKETING, p6)
        t("p7_analytics", "AnalyticsSEOAgent",     Phase.MARKETING, p6)

    def _register_gates(self):
        """Quality gates between phases."""
        gates_config = [
            ("gate_1", Phase.MARKET_RESEARCH, [
                "Market demand validated",
                "Audience persona defined",
                "Competitive positioning clear",
                "Pricing model justified",
            ]),
            ("gate_2", Phase.COMPLIANCE_MAPPING, [
                "NEP 2020 alignment documented",
                "CBSE/NCF syllabus cross-walk complete",
                "SCORM manifest valid",
                "WCAG 2.1 AA checklist signed off",
            ]),
            ("gate_3", Phase.PEDAGOGY_FRAMEWORK, [
                "Learning objectives in Bloom's taxonomy",
                "Curriculum map covers all topics",
                "Assessment rubrics defined",
            ]),
            ("gate_4", Phase.CONTENT_GENERATION, [
                "Reading material complete and reviewed",
                "Exercises cover all objectives",
                "AI tutor scripts cover top 50 FAQs",
            ]),
            ("gate_5", Phase.FORMAT_PACKAGE, [
                "SCORM package validates in SCORM Cloud",
                "PDF/EPUB render correctly",
                "QA score >= 85/100",
            ]),
            ("gate_6", Phase.PUBLISH_DEPLOY, [
                "Portal listing live",
                "LMS import successful",
                "AI bot responds correctly",
            ]),
        ]
        for gate_id, phase, checks in gates_config:
            self.gates[gate_id] = QualityGate(gate_id=gate_id, after_phase=phase, checks=checks)

    # ── Orchestrator thinking ──────────────────────────────────────────────────

    def _think_about_brief(self) -> Dict[str, Any]:
        """
        Uses Claude with extended thinking to analyse the brief and
        return a strategic execution plan before any agents run.
        """
        print(f"[Orchestrator] Analysing brief with extended thinking...")

        prompt = f"""You are the Master Orchestrator of a 21-agent educational content pipeline.

Analyse this course brief and produce a structured execution plan:

{json.dumps(self.brief.model_dump(), indent=2, default=str)}

Return a JSON object with:
{{
  "risk_flags": ["..."],          // things that could block the pipeline
  "phase_priorities": {{"phase": "rationale"}},
  "content_strategy": "...",      // 2-3 sentences
  "compliance_notes": "...",
  "recommended_tone": "...",
  "estimated_tokens": 0,          // rough total token budget
  "go_no_go": "GO" | "NO_GO",
  "go_no_go_reason": "..."
}}"""

        if self.dry_run:
            return {
                "risk_flags": ["dry_run_mode"],
                "go_no_go": "GO",
                "go_no_go_reason": "Dry run — skipping actual API call",
                "content_strategy": "Dry run strategy",
                "compliance_notes": "",
                "recommended_tone": self.brief.content_tone,
                "estimated_tokens": 0,
            }

        response = self.client.messages.create(
            model=self.MODEL,
            max_tokens=16000,
            thinking={"type": "enabled", "budget_tokens": 10000},
            messages=[{"role": "user", "content": prompt}],
        )

        # Extract text block
        text = next(b.text for b in response.content if b.type == "text")
        # Strip markdown fences if present
        text = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        return json.loads(text)

    # ── Gate evaluation ────────────────────────────────────────────────────────

    def _evaluate_gate(self, gate: QualityGate, phase_results: Dict[str, Any]) -> bool:
        """Asks Claude to score the phase outputs against the gate checks."""
        if self.dry_run:
            gate.passed = True
            gate.score = 1.0
            gate.notes = "Dry run auto-pass"
            return True

        prompt = f"""Quality gate evaluation for {gate.after_phase}.

Gate checks:
{json.dumps(gate.checks, indent=2)}

Phase outputs summary:
{json.dumps(phase_results, indent=2, default=str)[:4000]}

Score each check 0.0–1.0. Return JSON:
{{"scores": {{}}, "overall": 0.0, "pass": true, "notes": "..."}}"""

        response = self.client.messages.create(
            model=self.MODEL,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.content[0].text.strip()
        text = text.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        result = json.loads(text)
        gate.score = result["overall"]
        gate.passed = result["pass"] and gate.score >= gate.min_pass_score
        gate.notes = result.get("notes", "")
        return gate.passed

    # ── Task runner ────────────────────────────────────────────────────────────

    async def _run_task(self, task: AgentTask, agent_fn: Callable) -> None:
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        print(f"  [→] {task.agent_name} starting...")
        try:
            task.result = await agent_fn(self.brief, self.pipeline_output)
            task.status = TaskStatus.DONE
            self.pipeline_output[task.task_id] = task.result
            print(f"  [✓] {task.agent_name} done ({task.duration_seconds():.1f}s)")
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            print(f"  [✗] {task.agent_name} FAILED: {e}")
        finally:
            task.finished_at = datetime.utcnow()

    def _get_phase_tasks(self, phase: Phase) -> List[AgentTask]:
        return [t for t in self.tasks.values() if t.phase == phase]

    def _collect_phase_results(self, phase: Phase) -> Dict[str, Any]:
        return {
            t.task_id: t.result
            for t in self._get_phase_tasks(phase)
            if t.result is not None
        }

    # ── Main pipeline ──────────────────────────────────────────────────────────

    async def run(self, agent_registry: Dict[str, Callable]) -> Dict[str, Any]:
        """
        Execute all 7 phases in sequence, with parallel tasks within each phase.
        Returns the final pipeline report.
        """
        print(f"\n{'='*60}")
        print(f"MASTER ORCHESTRATOR — Run {self.run_id}")
        print(f"Brief: {self.brief.brief_id} | {self.brief.title}")
        print(f"{'='*60}\n")

        # Pre-flight: analyse brief
        plan = self._think_about_brief()
        if plan.get("go_no_go") == "NO_GO":
            return {"status": "ABORTED", "reason": plan.get("go_no_go_reason"), "plan": plan}

        print(f"[Orchestrator] GO signal received. Strategy: {plan.get('content_strategy','')}\n")

        phase_order = [
            (Phase.MARKET_RESEARCH,    "gate_1"),
            (Phase.COMPLIANCE_MAPPING, "gate_2"),
            (Phase.PEDAGOGY_FRAMEWORK, "gate_3"),
            (Phase.CONTENT_GENERATION, "gate_4"),
            (Phase.FORMAT_PACKAGE,     "gate_5"),
            (Phase.PUBLISH_DEPLOY,     "gate_6"),
            (Phase.MARKETING,          None),
        ]

        for phase, gate_id in phase_order:
            print(f"\n[Phase] {phase.value}")
            tasks = self._get_phase_tasks(phase)

            # Run all tasks in this phase concurrently
            coros = []
            for task in tasks:
                fn = agent_registry.get(task.agent_name)
                if fn is None:
                    task.status = TaskStatus.BLOCKED
                    task.error = "Agent not registered"
                    print(f"  [!] {task.agent_name} — no agent registered, skipping")
                    continue
                coros.append(self._run_task(task, fn))

            await asyncio.gather(*coros)

            # Quality gate
            if gate_id:
                gate = self.gates[gate_id]
                phase_results = self._collect_phase_results(phase)
                print(f"\n[Gate] Evaluating {gate_id}...")
                passed = self._evaluate_gate(gate, phase_results)
                if not passed:
                    print(f"[Gate] FAILED — score {gate.score:.2f} < {gate.min_pass_score}")
                    print(f"       Notes: {gate.notes}")
                    return self._build_report(status="GATE_FAILED", failed_gate=gate_id)
                print(f"[Gate] PASSED — score {gate.score:.2f}")

        return self._build_report(status="COMPLETE")

    # ── Report ─────────────────────────────────────────────────────────────────

    def _build_report(self, status: str, failed_gate: Optional[str] = None) -> Dict[str, Any]:
        tasks_summary = {
            tid: {
                "agent": t.agent_name,
                "phase": t.phase,
                "status": t.status,
                "duration_s": t.duration_seconds(),
                "error": t.error,
            }
            for tid, t in self.tasks.items()
        }
        gates_summary = {
            gid: {"passed": g.passed, "score": g.score, "notes": g.notes}
            for gid, g in self.gates.items()
        }
        return {
            "run_id": self.run_id,
            "status": status,
            "failed_gate": failed_gate,
            "brief_id": self.brief.brief_id,
            "tasks": tasks_summary,
            "gates": gates_summary,
            "deliverables": self.pipeline_output,
        }
