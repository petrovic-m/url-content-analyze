import time
import httpx
import asyncio
import re
from collections import Counter
from bs4 import BeautifulSoup
from urllib.parse import urlparse

DOMAIN_LIMITERS: dict[str, asyncio.Semaphore] = {}
STOP_WORDS = {
    "a", "an", "the", "and", "or", "to", "for", "of", "in", "on", "at",
    "by", "with", "from", "as", "is", "are", "was", "were", "be", "been",
    "we", "you", "your", "our", "it", "this", "that", "they", "their",
}


class AnalyzerService:
    async def analyze(self, url: str) -> dict:
        start = time.time()
        limiter = self.__get_domain_limiter(url)

        async with limiter:
            async with httpx.AsyncClient(
                    timeout=httpx.Timeout(5.0),
                    follow_redirects=True
            ) as client:
                response = await client.get(url)

        duration = int((time.time() - start) * 1000)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        title = soup.title.string if soup.title else None
        text = soup.get_text(" ", strip=True).lower()
        words = re.findall(r"[a-zA-Z]{3,}", text)
        filtered_words = [
            word for word in words
            if word not in STOP_WORDS
        ]
        words_count = len(filtered_words)
        counter = Counter(filtered_words)
        top_words = [
            word for word, _ in counter.most_common(10)
        ]
        return {
            "http_status_code": response.status_code,
            "response_time_ms": duration,
            "title": title,
            "word_count": words_count,
            "top_words": top_words,
        }

    def __get_domain_limiter(self, url: str) -> asyncio.Semaphore:
        domain = urlparse(url).netloc
        if domain not in DOMAIN_LIMITERS:
            DOMAIN_LIMITERS[domain] = asyncio.Semaphore(2)
        return DOMAIN_LIMITERS[domain]