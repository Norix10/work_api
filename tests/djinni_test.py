import asyncio
from parsers.djinni import DjinniParser

async def main():
    parser = DjinniParser()
    jobs = await parser.fetch_jobs()
    for job in jobs:
        print(job.title, job.url)

asyncio.run(main())