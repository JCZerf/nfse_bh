import asyncio
import time
from pathlib import Path

import httpx

CAPTCHA_URL = "https://bhissdigital.pbh.gov.br/nfse/captcha.jpg"
SAMPLES_DIR = Path(__file__).parent.parent / "samples"
CONCURRENCY = 20

HEADERS = {
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36"
    ),
}


async def download_one(client: httpx.AsyncClient, index: int, semaphore: asyncio.Semaphore) -> None:
    async with semaphore:
        response = await client.get(CAPTCHA_URL, params={"pk": index})
        response.raise_for_status()
        timestamp = int(time.time() * 1000)
        output_path = SAMPLES_DIR / f"captcha_{timestamp}_{index}.jpg"
        output_path.write_bytes(response.content)


async def collect_samples_async(count: int) -> None:
    SAMPLES_DIR.mkdir(parents=True, exist_ok=True)
    semaphore = asyncio.Semaphore(CONCURRENCY)
    async with httpx.AsyncClient(headers=HEADERS) as client:
        tasks = [download_one(client, index, semaphore) for index in range(count)]
        await asyncio.gather(*tasks)


def collect_samples(count: int) -> None:
    asyncio.run(collect_samples_async(count))


if __name__ == "__main__":
    collect_samples(count=500)
    print(f"Amostras salvas em {SAMPLES_DIR}")
