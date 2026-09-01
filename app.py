import asyncio
from playwright.async_api import async_playwright


async def main():
    print("[LUNA] starting...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
            ],
        )

        page = await browser.new_page()

        print("[LUNA] opening ChatGPT...")

        await page.goto(
            "https://chatgpt.com/",
            wait_until="domcontentloaded",
            timeout=60000,
        )

        print("[LUNA] ChatGPT opened")
        print("[LUNA] URL:", page.url)
        print("[LUNA] TITLE:", await page.title())

        while True:
            await asyncio.sleep(60)


asyncio.run(main())
