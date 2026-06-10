from playwright.sync_api import Page, expect


class InventoryPage:

    def __init__(self, page: Page, base_url: str):
        self.page     = page
        self.base_url = base_url

        self.page_title    = page.locator(".title")
        self.burger_menu   = page.locator("#react-burger-menu-btn")
        self.logout_link   = page.locator("#logout_sidebar_link")
        self.product_items = page.locator(".inventory_item")
        self.cart_link     = page.locator(".shopping_cart_link")
        self.cart_badge    = page.locator(".shopping_cart_badge")

    # ── State checks ────────────────────────────────────────────

    def is_loaded(self) -> bool:
        expect(self.page).to_have_url(f"{self.base_url}/inventory.html")
        expect(self.page_title).to_have_text("Products")
        return True

    def get_product_count(self) -> int:
        return self.product_items.count()

    def get_cart_count(self) -> int:
        if not self.cart_badge.is_visible():
            return 0
        return int(self.cart_badge.inner_text())

    # ── Actions ─────────────────────────────────────────────────

    def add_to_cart(self, item_name: str):
        """Tambah item ke cart berdasarkan nama produk."""
        slug = item_name.lower().replace(" ", "-")
        self.page.locator(f"[data-test='add-to-cart-{slug}']").click()
        return self

    def go_to_cart(self):
        from pages.cart_page import CartPage
        self.cart_link.click()
        return CartPage(self.page, self.base_url)

    def logout(self):
        from pages.login_page import LoginPage
        self.burger_menu.click()
        self.logout_link.click()
        return LoginPage(self.page, self.base_url)
