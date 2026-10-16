from __future__ import annotations
import io
import os
import time
import uuid
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, UploadFile, File, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware

from .logger import setup_logging, get_logger, RECENT_LOGS_BUFFER
from .schemas import (
    UrlAnalysisRequest,
    CourseProposalSchema,
    GenerationJobResponse,
    ReferenceVideoItem,
    BatchJobRequest,
    BatchJobResponse,
    SystemStatusResponse,
    LLMConfigSchema,
    LLMConfigUpdateSchema,
    LLMTestResponse,
    UserProfileSchema,
    AuthStatusResponse,
    ConnectedAccountSchema,
    ProviderConnectRequest,
    ProvidersStatusResponse,
    ProposalPromptItem,
    ProposalFinalizeRequest,
    ExtractedUrlsResponse,
)
from .services.scraper import WebScraper
from .services.llm_client import build_proposal_prompts, parse_proposal_response
from .services.course_builder import CourseBuilderService, OUTPUT_DIR, slugify
from .services.session_store import session_store, UserSession, SESSION_COOKIE, SESSION_TTL_SECONDS


# Initialize structured logging
setup_logging(os.getenv("LOG_LEVEL", "INFO"))
logger = get_logger("main")

app = FastAPI(
    title="FX Learning Agent API",
    description="Enterprise orchestration service for AI-powered Moodle course generation",
    version="1.0.0",
)

# 1. Production Request Tracing & Performance Logging Middleware
class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        req_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())[:8]
        start_time = time.time()

        client_host = request.client.host if request.client else "unknown"
        logger.info("[%s] Incoming %s %s from %s", req_id, request.method, request.url.path, client_host)

        try:
            response: Response = await call_next(request)
            duration_ms = (time.time() - start_time) * 1000
            response.headers["X-Request-ID"] = req_id
            response.headers["X-Process-Time-Ms"] = f"{duration_ms:.2f}"
            logger.info(
                "[%s] Completed %s %s -> %d (%.1fms)",
                req_id,
                request.method,
                request.url.path,
                response.status_code,
                duration_ms,
            )
            return response
        except Exception as exc:
            duration_ms = (time.time() - start_time) * 1000
            logger.error(
                "[%s] Unhandled exception processing %s %s after %.1fms: %s",
                req_id,
                request.method,
                request.url.path,
                duration_ms,
                exc,
                exc_info=True,
            )
            return JSONResponse(
                status_code=500,
                content={
                    "error": "InternalServerError",
                    "message": "An unexpected error occurred while processing the request.",
                    "request_id": req_id,
                },
                headers={"X-Request-ID": req_id},
            )

app.add_middleware(RequestLoggingMiddleware)

# 2. Per-user session middleware: every browser gets its own LLM selection and
#    cloud provider keys, so one user's settings never leak to other users.
class UserSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        incoming_sid = request.cookies.get(SESSION_COOKIE)
        sid, session = session_store.get_or_create(incoming_sid)
        request.state.session = session
        response: Response = await call_next(request)
        if sid != incoming_sid:
            is_https = request.headers.get("x-forwarded-proto", request.url.scheme) == "https"
            response.set_cookie(
                SESSION_COOKIE,
                sid,
                max_age=int(SESSION_TTL_SECONDS),
                httponly=True,
                samesite="lax",
                secure=is_https,
            )
        return response

app.add_middleware(UserSessionMiddleware)

def get_session(request: Request) -> UserSession:
    return request.state.session

# 3. CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Global Exception Handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    req_id = request.headers.get("X-Request-ID", "unknown")
    logger.warning("[%s] Validation error on %s: %s", req_id, request.url.path, exc.errors())
    return JSONResponse(
        status_code=422,
        content={
            "error": "ValidationError",
            "message": "Invalid input parameters provided.",
            "details": exc.errors(),
            "request_id": req_id,
        },
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    req_id = request.headers.get("X-Request-ID", "unknown")
    logger.warning("[%s] HTTP %d on %s: %s", req_id, exc.status_code, request.url.path, exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTPException",
            "message": exc.detail,
            "status_code": exc.status_code,
            "request_id": req_id,
        },
    )

