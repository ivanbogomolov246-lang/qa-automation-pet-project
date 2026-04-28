from playwright.sync_api import Page

from pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_CONTAINER = "[data-test='error']"

    def __init__(self, page: Page, base_url: str, timeout_ms: int = 10000) -> None:
        super().__init__(page, timeout_ms)
        self.base_url = base_url.rstrip("/")

    def open(self) -> None:
        super().open(self.base_url)

    def login(self, username: str, password: str) -> None:
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_error_text(self) -> str:
        return self.get_text(self.ERROR_CONTAINER)

    def is_login_form_displayed(self) -> bool:
        self.wait_visible(self.LOGIN_BUTTON)
        return self.page.locator(self.LOGIN_BUTTON).is_visible()
