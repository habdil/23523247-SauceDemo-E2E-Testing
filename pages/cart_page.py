from playwright.sync_api import Page, expect


class CartPage:

    def __init__(self, page: Page, base_url: str):
        self.page     = page
        self.base_url = base_url

        self.cart_items        = page.locator(".cart_item")
        self.checkout_button   = page.locator("[data-test='checkout']")
        self.continue_shopping = page.locator("[data-test='continue-shopping']")

    # ── State checks ────────────────────────────────────────────

    def is_loaded(self) -> bool:
        expect(self.page).to_have_url(f"{self.base_url}/cart.html")
        return True

    def get_item_count(self) -> int:
        return self.cart_items.count()

    def get_item_names(self) -> list:
        return [
            self.cart_items.nth(i).locator(".inventory_item_name").inner_text()
            for i in range(self.cart_items.count())
        ]

    # ── Actions ─────────────────────────────────────────────────

    def remove_item(self, item_name: str):
        slug = item_name.lower().replace(" ", "-")
        self.page.locator(f"[data-test='remove-{slug}']").click()
        return self

    def go_to_checkout(self):
        from pages.checkout_page import CheckoutPage
        self.checkout_button.click()
        return CheckoutPage(self.page, self.base_url)

    def continue_shopping_action(self):
        from pages.inventory_page import InventoryPage
        self.continue_shopping.click()
        return InventoryPage(self.page, self.base_url)
