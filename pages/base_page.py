from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page, timeout_ms: int = 10000) -> None:
        self.page = page
        self.timeout_ms = timeout_ms

    def open(self, url: str) -> None:
        self.page.goto(url, wait_until="domcontentloaded", timeout=self.timeout_ms)

    def wait_visible(self, selector: str) -> None:
        self.page.locator(selector).wait_for(state="visible", timeout=self.timeout_ms)

    def click(self, selector: str) -> None:
        self.wait_visible(selector)
        self.page.locator(selector).click()

    def fill(self, selector: str, value: str) -> None:
        self.wait_visible(selector)
        self.page.locator(selector).fill(value)

    def get_text(self, selector: str) -> str:
        self.wait_visible(selector)
        return self.page.locator(selector).inner_text()
