import re
from datetime import date

from app.models.state import ResearchState


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9-]+", "-", value.lower()).strip("-")


def export_obsidian(state: ResearchState) -> dict[str, str]:
    report = state["report"]
    lines = [
        "---",
        f"title: {report['title']}",
        f"date: {date.today().isoformat()}",
        "tags:",
        f"  - research/{_slug(report['title'])}",
        "  - research",
        "---",
        "",
        f"# {report['title']}",
        "",
        "## Executive Summary",
        "",
        str(report["executive_summary"]),
        "",
        "## Key Findings",
        "",
    ]
    lines.extend(f"{index}. {finding}" for index, finding in enumerate(report["key_findings"], 1))
    lines.extend(["", "## Analysis", "", str(report["analysis"]), "", "## Advantages", ""])
    lines.extend(f"- {item}" for item in report["advantages"])
    lines.extend(["", "## Risks", ""])
    lines.extend(f"- {item}" for item in report["risks"])
    lines.extend(["", "## Conclusion", "", str(report["conclusion"]), "", "## Sources", ""])
    lines.extend(f"- [{source['title']}]({source['url']}) - {source['publisher']}" for source in report["sources"])
    return {"markdown": "\n".join(lines) + "\n"}
