import pytest
from playwright.sync_api import Page

BASE_URL   = "https://www.saucedemo.com"
VALID_USER = "standard_user"
VALID_PASS = "secret_sauce"


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
    }


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        # "headless": True,   # uncomment untuk CI/CD
        "slow_mo": 400,       # delay 400ms — mudah diikuti saat demo
    }


@pytest.fixture
def login_page(page: Page):
    """Buka halaman login, return LoginPage."""
    from pages.login_page import LoginPage
    lp = LoginPage(page, BASE_URL)
    lp.navigate()
    return lp


@pytest.fixture
def authenticated_page(page: Page):
    """Sudah login sebagai standard_user, return InventoryPage."""
    from pages.login_page import LoginPage
    lp = LoginPage(page, BASE_URL)
    lp.navigate()
    return lp.login(VALID_USER, VALID_PASS)


@pytest.fixture
def cart_page(page: Page):
    """Sudah login dan sudah add 1 item (Sauce Labs Backpack), return CartPage."""
    from pages.login_page import LoginPage
    lp = LoginPage(page, BASE_URL)
    lp.navigate()
    inventory = lp.login(VALID_USER, VALID_PASS)
    inventory.add_to_cart("Sauce Labs Backpack")
    return inventory.go_to_cart()


@pytest.fixture
def checkout_page(page: Page):
    """Sudah login, add item, masuk cart, lalu ke checkout step one, return CheckoutPage."""
    from pages.login_page import LoginPage
    lp = LoginPage(page, BASE_URL)
    lp.navigate()
    inventory = lp.login(VALID_USER, VALID_PASS)
    inventory.add_to_cart("Sauce Labs Backpack")
    cart = inventory.go_to_cart()
    return cart.go_to_checkout()
