from __future__ import annotations
from typing import List, Optional, Any
from pydantic import BaseModel, Field

class ReferenceVideoItem(BaseModel):
    title: str
    url: str
    publisher: str
    note: str

class CourseProposalSchema(BaseModel):
    id: str
    source_url: str
    course_name: str
    course_overview: str
    course_duration_minutes: int = 60
    level: str = "beginner"  # beginner, intermediate, advanced
    language: str = "en-US"
    audience: str
    module_count: int = 1
    topics: List[str] = Field(default_factory=list)
    reference_videos: List[ReferenceVideoItem] = Field(default_factory=list)
    is_approved: bool = False
    status: str = "pending"
    error_message: Optional[str] = None
    package_path: Optional[str] = None

class UrlAnalysisRequest(BaseModel):
    urls: List[str]

class GenerationJobResponse(BaseModel):
    job_id: str
    course_slug: str
    course_name: str
    step: str
    progress: float
    logs: List[str]
    mbz_download_url: Optional[str] = None
    error: Optional[str] = None
    created_at: str

class BatchJobRequest(BaseModel):
    proposals: List[CourseProposalSchema]

class BatchJobResponse(BaseModel):
    batch_id: str
    total_courses: int
    jobs: List[GenerationJobResponse]

class SystemStatusResponse(BaseModel):
    api_status: str
    llm_connected: bool
    llm_model: str
    llm_provider: str = "local"
    output_courses_count: int
    docker_available: bool

class LLMConfigSchema(BaseModel):
    provider: str  # "local" | "cloud"
    model: str
    base_url: str
    has_api_key: bool
    available_local_models: List[str] = Field(default_factory=list)
    available_cloud_models: List[str] = Field(default_factory=list)
    is_connected: bool

class LLMConfigUpdateSchema(BaseModel):
    provider: str  # "local" | "cloud"
    model: str
    base_url: Optional[str] = None
    api_key: Optional[str] = None

class LLMTestResponse(BaseModel):
    success: bool
    provider: str
    model: str
    message: str

class UserProfileSchema(BaseModel):
    id: str
    name: str
    email: str
    tenant_name: str = "Enterprise Tenant"
    role: str = "Instructional Designer"
    avatar_initials: str = "FX"

class ConnectedAccountSchema(BaseModel):
    provider_id: str  # "claude" | "chatgpt" | "gemini" | "grok"
    provider_name: str
    is_connected: bool = False
    account_email: Optional[str] = None
    plan: Optional[str] = None
    available_models: List[str] = Field(default_factory=list)

class ProviderConnectRequest(BaseModel):
    email: Optional[str] = None
    api_key: Optional[str] = None
    plan: Optional[str] = "Personal Subscription"

class ProvidersStatusResponse(BaseModel):
    providers: List[ConnectedAccountSchema]
    any_connected: bool
    unlocked_models: List[str] = Field(default_factory=list)

class AuthStatusResponse(BaseModel):
    is_authenticated: bool
    user: Optional[UserProfileSchema] = None
    cloud_models_unlocked: bool = False
    auth_provider: Optional[str] = None
    allowed_cloud_models: List[str] = Field(default_factory=list)
    providers: List[ConnectedAccountSchema] = Field(default_factory=list)



