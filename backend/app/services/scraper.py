from __future__ import annotations
import re
import httpx
from bs4 import BeautifulSoup
from ..logger import get_logger

logger = get_logger("scraper")

try:
    import trafilatura
    HAS_TRAFILATURA = True
except ImportError:
    HAS_TRAFILATURA = False

class WebScraper:
    def __init__(self, timeout_seconds: float = 15.0):
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        }
        self.timeout = timeout_seconds

    async def extract_content(self, url: str) -> dict[str, str | list[str]]:
        """Fetch URL and extract clean text body, headings, and metadata."""
        logger.info("Extracting content from URL: %s", url)
        try:
            async with httpx.AsyncClient(headers=self.headers, follow_redirects=True, timeout=self.timeout) as client:
                response = await client.get(url)
                response.raise_for_status()
                html = response.text
                logger.info("Successfully fetched %s (HTTP %d, %d bytes)", url, response.status_code, len(html))
        except Exception as e:
            logger.warning("Scrape failed for %s (%s). Falling back to URL heuristic.", url, str(e))
            # Return basic fallback if URL fetch fails
            fallback_title = url.rstrip("/").split("/")[-1].replace("-", " ").title()
            return {
                "title": fallback_title or "Technical Learning Course",
                "body": f"Could not fetch full page content ({str(e)}). Using URL context.",
                "headings": [],
                "raw_duration": "",
                "fetch_error": str(e),
            }

        soup = BeautifulSoup(html, "html.parser")

        # 1. Title
        title = ""
        if soup.title and soup.title.string:
            title = soup.title.string.strip()
        h1 = soup.find("h1")
        if h1 and h1.get_text():
            title = h1.get_text().strip()

        # 2. Main content extraction
        body = ""
        if HAS_TRAFILATURA:
            body = trafilatura.extract(html, include_links=False, include_images=False) or ""
        if not body:
            paragraphs = [p.get_text().strip() for p in soup.find_all("p") if p.get_text().strip()]
            body = "\n\n".join(paragraphs[:15])

        # 3. Headings for topic extraction
        headings = [
            h.get_text().strip()
            for h in soup.find_all(["h2", "h3"])
            if h.get_text() and len(h.get_text().strip()) < 80
        ]

        # 4. Attempt duration pattern matching
        duration_hint = ""
        dur_match = re.search(r"(\d+\s*(?:hr|hour|min|minute|mins|hours)[s]?)", body or "", re.IGNORECASE)
        if dur_match:
            duration_hint = dur_match.group(1)

        logger.info(
            "Parsed URL %s: title='%s', extracted %d headings, content_len=%d",
            url,
            title[:40],
            len(headings),
            len(body),
        )

        return {
            "title": title or "Online Learning Course",
            "body": body[:5000] if body else "",
            "headings": headings[:8],
            "raw_duration": duration_hint,
        }
