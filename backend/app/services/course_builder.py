from __future__ import annotations
import asyncio
import json
import re
import shutil
import sys
import uuid
from datetime import datetime
from urllib.parse import urlparse
from pathlib import Path
from typing import Any

from ..schemas import CourseProposalSchema, GenerationJobResponse
from ..logger import get_logger
from .mbz_builder import build_mbz

logger = get_logger("course_builder")

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

OUTPUT_DIR = REPO_ROOT / "output"

# In-memory store for jobs
ACTIVE_JOBS: dict[str, dict[str, Any]] = {}

def slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower()).strip("-")
    return slug or "generated-course"

class CourseBuilderService:
    def __init__(self):
        OUTPUT_DIR.mkdir(exist_ok=True)
        logger.info("CourseBuilderService initialized with OUTPUT_DIR: %s", OUTPUT_DIR)

    @staticmethod
    def _reserve_course_dir(base_slug: str) -> str:
        """Claim a fresh output folder so a new build never overwrites an existing course."""
        for n in range(1, 1000):
            slug = base_slug if n == 1 else f"{base_slug}-{n}"
            try:
                (OUTPUT_DIR / slug).mkdir(parents=True, exist_ok=False)
                return slug
            except FileExistsError:
                continue
        raise RuntimeError(f"Could not allocate an output folder for {base_slug}")

    async def create_job(self, proposal: CourseProposalSchema) -> GenerationJobResponse:
        slug = self._reserve_course_dir(slugify(proposal.course_name))
        job_id = f"job-{uuid.uuid4().hex[:12]}"

        logger.info("Creating generation job %s for '%s' (slug=%s)", job_id, proposal.course_name, slug)

        job_data = {
            "job_id": job_id,
            "course_slug": slug,
            "course_name": proposal.course_name,
            "step": "scrapingUrl",
            "progress": 0.1,
            "logs": ["Job created.", f"Target slug: {slug}"],
            "mbz_download_url": None,
            "error": None,
            "created_at": datetime.now().isoformat(),
            "proposal": proposal.dict(),
        }
        ACTIVE_JOBS[job_id] = job_data

        # Fire async background execution on active event loop
        asyncio.create_task(self._run_pipeline(job_id))

        return GenerationJobResponse(
            job_id=job_id,
            course_slug=slug,
            course_name=proposal.course_name,
            step="scrapingUrl",
            progress=0.1,
            logs=job_data["logs"],
            mbz_download_url=None,
            error=None,
            created_at=job_data["created_at"],
        )

    async def create_batch_jobs(self, proposals: list[CourseProposalSchema]) -> list[GenerationJobResponse]:
        logger.info("Creating batch generation jobs for %d proposals", len(proposals))
        jobs = []
        for p in proposals:
            job = await self.create_job(p)
            jobs.append(job)
        return jobs

    def get_job(self, job_id: str) -> GenerationJobResponse | None:
        data = ACTIVE_JOBS.get(job_id)
        if not data:
            return None
        return GenerationJobResponse(
            job_id=data["job_id"],
            course_slug=data["course_slug"],
            course_name=data["course_name"],
            step=data["step"],
            progress=data["progress"],
            logs=data["logs"],
            mbz_download_url=data["mbz_download_url"],
            error=data["error"],
            created_at=data["created_at"],
        )

    async def _run_pipeline(self, job_id: str) -> None:
        job = ACTIVE_JOBS[job_id]
        proposal = job["proposal"]
        slug = job["course_slug"]
        course_dir = OUTPUT_DIR / slug
        course_dir.mkdir(parents=True, exist_ok=True)

        logger.info("[%s] Pipeline started in %s", job_id, course_dir)

        try:
            # Step 1: Course Brief
            job["step"] = "synthesizingAi"
            job["progress"] = 0.3
            job["logs"].append("Writing Course Brief from the approved proposal...")

            brief_path = course_dir / "course-brief.json"
            brief_data = self._generate_brief_dict(proposal, slug)
            with brief_path.open("w", encoding="utf-8") as f:
                json.dump(brief_data, f, indent=2)
            job["logs"].append(f"Generated {brief_path.name} ({len(brief_data['sources'])} modules)")
            logger.info("[%s] Generated course brief: %s (%d sources)", job_id, brief_path.name, len(brief_data["sources"]))

            # Step 2: Course Definition (validates the brief and checks every source URL is reachable)
            job["step"] = "compilingDefinition"
            job["progress"] = 0.5
            job["logs"].append("Compiling Course Definition and checking source URLs are reachable...")

            def_path = course_dir / "course-definition.json"
            await asyncio.to_thread(self._compile_definition, brief_path, def_path)
            job["logs"].append(f"Course Definition validated: {def_path.name}")
            logger.info("[%s] Course definition compiled: %s", job_id, def_path.name)

            # Step 3: Moodle packaging from the engine-produced five-activity template.
            job["step"] = "packagingMbz"
            job["progress"] = 0.85
            job["logs"].append("Packaging Moodle 5.x backup (.mbz) with the 5 standard activities...")

            definition = json.loads(def_path.read_text(encoding="utf-8"))
            mbz_path = course_dir / "course-package.mbz"
            await asyncio.to_thread(build_mbz, definition, mbz_path)

            job["step"] = "completed"
            job["progress"] = 1.0
            job["logs"].append(f"Moodle Course Package created: {mbz_path.name} ({mbz_path.stat().st_size} bytes)")
            job["logs"].append("Activities: Course overview, resources link, reference videos, certification assignment, discussion forum.")
            job["mbz_download_url"] = f"/api/download/{slug}.mbz"
            logger.info("[%s] Pipeline completed for '%s'. MBZ package: %s", job_id, slug, mbz_path)

        except Exception as e:
            job["step"] = "failed"
            job["error"] = str(e)
            job["logs"].append(f"ERROR: {str(e)}")
            logger.error("[%s] Pipeline execution failed: %s", job_id, e, exc_info=True)
            # The folder was reserved for this job only; drop it so a failed build
            # does not show up in the Course Library.
            shutil.rmtree(course_dir, ignore_errors=True)

    def _generate_brief_dict(self, proposal: dict[str, Any], slug: str) -> dict[str, Any]:
        """Convert the approved UI proposal into the Course Brief schema that course_research accepts."""
        course_name = proposal["course_name"].strip()
        source_url = proposal["source_url"].strip()
        publisher = urlparse(source_url).netloc or "Web Resource"
        topics = [t.strip() for t in (proposal.get("topics") or []) if t and t.strip()] or ["Overview and Core Concepts"]
        total_minutes = max(len(topics), int(proposal.get("course_duration_minutes") or 60))
        # Module minutes must fit inside the course learning-time budget.
        per_module = total_minutes // len(topics)

        sources = []
        for i, t in enumerate(topics):
            sources.append({
                "title": f"{course_name} - {t}",
                "activity_name": t[:40].rstrip(),
                "url": source_url,
                "publisher": publisher,
                "provider_item_id": f"{source_url}#module-{i + 1}",
                "source_type": "article",
                "language": "en-US",
                "duration_minutes": per_module,
                "activity_duration_minutes": per_module,
                "activity_purpose": f"Understand and apply concepts for {t}.",
                "access": {
                    "free": True,
                    "basis": "Publicly accessible web page entered by the course requester",
                    "evidence_url": source_url,
                },
            })

        videos = [
            {
                "title": v["title"],
                "url": v["url"],
                "publisher": v["publisher"],
                "note": v["note"],
            }
            for v in proposal.get("reference_videos", [])
            if all(v.get(k) for k in ("title", "url", "publisher", "note"))
        ]

        overview = (proposal.get("course_overview") or "").strip()
        brief = {
            "topic": course_name,
            "audience": (proposal.get("audience") or "").strip() or "General learners",
            "entry_level": proposal.get("level") or "beginner",
            "language": "en-US",
            "intended_learning_outcome": overview or f"Understand the core concepts of {course_name}",
            "learning_time_minutes": total_minutes,
            "source_url": source_url,
            "sources": sources,
            "reference_videos": videos,
        }
        if overview:
            brief["course_description"] = overview
        return brief

    def _compile_definition(self, brief_path: Path, output_path: Path) -> None:
        """Validate the brief and write course-definition.json via course_research.

        Raises CourseDefinitionError with a requester-facing message if the brief is invalid
        or a source URL is unreachable; the job is then marked failed rather than faked."""
        from course_research.cli import load_course_brief
        from course_research.generator import write_course_definition

        logger.debug("Compiling course definition %s -> %s", brief_path, output_path)
        write_course_definition(load_course_brief(brief_path), output_path)
