import pytest

from api.api_client import ApiClient
from config.settings import settings
from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.logger import configure_logging


def pytest_configure() -> None:
    # Enable one log format for all tests.
    configure_logging()


@pytest.fixture(scope="session")
def app_settings():
    return settings


@pytest.fixture(scope="session")
def api_client(app_settings):
    # One HTTP client for the whole test session.
    client = ApiClient(base_url=app_settings.api_base_url)
    yield client
    client.close()


@pytest.fixture(scope="session")
def browser_type_launch_args(app_settings):
    # Keep UI tests visible and make Chromium launch more stable in VS Code Testing.
    return {
        "headless": app_settings.ui_headless,
        "slow_mo": app_settings.ui_slowmo_ms,
        "args": [
            "--disable-gpu",
            "--disable-dev-shm-usage",
            "--disable-software-rasterizer",
        ],
    }


@pytest.fixture
def browser(browser_type, browser_type_launch_args):
    # Start a fresh browser for each UI test to reduce cross-test crashes.
    browser_instance = browser_type.launch(**browser_type_launch_args)
    yield browser_instance
    browser_instance.close()


@pytest.fixture
def login_page(page, app_settings):
    # Fixture that opens only the login page.
    page.set_default_timeout(app_settings.timeout_ms)
    login = LoginPage(
        page=page,
        base_url=app_settings.ui_base_url,
        timeout_ms=app_settings.timeout_ms,
    )
    login.open()
    return login


@pytest.fixture
def inventory_page(page, app_settings):
    # Fixture that logs in and returns the inventory page.
    page.set_default_timeout(app_settings.timeout_ms)
    login = LoginPage(
        page=page,
        base_url=app_settings.ui_base_url,
        timeout_ms=app_settings.timeout_ms,
    )
    login.open()
    login.login(app_settings.ui_username, app_settings.ui_password)
    inventory = InventoryPage(page=page, timeout_ms=app_settings.timeout_ms)
    inventory.wait_for_loaded()
    return inventory


@pytest.fixture
def cart_page(inventory_page, app_settings):
    inventory_page.open_cart()
    cart = CartPage(page=inventory_page.page, timeout_ms=app_settings.timeout_ms)
    cart.wait_for_loaded()
    return cart