scraper = WebScraper()
builder = CourseBuilderService()

# 4. Health & Production Probes
@app.get("/health")
def health_check():
    return {"status": "ok", "service": "fx-learning-agent-backend"}

@app.get("/health/liveness")
def liveness_probe():
    """Kubernetes / Azure Container Apps Liveness Probe."""
    return {"status": "alive", "timestamp": time.time()}

@app.get("/health/readiness")
async def readiness_probe():
    """Kubernetes / Azure Container Apps Readiness Probe."""
    storage_ready = OUTPUT_DIR.exists()
    status_code = 200 if storage_ready else 503
    return JSONResponse(
        status_code=status_code,
        content={
            "ready": storage_ready,
            "storage_mounted": storage_ready,
        },
    )


@app.get("/api/system-status", response_model=SystemStatusResponse)
async def system_status(request: Request):
    """Live diagnostic check for UI status bar.

    For the local provider the server only reports the user's selected model; the browser
    probes the user's own Ollama (http://localhost:11434 on their machine) directly."""
    llm = get_session(request).llm
    llm_ok = await llm.check_health()

    course_count = 0
    if OUTPUT_DIR.exists():
        course_count = sum(1 for item in OUTPUT_DIR.iterdir() if item.is_dir())
        
    docker_ok = False
    try:
        import shutil
        docker_ok = shutil.which("docker") is not None
    except Exception:
        pass

    if llm.provider == "local":
        active_model = llm.model
        ollama_state = "client_side"
        ollama_message = "Local models are detected by your browser on your own machine"
    else:
        active_model = llm.model if llm_ok else "Cloud AI Disconnected"
        ollama_state = "ready" if llm_ok else "offline"
        ollama_message = "Cloud AI Connected" if llm_ok else "Cloud AI Disconnected"

    import platform
    sys_name = platform.system().lower()
    host_os = "mac" if "darwin" in sys_name else ("windows" if "windows" in sys_name else "linux")

    return SystemStatusResponse(
        api_status="ok",
        llm_connected=llm_ok,
        llm_model=active_model,
        llm_provider=llm.provider,
        ollama_installed=False,
        ollama_state=ollama_state,
        ollama_message=ollama_message,
        host_os=host_os,
        output_courses_count=course_count,
        docker_available=docker_ok,
    )

# 5. Live Operational Telemetry Logs Endpoint
@app.get("/api/logs")
def get_recent_logs(level: Optional[str] = None, limit: int = 50):
    """Query recent backend execution logs for live observability and debugging."""
    logs = list(RECENT_LOGS_BUFFER)
    if level:
        lvl_upper = level.upper()
        logs = [entry for entry in logs if entry.get("level") == lvl_upper]
    return logs[-limit:]

# 6. Personal Cloud Provider Connections (Claude, ChatGPT, Gemini, Grok)
@app.get("/api/auth/providers", response_model=ProvidersStatusResponse)
def get_providers_status(request: Request):
    """Retrieve connection status and unlocked models for Claude, ChatGPT, Gemini, and Grok."""
    return get_session(request).auth.get_providers_status()

@app.post("/api/auth/connect/{provider_id}", response_model=ConnectedAccountSchema)
async def connect_provider(request: Request, provider_id: str, payload: Optional[ProviderConnectRequest] = None):
    """Authenticate and verify credentials directly with Claude, ChatGPT, Gemini, or Grok."""
    session = get_session(request)
    if not payload or not payload.api_key or not payload.api_key.strip():
        raise HTTPException(
            status_code=400,
            detail=f"Please provide your authentic {provider_id.title()} API Key / Token to sign in.",
        )
    try:
        connected = await session.auth.verify_and_connect(
            provider_id=provider_id,
            api_key=payload.api_key,
            email=payload.email,
            plan=payload.plan or "Personal Subscription",
        )
        # Register verified key into this user's LLM client for immediate usage
        session.llm.api_key = payload.api_key.strip()
        return connected
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/auth/disconnect/{provider_id}")
def disconnect_provider(request: Request, provider_id: str):
    """Disconnect a personal provider account and revert to local if model is currently active."""
    session = get_session(request)
    session.auth.disconnect_provider(provider_id)
    if session.llm.provider == "cloud":
        active_provider = session.auth.get_provider_for_model(session.llm.model)
        if active_provider == provider_id.lower():
            session.llm.update_config(provider="local", model="")
    return {"success": True, "disconnected": provider_id}

