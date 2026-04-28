import pytest

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@pytest.mark.ui
def test_success_login_opens_inventory(login_page, app_settings):
    # Positive login scenario.
    login_page.login(app_settings.ui_username, app_settings.ui_password)

    inventory = InventoryPage(login_page.page, timeout_ms=app_settings.timeout_ms)
    inventory.wait_for_loaded()

    assert inventory.get_page_title() == "Products"
    assert login_page.page.url.endswith("/inventory.html")


@pytest.mark.ui
def test_invalid_login_shows_error(login_page):
    # Negative login scenario.
    login_page.login("standard_user", "wrong_password")

    error_text = login_page.get_error_text()
    assert "Epic sadface" in error_text


@pytest.mark.ui
def test_add_item_to_cart_shows_badge(inventory_page):
    # Badge should show "1" after adding an item.
    inventory_page.add_backpack_to_cart()
    assert inventory_page.get_cart_badge_value() == "1"


@pytest.mark.ui
def test_cart_contains_added_item(inventory_page, app_settings):
    # Validate basic navigation: inventory -> cart.
    inventory_page.add_backpack_to_cart()
    inventory_page.open_cart()

    cart = CartPage(inventory_page.page, timeout_ms=app_settings.timeout_ms)
    cart.wait_for_loaded()

    assert cart.get_items_count() == 1


@pytest.mark.ui
def test_logout_returns_to_login_page(inventory_page, app_settings):
    # Logout should return user to login page.
    inventory_page.logout()

    login_page = LoginPage(
        page=inventory_page.page,
        base_url=app_settings.ui_base_url,
        timeout_ms=app_settings.timeout_ms,
    )
    assert login_page.is_login_form_displayed()
    assert inventory_page.page.url.endswith("/")
