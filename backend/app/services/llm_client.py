from __future__ import annotations
import json
import os
import re
import time
import httpx
from typing import Any, List
from ..logger import get_logger

logger = get_logger("llm_client")

DEFAULT_LOCAL_MODELS = [
    "llama3.1:latest",
    "llama3.2:latest",
    "qwen2.5-coder:14b",
    "qwen3:4b",
    "gemma4:latest",
]

DEFAULT_CLOUD_MODELS = [
    "gpt-4o",
    "gpt-4o-mini",
    "claude-3-5-sonnet",
    "gemini-1.5-pro",
    "deepseek-chat",
]

class UnifiedLLMClient:
    """Hybrid LLM Client supporting both local open-source models (Ollama/vLLM)
    and Cloud AI providers (Azure OpenAI, OpenAI, Groq, OpenRouter, Gemini)."""

    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "local")  # "local" or "cloud"
        self.local_base_url = os.getenv("LLM_LOCAL_BASE_URL", "http://localhost:11434").rstrip("/")
        self.cloud_base_url = os.getenv("LLM_CLOUD_BASE_URL", "https://api.openai.com/v1").rstrip("/")
        self.model = os.getenv("LLM_MODEL", "llama3.1:latest")
        self.api_key = os.getenv("LLM_API_KEY", "")
        self.timeout = float(os.getenv("LLM_TIMEOUT", "45.0"))
        logger.info(
            "UnifiedLLMClient initialized: provider=%s, model=%s, endpoint=%s",
            self.provider,
            self.model,
            self.current_base_url,
        )

    @property
    def current_base_url(self) -> str:
        return self.cloud_base_url if self.provider == "cloud" else self.local_base_url

    async def get_config(self, is_connected: bool = True) -> dict[str, Any]:
        local_models = list(DEFAULT_LOCAL_MODELS)
        try:
            async with httpx.AsyncClient(timeout=1.5) as client:
                res = await client.get(f"{self.local_base_url}/api/tags")
                if res.status_code == 200:
                    data = res.json()
                    names = [m["name"] for m in data.get("models", []) if "name" in m]
                    if names:
                        local_models = names
        except Exception as e:
            logger.debug("Could not fetch Ollama local tags (%s), using defaults", e)

        return {
            "provider": self.provider,
            "model": self.model,
            "base_url": self.current_base_url,
            "has_api_key": bool(self.api_key),
            "available_local_models": local_models,
            "available_cloud_models": DEFAULT_CLOUD_MODELS,
            "is_connected": is_connected,
        }

    def update_config(self, provider: str, model: str, base_url: str | None = None, api_key: str | None = None) -> None:
        old_provider = self.provider
        old_model = self.model
        self.provider = provider
        self.model = model
        if base_url:
            if provider == "cloud":
                self.cloud_base_url = base_url.rstrip("/")
            else:
                self.local_base_url = base_url.rstrip("/")
        if api_key is not None:
            self.api_key = api_key

        logger.info(
            "LLM Config updated: %s:%s -> %s:%s (endpoint=%s)",
            old_provider,
            old_model,
            self.provider,
            self.model,
            self.current_base_url,
        )

    async def check_health(self) -> bool:
        """Check if active LLM endpoint (local or cloud) is reachable."""
        try:
            headers = {}
            if self.provider == "cloud" and self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"

            url = f"{self.current_base_url}/models" if self.provider == "cloud" else f"{self.local_base_url}/api/tags"
            async with httpx.AsyncClient(timeout=3.0, headers=headers) as client:
                res = await client.get(url)
                is_healthy = res.status_code in (200, 401)
                logger.debug("Health check to %s: HTTP %d (healthy=%s)", url, res.status_code, is_healthy)
                return is_healthy
        except Exception as e:
            logger.warning("Health check failed for %s (%s)", self.current_base_url, e)
            return False

    async def test_connection(
        self,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
    ) -> dict[str, Any]:
        """Test active model with a lightweight test prompt with fast timeout and 2048 context."""
        active_provider = provider or self.provider
        active_model = model or self.model
        active_base_url = (base_url or (self.cloud_base_url if active_provider == "cloud" else self.local_base_url)).rstrip("/")
        active_key = api_key or self.api_key

        logger.info("Testing connection to model '%s' via %s (%s)...", active_model, active_provider, active_base_url)
        start_time = time.time()
        try:
            if active_provider == "local":
                native_url = f"{active_base_url}/api/chat"
                payload = {
                    "model": active_model,
                    "messages": [
                        {"role": "system", "content": "You are an assistant. Respond with 'PONG'."},
                        {"role": "user", "content": "PING"},
                    ],
                    "stream": False,
                    "options": {"temperature": 0.1, "num_predict": 10, "num_ctx": 2048},
                }
                async with httpx.AsyncClient(timeout=15.0) as client:
                    res = await client.post(native_url, json=payload)
                    if res.status_code == 200:
                        data = res.json()
                        duration = time.time() - start_time
                        msg = f"Connected to {active_model} in {duration:.2f}s. Response: '{data.get('message', {}).get('content', '').strip()}'"
                        return {"success": True, "provider": active_provider, "model": active_model, "message": msg}
                    else:
                        raise Exception(f"HTTP {res.status_code}: {res.text[:120]}")
            else:
                reply = await self._call_chat_completion(
                    "You are an assistant. Respond with 'PONG'.",
                    "PING",
                    max_tokens=10,
                )
                duration = time.time() - start_time
                msg = f"Connected to {active_model} via {active_provider} in {duration:.2f}s. Response: '{reply.strip()}'"
                return {"success": True, "provider": active_provider, "model": active_model, "message": msg}
        except httpx.ConnectError:
            duration = time.time() - start_time
            err_msg = f"Cannot reach {active_base_url}. Ollama is not running on your computer. Please start Ollama."
            return {"success": False, "provider": active_provider, "model": active_model, "message": err_msg}
        except httpx.TimeoutException:
            duration = time.time() - start_time
            err_msg = f"Connection timed out after {duration:.2f}s. Model '{active_model}' took too long to load into memory."
            return {"success": False, "provider": active_provider, "model": active_model, "message": err_msg}
        except Exception as e:
            duration = time.time() - start_time
            err_msg = f"Connection failed after {duration:.2f}s: {str(e)}"
            return {"success": False, "provider": active_provider, "model": active_model, "message": err_msg}

    async def stream_test_connection(
        self,
        provider: str = "local",
        model: str = "llama3.1:latest",
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
    ):
        """Stream real-time SSE diagnostic events for connection verification."""
        import json
        import asyncio

        target_base_url = (base_url or (self.cloud_base_url if provider == "cloud" else self.local_base_url)).rstrip("/")
        start_time = time.time()

        # Step 1: Endpoint Reachability
        yield f"data: {json.dumps({'step': 1, 'phase': 'HOST_CHECK', 'status': 'running', 'message': f'Connecting to host endpoint: {target_base_url}...', 'elapsed': round(time.time() - start_time, 2)})}\n\n"
        await asyncio.sleep(0.05)

        tags_data = {}
        try:
            headers = {}
            if provider == "cloud" and (api_key or self.api_key):
                headers["Authorization"] = f"Bearer {api_key or self.api_key}"

            check_url = f"{target_base_url}/models" if provider == "cloud" else f"{target_base_url}/api/tags"
            async with httpx.AsyncClient(timeout=4.0, headers=headers) as client:
                res = await client.get(check_url)
                if res.status_code in (200, 401):
                    host_latency = round(time.time() - start_time, 2)
                    yield f"data: {json.dumps({'step': 1, 'phase': 'HOST_CHECK', 'status': 'success', 'message': f'Host is online and reachable (responded in {host_latency}s)', 'elapsed': host_latency})}\n\n"
                    if res.status_code == 200 and provider == "local":
                        tags_data = res.json()
                else:
                    err_msg = f"Host returned HTTP {res.status_code} ({res.reason_phrase})"
                    yield f"data: {json.dumps({'step': 1, 'phase': 'HOST_CHECK', 'status': 'error', 'message': err_msg, 'elapsed': round(time.time() - start_time, 2), 'done': True, 'success': False})}\n\n"
                    return
        except httpx.ConnectError:
            err_msg = f"Cannot reach {target_base_url}. Ollama is not running on your computer. Please open Ollama."
            yield f"data: {json.dumps({'step': 1, 'phase': 'HOST_CHECK', 'status': 'error', 'message': err_msg, 'elapsed': round(time.time() - start_time, 2), 'done': True, 'success': False})}\n\n"
            return
        except Exception as e:
            err_msg = f"Failed to reach {target_base_url}: {str(e)}"
            yield f"data: {json.dumps({'step': 1, 'phase': 'HOST_CHECK', 'status': 'error', 'message': err_msg, 'elapsed': round(time.time() - start_time, 2), 'done': True, 'success': False})}\n\n"
            return

        # Step 2: Model Installation Verification
        msg_check = f"Verifying installed weights for '{model}'..."
        yield f"data: {json.dumps({'step': 2, 'phase': 'MODEL_CHECK', 'status': 'running', 'message': msg_check, 'elapsed': round(time.time() - start_time, 2)})}\n\n"
        await asyncio.sleep(0.05)

        if provider == "local":
            models_list = [m["name"] for m in tags_data.get("models", []) if "name" in m]
            model_base = model.split(":")[0]
            matched = any(m == model or m.startswith(model_base + ":") or m == model_base for m in models_list)
            if matched:
                msg_verified = f"Model '{model}' verified in local library"
                yield f"data: {json.dumps({'step': 2, 'phase': 'MODEL_CHECK', 'status': 'success', 'message': msg_verified, 'elapsed': round(time.time() - start_time, 2)})}\n\n"
            else:
                avail_str = ", ".join(models_list[:4]) if models_list else "None"
                err_msg = f"Model '{model}' is not installed in Ollama. (Available models: {avail_str}). Run 'ollama pull {model}' in terminal or choose an installed model from the dropdown."
                yield f"data: {json.dumps({'step': 2, 'phase': 'MODEL_CHECK', 'status': 'error', 'message': err_msg, 'elapsed': round(time.time() - start_time, 2), 'done': True, 'success': False})}\n\n"
                return
        else:
            msg_cloud = f"Cloud model route verified for '{model}'"
            yield f"data: {json.dumps({'step': 2, 'phase': 'MODEL_CHECK', 'status': 'success', 'message': msg_cloud, 'elapsed': round(time.time() - start_time, 2)})}\n\n"

        # Step 3: Fast Neural Handshake (num_ctx: 2048)
        yield f"data: {json.dumps({'step': 3, 'phase': 'NEURAL_PING', 'status': 'running', 'message': f'Sending test PING to {model} (fast 2k context)...', 'elapsed': round(time.time() - start_time, 2)})}\n\n"

        try:
            if provider == "local":
                native_url = f"{target_base_url}/api/chat"
                payload = {
                    "model": model,
                    "messages": [
                        {"role": "system", "content": "You are a test assistant. Answer with PONG."},
                        {"role": "user", "content": "PING"},
                    ],
                    "stream": False,
                    "options": {"num_ctx": 2048, "num_predict": 10, "temperature": 0.1},
                }
                async with httpx.AsyncClient(timeout=60.0) as client:
                    post_task = asyncio.create_task(client.post(native_url, json=payload))
                    while not post_task.done():
                        await asyncio.sleep(2.0)
                        if not post_task.done():
                            curr_elapsed = round(time.time() - start_time, 1)
                            if curr_elapsed < 15:
                                msg = f"Connecting to {model}... Handshake in progress ({curr_elapsed}s)"
                            elif curr_elapsed < 40:
                                msg = f"Model {model} is loading weights into RAM memory ({curr_elapsed}s)..."
                            elif curr_elapsed < 60:
                                msg = f"Still attempting to connect ({curr_elapsed}s)... RAM allocation in progress. Please wait..."
                            else:
                                msg = f"Exceeded 60s ({curr_elapsed}s)... Still waiting for Ollama PONG response..."
                            yield f"data: {json.dumps({'step': 3, 'phase': 'NEURAL_PING', 'status': 'running', 'message': msg, 'elapsed': curr_elapsed})}\n\n"

                    chat_res = await post_task
                    if chat_res.status_code == 200:
                        total_duration = round(time.time() - start_time, 2)
                        yield f"data: {json.dumps({'step': 3, 'phase': 'NEURAL_PING', 'status': 'success', 'message': f'💥 PONG received! Model responded in {total_duration}s', 'elapsed': total_duration})}\n\n"
                        yield f"data: {json.dumps({'done': True, 'success': True, 'message': f'Connected to {model} (Pong 200 OK)! Ready to generate courses.', 'model': model, 'latency': total_duration})}\n\n"
                        return
                    else:
                        raise Exception(f"HTTP {chat_res.status_code}: {chat_res.text[:120]}")
            else:
                cloud_url = f"{target_base_url}/chat/completions" if not target_base_url.endswith("/chat/completions") else target_base_url
                payload = {
                    "model": model,
                    "messages": [{"role": "user", "content": "PING"}],
                    "max_tokens": 10,
                }
                async with httpx.AsyncClient(timeout=30.0, headers=headers) as client:
                    post_task = asyncio.create_task(client.post(cloud_url, json=payload))
                    while not post_task.done():
                        await asyncio.sleep(2.0)
                        if not post_task.done():
                            curr_elapsed = round(time.time() - start_time, 1)
                            yield f"data: {json.dumps({'step': 3, 'phase': 'NEURAL_PING', 'status': 'running', 'message': f'Waiting for cloud provider response ({curr_elapsed}s)...', 'elapsed': curr_elapsed})}\n\n"

                    chat_res = await post_task
                    chat_res.raise_for_status()
                    total_duration = round(time.time() - start_time, 2)
                    yield f"data: {json.dumps({'step': 3, 'phase': 'NEURAL_PING', 'status': 'success', 'message': f'💥 PONG received! Cloud model responded in {total_duration}s', 'elapsed': total_duration})}\n\n"
                    yield f"data: {json.dumps({'done': True, 'success': True, 'message': f'Connected to {model} (Pong 200 OK)! Ready to generate courses.', 'model': model, 'latency': total_duration})}\n\n"
                    return
        except httpx.TimeoutException:
            total_duration = round(time.time() - start_time, 2)
            err_msg = f"Timed out after {total_duration}s without receiving PONG. The model is NOT connected. Possible reasons: Model '{model}' is too heavy for CPU/RAM, or background tasks are slowing Ollama down. Recommendation: Try llama3.2 (faster 3B) or restart Ollama."
            yield f"data: {json.dumps({'step': 3, 'phase': 'NEURAL_PING', 'status': 'error', 'message': err_msg, 'elapsed': total_duration, 'done': True, 'success': False})}\n\n"
            return
        except Exception as e:
            total_duration = round(time.time() - start_time, 2)
            err_msg = f"Neural handshake failed after {total_duration}s: {str(e)}"
            yield f"data: {json.dumps({'step': 3, 'phase': 'NEURAL_PING', 'status': 'error', 'message': err_msg, 'elapsed': total_duration, 'done': True, 'success': False})}\n\n"
            return

    async def _call_chat_completion(self, system_prompt: str, user_prompt: str, max_tokens: int = 1500) -> str:
        headers = {}
        if self.provider == "cloud" and self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        start_time = time.time()

        # 1. If Local Ollama, try native /api/chat with reasonable num_ctx
        if self.provider == "local":
            native_url = f"{self.local_base_url}/api/chat"
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "stream": False,
                "options": {
                    "temperature": 0.2,
                    "num_predict": max_tokens,
                    "num_ctx": 2048 if max_tokens <= 20 else 8192,
                },
            }
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    res = await client.post(native_url, json=payload)
                    if res.status_code == 200:
                        data = res.json()
                        duration = time.time() - start_time
                        logger.info("Ollama native chat completion succeeded in %.2fs (model=%s)", duration, self.model)
                        return data["message"]["content"]
            except Exception as e:
                logger.debug("Ollama native /api/chat failed (%s), attempting OpenAI format fallback...", e)

        # 2. Standard OpenAI-compatible format (/v1/chat/completions)
        endpoint = self.current_base_url
        if not endpoint.endswith("/chat/completions"):
            endpoint = f"{endpoint.rstrip('/')}/v1/chat/completions" if "/v1" not in endpoint else f"{endpoint.rstrip('/')}/chat/completions"

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.2,
            "max_tokens": max_tokens,
        }

        async with httpx.AsyncClient(timeout=self.timeout, headers=headers) as client:
            response = await client.post(endpoint, json=payload)
            response.raise_for_status()
            data = response.json()
            duration = time.time() - start_time
            logger.info("OpenAI-compatible chat completion succeeded in %.2fs (endpoint=%s, model=%s)", duration, endpoint, self.model)
            return data["choices"][0]["message"]["content"]

    async def extract_proposal(self, url: str, scraped: dict[str, Any]) -> dict[str, Any]:
        """Use active LLM (Local or Cloud) to extract structured Course Proposal."""
        system_prompt = (
            "You are an expert instructional designer converting web learning resources into "
            "standardized Moodle courses. Respond ONLY with valid, raw JSON (no markdown fences, no explanation)."
        )

        user_prompt = f"""
Analyze this web resource and produce a Course Proposal.

URL: {url}
Detected Page Title: {scraped.get('title')}
Detected Headings: {', '.join(scraped.get('headings', []))}
Duration Hint: {scraped.get('raw_duration')}
Content Excerpt:
{scraped.get('body', '')[:3000]}

Generate JSON with EXACTLY these keys:
{{
  "course_name": "Short, clear professional title (under 50 chars)",
  "course_overview": "1-2 sentences on what the learner will accomplish and understand.",
  "course_duration_minutes": 90,
  "level": "beginner", 
  "audience": "Target learner persona",
  "topics": ["Module 1 title", "Module 2 title", "Module 3 title"]
}}

Rules:
- "level" MUST be one of: "beginner", "intermediate", "advanced".
- "course_duration_minutes" must be an integer (e.g. 60, 90, 120).
- "topics" must contain 3 to 6 distinct module titles based on the text.
"""

        try:
            logger.info("Invoking LLM (%s:%s) for curriculum proposal extraction on %s", self.provider, self.model, url)
            raw_response = await self._call_chat_completion(system_prompt, user_prompt)
            cleaned = re.sub(r"^```(?:json)?\s*", "", raw_response.strip(), flags=re.MULTILINE)
            cleaned = re.sub(r"```$", "", cleaned.strip(), flags=re.MULTILINE).strip()
            data = json.loads(cleaned)
            logger.info("LLM successfully generated proposal for '%s': course_name='%s'", url, data.get("course_name"))
            return data
        except Exception as e:
            logger.warning("LLM generation failed for %s (%s). Engaging deterministic heuristic fallback.", url, str(e))
            return self._heuristic_fallback(url, scraped)

    def _heuristic_fallback(self, url: str, scraped: dict[str, Any]) -> dict[str, Any]:
        title = scraped.get("title") or "Technical Learning Course"
        title = re.sub(r"\s*[-|]\s*.*$", "", title).strip()[:50]

        topics = scraped.get("headings", [])
        if not topics:
            topics = [
                "Foundational Concepts and Architecture",
                "Core Implementation and Workflows",
                "Best Practices and Governance",
            ]

        logger.info("Heuristic fallback synthesized proposal for '%s' (title='%s', %d topics)", url, title, len(topics))
        return {
            "course_name": title or "Introduction to Course Topics",
            "course_overview": (
                "Understand the core architecture, operational workflows, and practical techniques "
                "to effectively design and implement enterprise solutions."
            ),
            "course_duration_minutes": 90,
            "level": "beginner",
            "audience": "Developers, architects, and technical analysts",
            "topics": topics[:5],
        }

# Backwards compatibility alias
LocalLLMClient = UnifiedLLMClient