@app.get("/api/auth/status", response_model=AuthStatusResponse)
def get_auth_status(request: Request):
    """Check overall personal provider connections status."""
    return get_session(request).auth.get_auth_status()

@app.post("/api/auth/logout", response_model=AuthStatusResponse)
def logout(request: Request):
    """Disconnect all cloud providers and revert to local open-source models."""
    session = get_session(request)
    for p in ["claude", "chatgpt", "gemini", "grok"]:
        session.auth.disconnect_provider(p)
    if session.llm.provider == "cloud":
        session.llm.update_config(provider="local", model="")
    return session.auth.get_auth_status()

# 7. LLM Configuration & Testing Routes
@app.get("/api/llm/config", response_model=LLMConfigSchema)
async def get_llm_config(request: Request):
    """Retrieve current LLM provider, model, and endpoint configuration."""
    llm = get_session(request).llm
    is_connected = await llm.check_health()
    return await llm.get_config(is_connected=is_connected)

@app.post("/api/llm/config", response_model=LLMConfigSchema)
async def update_llm_config(request: Request, update: LLMConfigUpdateSchema):
    """Switch LLM provider (local <-> cloud), change active model or API key."""
    session = get_session(request)
    llm, auth_service = session.llm, session.auth
    if update.provider == "cloud":
        req_provider = auth_service.get_provider_for_model(update.model) or "cloud"
        if not auth_service.is_model_allowed(update.model):
            raise HTTPException(
                status_code=401,
                detail=f"Please connect your {req_provider.title()} account or subscription first to activate {update.model}.",
            )

    llm.update_config(
        provider=update.provider,
        model=update.model,
        base_url=update.base_url,
        api_key=update.api_key,
    )
    is_connected = await llm.check_health()
    return await llm.get_config(is_connected=is_connected)

def _reject_server_side_local(provider: Optional[str]) -> None:
    if provider == "local":
        raise HTTPException(
            status_code=409,
            detail="Local Ollama runs on your own machine and is tested from your browser, not the server.",
        )

@app.post("/api/llm/test", response_model=LLMTestResponse)
async def test_llm_connection(request: Request, config: Optional[LLMConfigUpdateSchema] = None):
    """Test connectivity to current active or specified cloud LLM model."""
    llm = get_session(request).llm
    _reject_server_side_local(config.provider if config else llm.provider)
    if config:
        result = await llm.test_connection(
            provider=config.provider,
            model=config.model,
            base_url=config.base_url,
            api_key=config.api_key,
        )
    else:
        result = await llm.test_connection()
    return result

@app.get("/api/llm/test-stream")
async def stream_test_llm_connection(
    request: Request,
    provider: Optional[str] = None,
    model: Optional[str] = None,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
):
    """Stream real-time SSE diagnostic events for cloud connection verification."""
    from fastapi.responses import StreamingResponse
    llm = get_session(request).llm
    _reject_server_side_local(provider or llm.provider)
    return StreamingResponse(
        llm.stream_test_connection(
            provider=provider or llm.provider,
            model=model or llm.model,
            base_url=base_url,
            api_key=api_key,
        ),
        media_type="text/event-stream",
    )


