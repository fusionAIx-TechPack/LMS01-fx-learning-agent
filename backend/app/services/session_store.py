from __future__ import annotations
import secrets
import threading
import time
from collections import OrderedDict
from dataclasses import dataclass, field

from .llm_client import UnifiedLLMClient
from .auth_service import ProviderConnectionService
from ..logger import get_logger

logger = get_logger("session_store")

SESSION_COOKIE = "fx_sid"
SESSION_TTL_SECONDS = 24 * 3600
MAX_SESSIONS = 5000


@dataclass
class UserSession:
    """Per-browser state: each user gets their own model selection and cloud provider keys."""
    llm: UnifiedLLMClient = field(default_factory=UnifiedLLMClient)
    auth: ProviderConnectionService = field(default_factory=ProviderConnectionService)
    last_seen: float = field(default_factory=time.time)


class SessionStore:
    """In-memory session registry keyed by an opaque cookie id.

    Evicts sessions idle longer than SESSION_TTL_SECONDS and caps total count
    (least recently used first) so memory stays bounded on a shared deployment.
    """

    def __init__(self, ttl: float = SESSION_TTL_SECONDS, max_sessions: int = MAX_SESSIONS):
        self._ttl = ttl
        self._max = max_sessions
        self._sessions: OrderedDict[str, UserSession] = OrderedDict()
        self._lock = threading.Lock()

    @staticmethod
    def new_id() -> str:
        return secrets.token_urlsafe(24)

    def get_or_create(self, sid: str | None) -> tuple[str, UserSession]:
        now = time.time()
        with self._lock:
            self._evict(now)
            if sid and sid in self._sessions:
                session = self._sessions[sid]
                session.last_seen = now
                self._sessions.move_to_end(sid)
                return sid, session

            new_sid = self.new_id()
            session = UserSession()
            self._sessions[new_sid] = session
            logger.info("Created user session (active sessions: %d)", len(self._sessions))
            return new_sid, session

    def _evict(self, now: float) -> None:
        while self._sessions:
            oldest_sid, oldest = next(iter(self._sessions.items()))
            if now - oldest.last_seen > self._ttl or len(self._sessions) >= self._max:
                del self._sessions[oldest_sid]
            else:
                break


session_store = SessionStore()
