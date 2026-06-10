class TestInventory:

    def test_product_count(self, authenticated_page):
        assert authenticated_page.get_product_count() == 6

    def test_add_to_cart_updates_badge(self, authenticated_page):
        authenticated_page.add_to_cart("Sauce Labs Backpack")

        assert authenticated_page.get_cart_count() == 1

    def test_add_multiple_items_updates_badge(self, authenticated_page):
        authenticated_page.add_to_cart("Sauce Labs Backpack")
        authenticated_page.add_to_cart("Sauce Labs Bike Light")

        assert authenticated_page.get_cart_count() == 2
