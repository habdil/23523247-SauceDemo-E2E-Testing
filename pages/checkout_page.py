from playwright.sync_api import Page, expect


class CheckoutPage:

    def __init__(self, page: Page, base_url: str):
        self.page     = page
        self.base_url = base_url

        # Step one
        self.first_name_input  = page.locator("[data-test='firstName']")
        self.last_name_input   = page.locator("[data-test='lastName']")
        self.postal_code_input = page.locator("[data-test='postalCode']")
        self.continue_button   = page.locator("[data-test='continue']")
        self.cancel_button     = page.locator("[data-test='cancel']")
        self.error_message     = page.locator("[data-test='error']")

        # Step two
        self.finish_button     = page.locator("[data-test='finish']")
        self.summary_total     = page.locator(".summary_total_label")

        # Complete
        self.complete_header   = page.locator(".complete-header")
        self.back_home_button  = page.locator("[data-test='back-to-products']")

    # ── State checks ────────────────────────────────────────────

    def is_on_step_one(self) -> bool:
        expect(self.page).to_have_url(f"{self.base_url}/checkout-step-one.html")
        return True

    def is_on_step_two(self) -> bool:
        expect(self.page).to_have_url(f"{self.base_url}/checkout-step-two.html")
        return True

    def is_complete(self) -> bool:
        expect(self.page).to_have_url(f"{self.base_url}/checkout-complete.html")
        expect(self.complete_header).to_have_text("Thank you for your order!")
        return True

    def has_error(self) -> bool:
        return self.error_message.is_visible()

    def get_error_message(self) -> str:
        return self.error_message.inner_text().strip()

    # ── Actions ─────────────────────────────────────────────────

    def fill_info(self, first_name: str, last_name: str, postal_code: str):
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)
        return self

    def submit_info(self):
        self.continue_button.click()
        return self

    def finish(self):
        self.finish_button.click()
        return self

    def cancel(self):
        from pages.inventory_page import InventoryPage
        self.cancel_button.click()
        return InventoryPage(self.page, self.base_url)