# 7. Workflow Endpoints
def _build_proposal(url: str, index: int, scraped: dict, ai_data: dict) -> CourseProposalSchema:
    course_name = ai_data.get("course_name") or scraped.get("title") or "Technical Course"
    proposal_id = f"prop-{int(time.time() * 1000)}-{index}"
    topics = [str(t) for t in ai_data.get("topics", []) if t]
    try:
        duration = max(1, int(ai_data.get("course_duration_minutes", 60)))
    except (TypeError, ValueError):
        duration = 60
    level = str(ai_data.get("level", "beginner")).strip().lower()
    if level not in ("beginner", "intermediate", "advanced"):
        level = "beginner"

    return CourseProposalSchema(
        id=proposal_id,
        source_url=url,
        course_name=course_name,
        course_overview=ai_data.get("course_overview", ""),
        course_duration_minutes=duration,
        level=level,
        language="en-US",
        audience=ai_data.get("audience", "Technical professionals"),
        module_count=len(topics) or 1,
        topics=topics,
        # No reference videos are invented; the Videos activity says none were selected.
        reference_videos=[],
        is_approved=False,
        status="pending",
    )

@app.post("/api/analyze-urls", response_model=List[CourseProposalSchema])
async def analyze_urls(request: Request, body: UrlAnalysisRequest):
    """Scrape web pages and invoke the user's cloud LLM to propose course brief metadata.

    Local Ollama users go through /api/proposals/prepare + /api/proposals/finalize instead,
    because their model runs on their own machine and is called by their browser."""
    llm = get_session(request).llm
    _reject_server_side_local(llm.provider)
    pages = await _scrape_all(body.urls)
    proposals = [
        _build_proposal(url, index, scraped, await llm.extract_proposal(url, scraped))
        for index, (url, scraped) in enumerate(pages)
    ]
    return proposals

async def _scrape_all(urls: List[str]) -> List[tuple[str, dict]]:
    """Scrape every URL; reject the request if any page cannot be opened, so no course is
    ever invented from a URL whose content was never read."""
    pages: List[tuple[str, dict]] = []
    failures: List[str] = []
    for url in urls:
        url = url.strip()
        if not url:
            continue
        scraped = await scraper.extract_content(url)
        if scraped.get("fetch_error"):
            failures.append(f"{url} ({scraped['fetch_error']})")
        else:
            pages.append((url, scraped))
    if failures:
        raise HTTPException(status_code=400, detail="Could not open: " + "; ".join(failures))
    if not pages:
        raise HTTPException(status_code=400, detail="No valid URLs provided")
    return pages

@app.post("/api/proposals/prepare", response_model=List[ProposalPromptItem])
async def prepare_proposals(body: UrlAnalysisRequest):
    """Scrape pages and return the prompts for the browser to run on the user's local Ollama."""
    items: List[ProposalPromptItem] = []
    for url, scraped in await _scrape_all(body.urls):
        system_prompt, user_prompt = build_proposal_prompts(url, scraped)
        items.append(
            ProposalPromptItem(url=url, scraped=scraped, system_prompt=system_prompt, user_prompt=user_prompt)
        )
    return items

@app.post("/api/proposals/finalize", response_model=CourseProposalSchema)
def finalize_proposal(body: ProposalFinalizeRequest):
    """Turn the user's local model reply into a course proposal (heuristic fallback if unparseable)."""
    scraped = body.scraped.model_dump()
    ai_data = parse_proposal_response(body.raw_response, body.url, scraped)
    return _build_proposal(body.url, body.index, scraped, ai_data)

async def _extract_urls_from_upload(file: UploadFile) -> List[str]:
    import re
    content = await file.read()
    filename = file.filename or ""

    urls: List[str] = []
    url_re = re.compile(r"^\s*(https?://\S+?)\s*$", re.IGNORECASE)

    if filename.endswith(".csv"):
        import csv
        reader = csv.reader(io.StringIO(content.decode("utf-8-sig", errors="ignore")))
        for row in reader:
            for cell in row:
                m = url_re.match(cell)
                if m:
                    urls.append(m.group(1))
                    break
    elif filename.endswith((".xlsx", ".xlsm")):
        import openpyxl
        wb = openpyxl.load_workbook(io.BytesIO(content), read_only=True)
        sheet = wb.active
        for row in sheet.iter_rows(values_only=True):
            for cell in row:
                if cell and isinstance(cell, str):
                    m = url_re.match(cell)
                    if m:
                        urls.append(m.group(1))
                        break

    if not urls:
        raise HTTPException(status_code=400, detail="No valid HTTP URLs found in spreadsheet")

    # Analyze first 5 to keep batch fast
    return urls[:5]

