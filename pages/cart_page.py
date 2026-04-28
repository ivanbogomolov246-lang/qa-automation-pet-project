from playwright.sync_api import Page

from pages.base_page import BasePage


class CartPage(BasePage):
    TITLE = ".title"
    CART_ITEMS = ".cart_item"
    CONTINUE_SHOPPING_BUTTON = "#continue-shopping"

    def __init__(self, page: Page, timeout_ms: int = 10000) -> None:
        super().__init__(page, timeout_ms)

    def wait_for_loaded(self) -> None:
        self.page.wait_for_url("**/cart.html", timeout=self.timeout_ms)
        self.wait_visible(self.TITLE)

    def get_items_count(self) -> int:
        return self.page.locator(self.CART_ITEMS).count()

    def continue_shopping(self) -> None:
        self.click(self.CONTINUE_SHOPPING_BUTTON)
        self.page.wait_for_url("**/inventory.html", timeout=self.timeout_ms)
