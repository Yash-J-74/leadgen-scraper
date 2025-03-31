import asyncio
import sys
from typing import Optional
from playwright.async_api import async_playwright, Browser, Page, Playwright
from contextlib import asynccontextmanager

class PlaywrightManager:
    """A manager class for Playwright browser sessions."""
    
    DEFAULT_HEADERS = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/115.0.0.0 Safari/537.36'
    }
    
    def __init__(self, headless: bool = True, headers: Optional[dict] = None):
        """
        Initialize PlaywrightManager.
        
        Args:
            headless (bool): Whether to run browser in headless mode
            headers (dict, optional): Custom headers to use for requests
        """
        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        self.headless = headless
        self.headers = headers or self.DEFAULT_HEADERS
        self._playwright: Optional[Playwright] = None
        self._browser: Optional[Browser] = None
        
    async def __aenter__(self) -> Page:
        """Async context manager entry."""
        return await self.create_page()
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.cleanup()
    
    @asynccontextmanager
    async def get_page(self):
        """Context manager for getting a page instance."""
        page = await self.create_page()
        try:
            yield page
        finally:
            await self.cleanup()
    
    async def create_page(self) -> Page:
        """Create and return a new page instance."""
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(headless=self.headless)
        context = await self._browser.new_context()
        page = await context.new_page()
        await page.set_extra_http_headers(self.headers)
        return page
    
    async def cleanup(self):
        """Clean up Playwright resources."""
        if self._browser:
            await self._browser.close()
            self._browser = None
        if self._playwright:
            await self._playwright.stop()
            self._playwright = None