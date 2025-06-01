import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(ignore_https_errors=True)
        page = await context.new_page()
        await page.goto("https://www.cccp13.fr/embouestV38/", timeout=30000)

        # Connexion avec tabulation
        await page.keyboard.type("013")
        await page.keyboard.press("Tab")
        await page.keyboard.type("EUROFOS")

        # Clic sur le bouton "Embauche"
        await page.locator('form[name="index"] button').first.click()

        # Attendre que le tableau soit visible
        await page.wait_for_selector("table", timeout=10000)

        # Récupérer et sauvegarder le HTML brut
        html = await page.content()
        with open("debug.html", "w") as f:
            f.write(html)

        await browser.close()

asyncio.run(run())