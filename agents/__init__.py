# Specialist agent registry
from agents.phase1_research import PHASE1_AGENTS
from agents.phase2_compliance import PHASE2_AGENTS
from agents.phase3_pedagogy import PHASE3_AGENTS
from agents.phase4_content import PHASE4_AGENTS
from agents.phase5_packaging import PHASE5_AGENTS
from agents.phase6_publish import PHASE6_AGENTS
from agents.phase7_marketing import PHASE7_AGENTS

ALL_AGENTS = {
    **PHASE1_AGENTS,
    **PHASE2_AGENTS,
    **PHASE3_AGENTS,
    **PHASE4_AGENTS,
    **PHASE5_AGENTS,
    **PHASE6_AGENTS,
    **PHASE7_AGENTS,
}
