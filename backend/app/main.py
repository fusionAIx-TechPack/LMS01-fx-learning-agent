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
    PullModelRequest,
)
from .services.scraper import WebScraper
from .services.llm_client import UnifiedLLMClient, is_ollama_installed_on_system
from .services.course_builder import CourseBuilderService, OUTPUT_DIR, slugify
from .services.auth_service import auth_service, PROVIDER_CATALOG


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

# 2. CORS Middleware
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
llm = UnifiedLLMClient()
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
    llm_ready = await llm.check_health()
    storage_ready = OUTPUT_DIR.exists()
    status_code = 200 if storage_ready else 503
    return JSONResponse(
        status_code=status_code,
        content={
            "ready": storage_ready,
            "storage_mounted": storage_ready,
            "llm_accessible": llm_ready,
        },
    )


@app.get("/api/system-status", response_model=SystemStatusResponse)
async def system_status():
    """Live diagnostic check for UI status bar."""
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

    ollama_installed = is_ollama_installed_on_system()
    ollama_state = "ready"
    ollama_message = "Ollama is ready"

    if llm.provider == "local":
        if not ollama_installed:
            ollama_state = "not_installed"
            ollama_message = "Ollama is not installed on this system"
            active_model = "Ollama Not Installed"
        elif not llm_ok:
            is_running = False
            try:
                import httpx
                async with httpx.AsyncClient(timeout=1.0) as client:
                    r = await client.get(f"{llm.local_base_url}/api/tags")
                    if r.status_code == 200:
                        is_running = True
            except Exception:
                is_running = False

            if is_running:
                ollama_state = "no_models"
                ollama_message = "Ollama is running, but no models are downloaded"
                active_model = "No Models Downloaded"
            else:
                ollama_state = "not_running"
                ollama_message = "Ollama is installed, but not running"
                active_model = "Ollama Not Running"
        else:
            ollama_state = "ready"
            ollama_message = f"Ollama is ready ({llm.model})"
            active_model = llm.model
    else:
        active_model = llm.model if llm_ok else "Cloud AI Disconnected"

    import platform
    sys_name = platform.system().lower()
    host_os = "mac" if "darwin" in sys_name else ("windows" if "windows" in sys_name else "linux")

    return SystemStatusResponse(
        api_status="ok",
        llm_connected=llm_ok,
        llm_model=active_model or ("No Model Connected" if not llm_ok else "Active"),
        llm_provider=llm.provider,
        ollama_installed=ollama_installed,
        ollama_state=ollama_state,
        ollama_message=ollama_message,
        host_os=host_os,
        output_courses_count=course_count,
        docker_available=docker_ok,
    )

