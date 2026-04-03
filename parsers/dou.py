import feedparser
import httpx
from bs4 import BeautifulSoup
from parsers.base import BaseParser
from app.schemas.job import JobCreate
from app.models.enums.job_enum import JobSource
from app.models.enums.dou_enum import LEVEL_MAP


class DouParser(BaseParser):
    BASE_URL = "https://jobs.dou.ua/vacancies/feeds/"

    def _clean_html(self, text: str | None) -> str | None:
        if not text:
            return None
        soup = BeautifulSoup(text, "html.parser")
        return soup.get_text(separator="\n").strip()

    async def fetch_jobs(
        self,
        technologies: list[str],
        level: str | None = None,
        remote_type: str | None = None,
    ) -> list[JobCreate]:
        all_jobs = []
        seen_urls = set()

        for keyword in technologies:
            url = f"{self.BASE_URL}?category={keyword}"
            if level:
                exp = LEVEL_MAP.get(level, "")
                if exp:
                    url += f"&exp={exp}"

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    url,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                    },
                )

            feed = feedparser.parse(response.text)

            for entry in feed.entries:
                if entry.link not in seen_urls:
                    title_lower = entry.title.lower()
                    description_lower = entry.get("summary", "").lower()
                    keyword_lower = keyword.lower()

                    if (
                        keyword_lower not in title_lower
                        and keyword_lower not in description_lower
                    ):
                        continue

                    seen_urls.add(entry.link)
                    all_jobs.append(
                        JobCreate(
                            title=entry.title,
                            url=entry.link,
                            description=self._clean_html(entry.get("summary", None)),
                            source=JobSource.dou,
                        )
                    )

        return all_jobs
