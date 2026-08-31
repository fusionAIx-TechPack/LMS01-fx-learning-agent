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


def require_none(document: str, values: tuple[str, ...], context: str) -> None:
    present = [value for value in values if value in document]
    assert not present, f"{context} must not contain: {', '.join(present)}"


require_all(
    skill,
    (
        "Course Research Request",
        "public web",
        "source URL",
        "Course Name",
        "Course Overview",
        "Course Duration",
        "Level",
        "Language",
        "Audience",
        "fundamental",
        "beginner",
        "intermediate",
        "advanced",
        "Would you like to continue creating the course for your Moodle?",
    ),
    "URL-based Course Research Request contract",
)

require_all(
    skill,
    (
        "Provide a source URL, a list of source URLs in an order, or attach an Excel file",
        "one course per URL",
        "build from input",
        "bin/course-urls",
        "single bulk confirmation",
        "its own `output/<course-slug>/`",
    ),
    "single URL, ordered list, or attached spreadsheet of URLs",
)

require_all(
    skill,
    (
        "stated completion",
        "Level using a typical average",
    ),
    "Course Duration derivation rule",
)

require_all(
    research,
    (
        "public web",
        "confirmed Course Research Request",
        "URL the Course Requester entered",
        "topical fit",
        "credibility gate",
        "Do not pad with weak Sources",
        "sign-in required",
        "company licence",
    ),
    "Source research behavior",
)

require_all(
    skill + research,
    (
        "Select the Sources and their order yourself",
        "no separate human selection step",
        "no human review of the staged",
    ),
    "agent Source selection replaces the human selection gate",
)

require_none(
    skill + template_path.read_text(encoding="utf-8"),
    (
        "explicitly selected Sources",
        "Course Requester explicitly chooses",
        "update the dossier with that decision",
    ),
    "removed human Source-selection gate",
)

assert template_path.exists(), "Source Research Dossier template is missing"
template = template_path.read_text(encoding="utf-8")
require_all(
    template,
    (
        "# Source Research Dossier",
        "## Course Research Request",
        "- URL:",
        "## Source Candidates",
        "## Topic Coverage",
        "## Excluded Candidates",
        "## Selected Sources",
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
        "dossier records the selected Sources",
        "Course Brief JSON",
        "dossier order",
    ),
    "Source selection to Course Brief gate",
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

require_all(
    skill,
    (
        "--accept --skip-restore",
        "automated review-learner HTTP verification",
        "not been restore-tested",
        "bin/course-package verify",
    ),
    "automated packaging contract",
)
