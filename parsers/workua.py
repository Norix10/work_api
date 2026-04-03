import httpx
from bs4 import BeautifulSoup
from parsers.base import BaseParser
from app.schemas.job import JobCreate
from app.models.enums.job_enum import JobSource

class WorkUaParser(BaseParser):
    BASE_URL = "https://www.work.ua/jobs-"

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
            url = f"{self.BASE_URL}{keyword.lower()}/"

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    url,
                    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
                )

            soup = BeautifulSoup(response.text, "html.parser")
            job_cards = soup.find_all("div", class_="card-hover") 

            for card in job_cards:
                link_tag = card.find("h2")
                if not link_tag:
                    continue
                a_tag = link_tag.find("a")
                if not a_tag:
                    continue

                job_url = "https://www.work.ua" + a_tag["href"]
                if job_url in seen_urls:
                    continue

                title = a_tag.get_text(strip=True)
                
                if keyword.lower() not in title.lower():
                    continue

                company_tag = card.find("a", {"href": lambda x: x and "/company/" in x})
                company = company_tag.get_text(strip=True) if company_tag else None

                description_tag = card.find("p", class_="text-default-7")
                description = description_tag.get_text(strip=True) if description_tag else None

                seen_urls.add(job_url)
                all_jobs.append(JobCreate(
                    title=title,
                    company=company,
                    url=job_url,
                    description=description,
                    source=JobSource.workua,
                ))

        return all_jobs