import asyncio
import os

from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from playwright.async_api import async_playwright


async def main():
    print("[LUNA] starting...")

    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=os.getenv("BROWSER_PROFILE_DIR", "/tmp/luna-browser-profile"),
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
            ],
        )

        page = context.pages[0] if context.pages else await context.new_page()

        print("[LUNA] opening ChatGPT...")

        await page.goto(
            "https://chatgpt.com/",
            wait_until="domcontentloaded",
            timeout=60000,
        )

        await asyncio.sleep(5)

        url = page.url
        title = await page.title()
        is_cloudflare = (
            "__cf_chl" in url.lower()
            or "just a moment" in title.lower()
            or await page.locator(
                'script[src*="/cdn-cgi/challenge-platform/"], '
                'iframe[src*="challenges.cloudflare.com"]'
            ).count()
            > 0
        )

        print("[LUNA] URL:", url)
        print("[LUNA] TITLE:", title)

        if is_cloudflare:
            print("[LUNA] CLOUDFLARE_CHALLENGE")
        else:
            try:
                await page.locator("#prompt-textarea").wait_for(
                    state="visible", timeout=15000
                )
                print("[LUNA] CHATGPT_READY")
            except PlaywrightTimeoutError:
                print("[LUNA] CHATGPT_NOT_READY")

        while True:
            await asyncio.sleep(60)


asyncio.run(main())
