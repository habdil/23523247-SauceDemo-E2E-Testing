from playwright.sync_api import Page, expect


class LoginPage:

    def __init__(self, page: Page, base_url: str):
        self.page     = page
        self.base_url = base_url

        # Locators — semua element login ada di sini
        # Kalau SauceDemo update HTML, cukup edit file ini
        self.username_input = page.locator("[data-test='username']")
        self.password_input = page.locator("[data-test='password']")
        self.login_button   = page.locator("[data-test='login-button']")
        self.error_message  = page.locator("[data-test='error']")

    # ── Navigation ──────────────────────────────────────────────

    def navigate(self):
        self.page.goto(f"{self.base_url}/")
        expect(self.login_button).to_be_visible()
        return self

    # ── Actions ─────────────────────────────────────────────────

    def fill_username(self, username: str):
        self.username_input.fill(username)
        return self  # method chaining

    def fill_password(self, password: str):
        self.password_input.fill(password)
        return self

    def click_login(self):
        self.login_button.click()
        return self

    def login(self, username: str, password: str):
        """
        Happy path: isi form dan submit.
        Return InventoryPage (halaman setelah login berhasil).
        """
        from pages.inventory_page import InventoryPage
        self.fill_username(username)
        self.fill_password(password)
        self.click_login()
        return InventoryPage(self.page, self.base_url)

    # ── Assertions helper ───────────────────────────────────────

    def get_error_message(self) -> str:
        return self.error_message.inner_text().strip()

    def has_error(self) -> bool:
        return self.error_message.is_visible()

    def is_on_login_page(self) -> bool:
        return self.page.url == f"{self.base_url}/"
