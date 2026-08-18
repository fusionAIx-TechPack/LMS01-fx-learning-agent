from pathlib import Path


repo_root = Path(__file__).resolve().parents[1]
skill = (repo_root / ".agents/skills/create-course/SKILL.md").read_text(encoding="utf-8")
research = (repo_root / ".agents/skills/create-course/references/source-research.md").read_text(
    encoding="utf-8"
)
template_path = repo_root / ".agents/skills/create-course/templates/source-candidates.md"


def require_all(document: str, values: tuple[str, ...], context: str) -> None:
    missing = [value for value in values if value not in document]
    assert not missing, f"{context} is missing: {', '.join(missing)}"


require_all(
    skill,
    (
        "Course Research Request",
        "public web",
        "name",
        "description",
        "topics",
        "audience",
        "level",
        "language",
        "intended learning outcome",
        "learning-time budget",
    ),
    "Course Research Request contract",
)

require_all(
    research,
    (
        "public web",
        "5–10",
        "topical fit",
        "credibility gate",
        "fewer than five",
        "coverage gaps",
        "sign-in required",
        "company licence",
    ),
    "Source Candidate shortlist behavior",
)

assert template_path.exists(), "Source Research Dossier template is missing"
template = template_path.read_text(encoding="utf-8")
require_all(
    template,
    (
        "# Source Research Dossier",
        "## Course Research Request",
        "## Source Candidates",
        "## Topic Coverage",
        "## Recommendation",
        "## Excluded Candidates",
        "## Course Requester Selection",
        "Provider item ID",
        "Current availability",
    ),
    "Source Research Dossier template",
)
require_all(
    skill + research,
    ("templates/source-candidates.md", "source-candidates-<assessment-date>.md"),
    "versioned Source Research Dossier workflow",
)

require_all(
    skill,
    (
        "update the dossier with that decision",
        "only the explicitly selected Sources",
        "Course Brief JSON",
    ),
    "human selection to Course Brief gate",
)

require_all(
    skill + research,
    (
        "en-US",
        "activity_duration_minutes",
        "Source duration",
        "activity duration",
    ),
    "English Source Activity duration contract",
)