@app.post("/api/extract-urls", response_model=ExtractedUrlsResponse)
async def extract_urls(file: UploadFile = File(...)):
    """Extract URLs from an uploaded .xlsx or .csv (used by the browser-side local Ollama flow)."""
    return ExtractedUrlsResponse(urls=await _extract_urls_from_upload(file))

@app.post("/api/upload-spreadsheet", response_model=List[CourseProposalSchema])
async def upload_spreadsheet(request: Request, file: UploadFile = File(...)):
    """Extract URLs from uploaded .xlsx or .csv and generate course proposals with the cloud LLM."""
    urls = await _extract_urls_from_upload(file)
    return await analyze_urls(request, UrlAnalysisRequest(urls=urls))

@app.post("/api/jobs", response_model=GenerationJobResponse)
async def start_generation_job(proposal: CourseProposalSchema):
    """Trigger the course packaging pipeline for an approved proposal."""
    return await builder.create_job(proposal)

@app.post("/api/jobs/batch", response_model=BatchJobResponse)
async def start_batch_jobs(request: BatchJobRequest):
    """Trigger packaging pipeline for multiple approved proposals."""
    batch_id = f"batch-{int(time.time() * 1000)}"
    jobs = await builder.create_batch_jobs(request.proposals)
    return BatchJobResponse(
        batch_id=batch_id,
        total_courses=len(jobs),
        jobs=jobs,
    )

@app.get("/api/jobs/{job_id}", response_model=GenerationJobResponse)
def get_job_status(job_id: str):
    job = builder.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@app.get("/api/courses", response_model=List[CourseProposalSchema])
def list_completed_courses():
    """List all completed courses currently available in output/."""
    courses: List[CourseProposalSchema] = []
    if not OUTPUT_DIR.exists():
        return courses

    for item in OUTPUT_DIR.iterdir():
        if item.is_dir():
            brief_path = item / "course-brief.json"
            mbz_path = item / "course-package.mbz"
            if brief_path.exists():
                try:
                    import json
                    data = json.loads(brief_path.read_text(encoding="utf-8"))
                    minutes = data.get("learning_time_minutes") or int(data.get("estimated_learning_hours", 1)) * 60
                    courses.append(
                        CourseProposalSchema(
                            id=item.name,
                            source_url=data.get("source_url", ""),
                            course_name=data.get("topic", item.name),
                            course_overview=data.get("intended_learning_outcome", ""),
                            course_duration_minutes=int(minutes),
                            level=data.get("entry_level", "beginner"),
                            language=data.get("language", "en-US"),
                            audience=data.get("audience") or data.get("target_audience") or "General",
                            module_count=len(data.get("sources", [])),
                            topics=[s.get("activity_name", "") for s in data.get("sources", [])],
                            is_approved=True,
                            status="completed" if mbz_path.exists() else "ready",
                            package_path=str(mbz_path) if mbz_path.exists() else None,
                        )
                    )
                except Exception as e:
                    logger.debug("Could not read course %s: %s", item.name, e)
    return courses

@app.get("/api/download/{course_slug}.mbz")
def download_course_package(course_slug: str):
    """Download the generated Moodle .mbz package file."""
    mbz_file = OUTPUT_DIR / course_slug / "course-package.mbz"
    if not mbz_file.exists():
        raise HTTPException(status_code=404, detail="Course package not found")
    return FileResponse(
        path=str(mbz_file),
        filename=f"{course_slug}-moodle-package.mbz",
        media_type="application/octet-stream",
    )

# ================= Monolithic Web Studio Static Mount =================
# Serves the Web Studio directly from root '/' on the exact same port.
candidate_web_dirs = [
    Path(__file__).resolve().parents[2] / "web_preview",
    Path("/app/web_preview"),
    Path(__file__).resolve().parent / "web_preview",
]
web_dir = next((d for d in candidate_web_dirs if d.exists()), None)
if web_dir:
    logger.info("Mounting monolithic Web Studio from: %s", web_dir)
    app.mount("/", StaticFiles(directory=str(web_dir), html=True), name="web_studio")

