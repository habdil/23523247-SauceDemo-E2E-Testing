class TestCheckoutStepOne:

    def test_step_one_loads(self, checkout_page):
        assert checkout_page.is_on_step_one()

    def test_empty_form_shows_error(self, checkout_page):
        checkout_page.submit_info()

        assert checkout_page.has_error()
        assert "First Name is required" in checkout_page.get_error_message()

    def test_missing_last_name_shows_error(self, checkout_page):
        checkout_page.fill_info("John", "", "12345").submit_info()

        assert checkout_page.has_error()
        assert "Last Name is required" in checkout_page.get_error_message()

    def test_missing_postal_code_shows_error(self, checkout_page):
        checkout_page.fill_info("John", "Doe", "").submit_info()

        assert checkout_page.has_error()
        assert "Postal Code is required" in checkout_page.get_error_message()

    def test_valid_info_goes_to_step_two(self, checkout_page):
        checkout_page.fill_info("John", "Doe", "12345").submit_info()

        assert checkout_page.is_on_step_two()


class TestCheckoutStepTwo:

    def test_finish_completes_order(self, checkout_page):
        checkout_page.fill_info("John", "Doe", "12345").submit_info()
        checkout_page.finish()

        assert checkout_page.is_complete()