@app.get("/api/llm/models")
async def get_models_from_endpoint(endpoint: Optional[str] = None):
    """Dynamically query installed models from an Ollama endpoint (local or remote tunnel)
    with detailed diagnostics for installation, service status, and model availability."""
    target = (endpoint or llm.local_base_url).rstrip("/")
    is_local_host = any(h in target for h in ["localhost", "127.0.0.1", "0.0.0.0"])
    ollama_installed = is_ollama_installed_on_system() if is_local_host else True

    import platform
    sys_name = platform.system().lower()
    host_os = "mac" if "darwin" in sys_name else ("windows" if "windows" in sys_name else "linux")

    try:
        import httpx
        async with httpx.AsyncClient(timeout=3.0) as client:
            res = await client.get(f"{target}/api/tags")
            if res.status_code == 200:
                data = res.json()
                models = [m["name"] for m in data.get("models", []) if "name" in m]
                if models:
                    return {
                        "status": "ready",
                        "connected": True,
                        "ollama_installed": True,
                        "endpoint": target,
                        "models": models,
                        "count": len(models),
                        "host_os": host_os,
                        "message": f"Ollama is online with {len(models)} model(s) downloaded.",
                    }
                else:
                    return {
                        "status": "no_models",
                        "connected": True,
                        "ollama_installed": True,
                        "endpoint": target,
                        "models": [],
                        "count": 0,
                        "host_os": host_os,
                        "message": "Ollama is running, but no AI models have been downloaded yet.",
                    }
            return {
                "status": "http_error",
                "connected": False,
                "ollama_installed": ollama_installed,
                "endpoint": target,
                "models": [],
                "count": 0,
                "host_os": host_os,
                "error": f"Endpoint returned HTTP {res.status_code}",
                "message": f"Endpoint returned HTTP {res.status_code}",
            }
    except Exception as e:
        if is_local_host and not ollama_installed:
            return {
                "status": "not_installed",
                "connected": False,
                "ollama_installed": False,
                "endpoint": target,
                "models": [],
                "count": 0,
                "host_os": host_os,
                "error": "Ollama is not installed on this system.",
                "message": "Ollama is not installed on this computer.",
            }
        elif is_local_host and ollama_installed:
            return {
                "status": "not_running",
                "connected": False,
                "ollama_installed": True,
                "endpoint": target,
                "models": [],
                "count": 0,
                "host_os": host_os,
                "error": "Ollama is installed, but the background service is not running.",
                "message": "Ollama is installed, but not currently running.",
            }
        else:
            return {
                "status": "endpoint_unreachable",
                "connected": False,
                "ollama_installed": False,
                "endpoint": target,
                "models": [],
                "count": 0,
                "host_os": host_os,
                "error": str(e),
                "message": f"Cannot reach endpoint at {target}.",
            }

@app.post("/api/llm/pull")
async def pull_ollama_model(req: PullModelRequest):
    """Stream 1-click model download from Ollama using SSE events."""
    from fastapi.responses import StreamingResponse
    target = (req.endpoint or llm.local_base_url).rstrip("/")
    pull_url = f"{target}/api/pull"

    async def event_generator():
        import json
        import httpx
        try:
            async with httpx.AsyncClient(timeout=3600.0) as client:
                async with client.stream("POST", pull_url, json={"name": req.model, "stream": True}) as response:
                    if response.status_code != 200:
                        yield f"data: {json.dumps({'status': 'error', 'message': f'Ollama returned HTTP {response.status_code}', 'done': True})}\n\n"
                        return

                    async for line in response.aiter_lines():
                        if not line:
                            continue
                        try:
                            item = json.loads(line)
                            status_text = item.get("status", "")
                            total = item.get("total", 0)
                            completed = item.get("completed", 0)
                            percent = round((completed / total * 100), 1) if total > 0 else 0

                            yield f"data: {json.dumps({'status': status_text, 'total': total, 'completed': completed, 'percent': percent, 'done': False})}\n\n"
                        except Exception:
                            continue

            yield f"data: {json.dumps({'status': 'success', 'done': True, 'message': f'Model {req.model} downloaded successfully.'})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'status': 'error', 'done': True, 'message': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

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
def get_providers_status():
    """Retrieve connection status and unlocked models for Claude, ChatGPT, Gemini, and Grok."""
    return auth_service.get_providers_status()

@app.post("/api/auth/connect/{provider_id}", response_model=ConnectedAccountSchema)
async def connect_provider(provider_id: str, payload: Optional[ProviderConnectRequest] = None):
    """Authenticate and verify credentials directly with Claude, ChatGPT, Gemini, or Grok."""
    if not payload or not payload.api_key or not payload.api_key.strip():
        raise HTTPException(
            status_code=400,
            detail=f"Please provide your authentic {provider_id.title()} API Key / Token to sign in.",
        )
    try:
        connected = await auth_service.verify_and_connect(
            provider_id=provider_id,
            api_key=payload.api_key,
            email=payload.email,
            plan=payload.plan or "Personal Subscription",
        )
        # Register verified key into LLM client for immediate usage
        llm.api_key = payload.api_key.strip()
        return connected
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/auth/disconnect/{provider_id}")
def disconnect_provider(provider_id: str):
    """Disconnect a personal provider account and revert to local if model is currently active."""
    auth_service.disconnect_provider(provider_id)
    if llm.provider == "cloud":
        active_provider = auth_service.get_provider_for_model(llm.model)
        if active_provider == provider_id.lower():
            llm.update_config(provider="local", model="llama3.1:latest")
    return {"success": True, "disconnected": provider_id}

