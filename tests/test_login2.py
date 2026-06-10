from playwright.sync_api import expect

BASE_URL = "https://www.saucedemo.com"


class TestLoginSuccess:

    def test_valid_login_redirects(self, login_page):
        inventory_page = login_page.login("standard_user", "secret_sauce")

        inventory_page.is_loaded()


class TestLoginFailure:

    def test_wrong_password_shows_error(self, login_page):
        login_page.login("standard_user", "wrongpassword")

        assert login_page.has_error()
        assert "do not match" in login_page.get_error_message()

    def test_empty_username_shows_error(self, login_page):
        login_page.click_login()

        assert login_page.has_error()
        assert "Username is required" in login_page.get_error_message()

    def test_locked_out_user_shows_error(self, login_page):
        """User yang diblokir admin tidak bisa login."""
        login_page.login("locked_out_user", "secret_sauce")

        assert login_page.has_error()
        assert "locked out" in login_page.get_error_message()


class TestLogout:

    def test_logout_redirects_to_login(self, authenticated_page):
        """Setelah logout, URL harus kembali ke halaman login."""
        login_page = authenticated_page.logout()

        expect(login_page.page).to_have_url(f"{BASE_URL}/")


class TestSpecialUsers:

    def test_problem_user_can_login(self, login_page):
        """problem_user bisa login tapi UI-nya bermasalah (gambar salah)."""
        inventory_page = login_page.login("problem_user", "secret_sauce")

        inventory_page.is_loaded()

    def test_problem_user_has_broken_images(self, login_page):
        """Gambar produk pada problem_user seharusnya broken (src sama semua)."""
        inventory_page = login_page.login("problem_user", "secret_sauce")
        inventory_page.is_loaded()

        images = inventory_page.page.locator(".inventory_item img").all()
        srcs = [img.get_attribute("src") for img in images]

        # Semua gambar punya src yang sama — tanda UI bermasalah
        assert len(set(srcs)) == 1, f"Expected all images broken (same src), got: {set(srcs)}"

    def test_performance_glitch_user_can_login(self, login_page):
        """performance_glitch_user bisa login meski lambat (simulasi lag)."""
        inventory_page = login_page.login("performance_glitch_user", "secret_sauce")

        inventory_page.is_loaded()