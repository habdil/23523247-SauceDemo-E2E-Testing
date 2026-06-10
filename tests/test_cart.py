class TestCart:

    def test_cart_loads(self, cart_page):
        assert cart_page.is_loaded()

    def test_item_appears_in_cart(self, cart_page):
        assert cart_page.get_item_count() == 1
        assert "Sauce Labs Backpack" in cart_page.get_item_names()

    def test_remove_item_empties_cart(self, cart_page):
        cart_page.remove_item("Sauce Labs Backpack")

        assert cart_page.get_item_count() == 0

    def test_continue_shopping_goes_back(self, cart_page):
        inventory_page = cart_page.continue_shopping_action()

        assert inventory_page.is_loaded()