@app.get("/api/auth/status", response_model=AuthStatusResponse)
def get_auth_status():
    """Check overall personal provider connections status."""
    return auth_service.get_auth_status()

@app.post("/api/auth/logout", response_model=AuthStatusResponse)
def logout():
    """Disconnect all cloud providers and revert to local open-source models."""
    for p in ["claude", "chatgpt", "gemini", "grok"]:
        auth_service.disconnect_provider(p)
    if llm.provider == "cloud":
        llm.update_config(provider="local", model="llama3.1:latest")
    return auth_service.get_auth_status()

# 7. LLM Configuration & Testing Routes
@app.get("/api/llm/config", response_model=LLMConfigSchema)
async def get_llm_config():
    """Retrieve current LLM provider, model, and endpoint configuration."""
    is_connected = await llm.check_health()
    return await llm.get_config(is_connected=is_connected)

@app.post("/api/llm/config", response_model=LLMConfigSchema)
async def update_llm_config(update: LLMConfigUpdateSchema):
    """Switch LLM provider (local <-> cloud), change active model or API key."""
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

@app.post("/api/llm/test", response_model=LLMTestResponse)
async def test_llm_connection(config: Optional[LLMConfigUpdateSchema] = None):
    """Test connectivity to current active or specified LLM model."""
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
    provider: Optional[str] = None,
    model: Optional[str] = None,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
):
    """Stream real-time SSE diagnostic events for connection verification."""
    from fastapi.responses import StreamingResponse
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
@app.post("/api/analyze-urls", response_model=List[CourseProposalSchema])
async def analyze_urls(request: UrlAnalysisRequest):
    """Scrape web pages and invoke local/cloud LLM to propose course brief metadata."""
    proposals: List[CourseProposalSchema] = []

    for index, url in enumerate(request.urls):
        url = url.strip()
        if not url:
            continue

        scraped = await scraper.extract_content(url)
        ai_data = await llm.extract_proposal(url, scraped)

        course_name = ai_data.get("course_name") or scraped.get("title") or "Technical Course"
        proposal_id = f"prop-{int(time.time() * 1000)}-{index}"

        ref_videos = [
            ReferenceVideoItem(
                title=f"{course_name} - Architecture Overview",
                url="https://www.youtube.com/watch?v=sample1",
                publisher="Technical Community",
                note="Covers fundamental concepts and architecture overview",
            )
        ]

        proposals.append(
            CourseProposalSchema(
                id=proposal_id,
                source_url=url,
                course_name=course_name,
                course_overview=ai_data.get("course_overview", ""),
                course_duration_minutes=int(ai_data.get("course_duration_minutes", 60)),
                level=ai_data.get("level", "beginner"),
                language="en-US",
                audience=ai_data.get("audience", "Technical professionals"),
                module_count=len(ai_data.get("topics", [])) or 1,
                topics=ai_data.get("topics", []),
                reference_videos=ref_videos,
                is_approved=False,
                status="pending",
            )
        )

    if not proposals:
        raise HTTPException(status_code=400, detail="No valid URLs provided")

    return proposals

@app.post("/api/upload-spreadsheet", response_model=List[CourseProposalSchema])
async def upload_spreadsheet(file: UploadFile = File(...)):
    """Extract URLs from uploaded .xlsx or .csv and generate course proposals."""
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
    return await analyze_urls(UrlAnalysisRequest(urls=urls[:5]))

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
                    courses.append(
                        CourseProposalSchema(
                            id=item.name,
                            source_url=data.get("source_url", ""),
                            course_name=data.get("topic", item.name),
                            course_overview=data.get("intended_learning_outcome", ""),
                            course_duration_minutes=int(data.get("estimated_learning_hours", 1)) * 60,
                            level=data.get("entry_level", "beginner"),
                            language=data.get("language", "en-US"),
                            audience=data.get("target_audience", "General"),
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

