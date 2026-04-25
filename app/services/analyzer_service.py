import time
import httpx
import asyncio
from collections import Counter
from bs4 import BeautifulSoup
from urllib.parse import urlparse

DOMAIN_LIMITERS: dict[str, asyncio.Semaphore] = {}

class AnalyzerService:
    async def analyze(self, url: str) -> dict:
        start = time.time()
        limiter = self.__get_domain_limiter(url)

        async with limiter:
            async with httpx.AsyncClient(
                    timeout=httpx.Timeout(connect=5),
                    follow_redirects=True,
            ) as client:
                response = await client.get(url)

        duration = int((time.time() - start) * 1000)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        title = soup.title.string if soup.title else None
        text = soup.get_text().lower()
        words = text.split()
        words_count = len(words)
        counter = Counter(words)
        top_words = [word for word, _ in counter.most_common(10)]

        return {
            "http_status_code": response.status_code,
            "response_time_ms": duration,
            "title": title,
            "word_count": words_count,
            "top_words": top_words,
        }

    async def __get_domain_limiter(self, url: str) -> asyncio.Semaphore:
        domain = urlparse(url).netloc
        if domain not in DOMAIN_LIMITERS:
            DOMAIN_LIMITERS[domain] = asyncio.Semaphore(2)
        return DOMAIN_LIMITERS[domain]