"""
Entry point — run the full 21-agent educational content pipeline.

Usage:
    python main.py                    # runs with sample brief
    python main.py --dry-run          # skips all API calls, validates the DAG
    python main.py --brief path.json  # loads a custom CourseBrief JSON file
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path

from intake_schema import CourseBrief, sample_brief
from orchestrator import MasterOrchestrator
from agents import ALL_AGENTS


def load_brief(path: str) -> CourseBrief:
    data = json.loads(Path(path).read_text())
    return CourseBrief(**data)


async def main():
    parser = argparse.ArgumentParser(description="Educational Content Multi-Agent Pipeline")
    parser.add_argument("--dry-run", action="store_true", help="Skip API calls, validate DAG only")
    parser.add_argument("--brief", type=str, help="Path to CourseBrief JSON file")
    parser.add_argument("--output", type=str, default="pipeline_output.json", help="Output file")
    args = parser.parse_args()

    brief = load_brief(args.brief) if args.brief else sample_brief()

    print(f"\nLoaded brief: {brief.brief_id} — {brief.title}")
    print(f"Formats: {', '.join(brief.delivery_formats)}")
    print(f"Boards: {', '.join(brief.compliance_boards)}")
    print(f"Agents registered: {len(ALL_AGENTS)}")
    print(f"Dry run: {args.dry_run}\n")

    orchestrator = MasterOrchestrator(brief=brief, dry_run=args.dry_run)
    report = await orchestrator.run(agent_registry=ALL_AGENTS)

    Path(args.output).write_text(json.dumps(report, indent=2, default=str))
    print(f"\nPipeline {report['status']} — report written to {args.output}")

    if report["status"] == "COMPLETE":
        # Print deliverables summary
        print(f"\nDeliverables produced:")
        for key in report.get("deliverables", {}):
            print(f"  ✓ {key}")
    elif report["status"] == "GATE_FAILED":
        print(f"\nBlocked at gate: {report.get('failed_gate')}")
        sys.exit(1)
    elif report["status"] == "ABORTED":
        print(f"\nAborted: {report.get('reason')}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
