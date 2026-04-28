from playwright.sync_api import Page

from pages.base_page import BasePage


class InventoryPage(BasePage):
    TITLE = ".title"
    CART_LINK = ".shopping_cart_link"
    CART_BADGE = ".shopping_cart_badge"
    ADD_BACKPACK_BUTTON = "#add-to-cart-sauce-labs-backpack"
    BURGER_MENU_BUTTON = "#react-burger-menu-btn"
    LOGOUT_LINK = "#logout_sidebar_link"

    def __init__(self, page: Page, timeout_ms: int = 10000) -> None:
        super().__init__(page, timeout_ms)

    def wait_for_loaded(self) -> None:
        self.page.wait_for_url("**/inventory.html", timeout=self.timeout_ms)
        self.wait_visible(self.TITLE)

    def get_page_title(self) -> str:
        return self.get_text(self.TITLE)

    def add_backpack_to_cart(self) -> None:
        self.click(self.ADD_BACKPACK_BUTTON)

    def get_cart_badge_value(self) -> str:
        badge = self.page.locator(self.CART_BADGE)
        if badge.count() == 0:
            return "0"
        return badge.inner_text()

    def open_cart(self) -> None:
        self.click(self.CART_LINK)
        self.page.wait_for_url("**/cart.html", timeout=self.timeout_ms)

    def open_menu(self) -> None:
        self.click(self.BURGER_MENU_BUTTON)
        self.wait_visible(self.LOGOUT_LINK)

    def logout(self) -> None:
        self.open_menu()
        self.click(self.LOGOUT_LINK)
        self.page.wait_for_url("**/", timeout=self.timeout_ms)
