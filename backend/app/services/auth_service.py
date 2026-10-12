from __future__ import annotations
import os
from typing import Optional, Dict, Any, List
from ..schemas import ConnectedAccountSchema, ProvidersStatusResponse, AuthStatusResponse, UserProfileSchema
from ..logger import get_logger

logger = get_logger("auth_service")

import httpx

PROVIDER_CATALOG = {
    "claude": {
        "name": "Anthropic Claude",
        "models": ["claude-3-5-sonnet", "claude-3-opus", "claude-3-haiku"],
        "default_url": "https://api.anthropic.com/v1",
        "auth_url": "https://console.anthropic.com/settings/keys",
        "key_prefix": "sk-ant-",
    },
    "chatgpt": {
        "name": "OpenAI ChatGPT",
        "models": ["gpt-4o", "gpt-4o-mini", "o1-preview", "o1-mini"],
        "default_url": "https://api.openai.com/v1",
        "auth_url": "https://platform.openai.com/api-keys",
        "key_prefix": "sk-",
    },
    "gemini": {
        "name": "Google Gemini",
        "models": ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-ultra"],
        "default_url": "https://generativelanguage.googleapis.com/v1beta",
        "auth_url": "https://aistudio.google.com/app/apikey",
        "key_prefix": "AIzaSy",
    },
    "grok": {
        "name": "xAI Grok",
        "models": ["grok-2", "grok-2-mini", "grok-beta"],
        "default_url": "https://api.x.ai/v1",
        "auth_url": "https://console.x.ai/",
        "key_prefix": "xai-",
    },
}

class ProviderConnectionService:
    """Manages real personal subscription connections for Claude, ChatGPT, Gemini, and Grok.
    Requires genuine authentication verification before unlocking models."""

    def __init__(self):
        self._connected: Dict[str, Dict[str, Any]] = {}

    def get_providers_status(self) -> ProvidersStatusResponse:
        accounts: List[ConnectedAccountSchema] = []
        unlocked: List[str] = []

        for pid, meta in PROVIDER_CATALOG.items():
            conn_info = self._connected.get(pid)
            is_conn = conn_info is not None
            if is_conn:
                unlocked.extend(meta["models"])

            accounts.append(
                ConnectedAccountSchema(
                    provider_id=pid,
                    provider_name=meta["name"],
                    is_connected=is_conn,
                    account_email=conn_info.get("email") if is_conn else None,
                    plan=conn_info.get("plan") if is_conn else None,
                    available_models=meta["models"],
                )
            )

        return ProvidersStatusResponse(
            providers=accounts,
            any_connected=len(self._connected) > 0,
            unlocked_models=unlocked,
        )

    async def verify_and_connect(
        self,
        provider_id: str,
        api_key: Optional[str] = None,
        email: Optional[str] = None,
        plan: str = "Personal Subscription",
    ) -> ConnectedAccountSchema:
        pid = provider_id.lower().strip()
        if pid not in PROVIDER_CATALOG:
            raise ValueError(f"Unknown provider: {provider_id}. Available: {list(PROVIDER_CATALOG.keys())}")

        clean_key = (api_key or "").strip()
        if not clean_key:
            raise ValueError(f"Please provide your authentic {PROVIDER_CATALOG[pid]['name']} API Key to sign in and connect.")

        # Real verification request directly to the provider's API
        logger.info("Verifying live credentials with %s...", PROVIDER_CATALOG[pid]["name"])
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                if pid == "gemini":
                    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={clean_key}"
                    res = await client.get(url)
                    if res.status_code != 200:
                        raise ValueError(f"Google Gemini rejected credentials (HTTP {res.status_code}). Please verify your key from Google AI Studio.")
                elif pid == "chatgpt":
                    url = "https://api.openai.com/v1/models"
                    res = await client.get(url, headers={"Authorization": f"Bearer {clean_key}"})
                    if res.status_code != 200:
                        raise ValueError(f"OpenAI rejected credentials (HTTP {res.status_code}). Please verify your key from OpenAI Platform.")
                elif pid == "claude":
                    url = "https://api.anthropic.com/v1/models"
                    res = await client.get(url, headers={"x-api-key": clean_key, "anthropic-version": "2023-06-01"})
                    if res.status_code != 200:
                        raise ValueError(f"Anthropic Claude rejected credentials (HTTP {res.status_code}). Please verify your key from Anthropic Console.")
                elif pid == "grok":
                    url = "https://api.x.ai/v1/models"
                    res = await client.get(url, headers={"Authorization": f"Bearer {clean_key}"})
                    if res.status_code != 200:
                        raise ValueError(f"xAI Grok rejected credentials (HTTP {res.status_code}). Please verify your key from xAI Console.")
        except httpx.RequestError as e:
            raise ValueError(f"Could not reach {PROVIDER_CATALOG[pid]['name']} verification endpoint: {str(e)}")

        user_email = email or f"{pid}.subscriber@verified-account.com"
        self._connected[pid] = {
            "email": user_email,
            "api_key": clean_key,
            "plan": plan,
        }
        logger.info("Successfully verified and connected %s account: %s", PROVIDER_CATALOG[pid]["name"], user_email)

        return ConnectedAccountSchema(
            provider_id=pid,
            provider_name=PROVIDER_CATALOG[pid]["name"],
            is_connected=True,
            account_email=user_email,
            plan=plan,
            available_models=PROVIDER_CATALOG[pid]["models"],
        )

    def get_connected_key(self, provider_id: str) -> Optional[str]:
        pid = provider_id.lower().strip()
        return self._connected.get(pid, {}).get("api_key")

    def disconnect_provider(self, provider_id: str) -> None:
        pid = provider_id.lower().strip()
        if pid in self._connected:
            email = self._connected[pid].get("email")
            del self._connected[pid]
            logger.info("Disconnected %s account: %s", pid, email)

    def is_model_allowed(self, model_name: str) -> bool:
        """Verify if the provider supporting this model is legitimately connected and verified."""
        model_clean = model_name.lower().split(" ")[0]
        for pid, meta in PROVIDER_CATALOG.items():
            if any(m in model_clean for m in meta["models"]):
                return pid in self._connected
        return False

    def get_provider_for_model(self, model_name: str) -> Optional[str]:
        model_clean = model_name.lower().split(" ")[0]
        for pid, meta in PROVIDER_CATALOG.items():
            if any(m in model_clean for m in meta["models"]):
                return pid
        return None

    # Backward compatibility helper for general auth check
    def get_auth_status(self) -> AuthStatusResponse:
        status = self.get_providers_status()
        return AuthStatusResponse(
            is_authenticated=status.any_connected,
            user=UserProfileSchema(
                id="usr-personal",
                name="Connected User",
                email="personal-ai-hub@user.com",
            ) if status.any_connected else None,
            cloud_models_unlocked=status.any_connected,
            auth_provider="Personal Subscription / Account",
            allowed_cloud_models=status.unlocked_models,
            providers=status.providers,
        )

# Singleton instance
auth_service = ProviderConnectionService()
