# Test Documentation — SauceDemo E2E Testing

Aplikasi yang diuji: [https://www.saucedemo.com](https://www.saucedemo.com)  
Framework: Playwright + pytest (Python)

---

## Ringkasan

| File | Jumlah Test |
|---|---|
| `tests/test_login2.py` | 7 |
| `tests/test_inventory.py` | 3 |
| `tests/test_cart.py` | 4 |
| `tests/test_checkout.py` | 6 |
| **Total** | **20** |

---

## 1. Login (`tests/test_login2.py`)

### TestLoginSuccess

| Test | Skenario | Yang Dicek |
|---|---|---|
| `test_valid_login_redirects` | Login dengan `standard_user` dan password benar | URL berpindah ke `/inventory.html` dan halaman Products tampil |

### TestLoginFailure

| Test | Skenario | Yang Dicek |
|---|---|---|
| `test_wrong_password_shows_error` | Login dengan password salah | Muncul pesan error yang mengandung "do not match" |
| `test_empty_username_shows_error` | Klik login tanpa mengisi apapun | Muncul pesan error "Username is required" |
| `test_locked_out_user_shows_error` | Login dengan `locked_out_user` (user diblokir admin) | Muncul pesan error yang mengandung "locked out" |

### TestLogout

| Test | Skenario | Yang Dicek |
|---|---|---|
| `test_logout_redirects_to_login` | Klik logout dari halaman inventory | URL kembali ke `/` (halaman login) |

### TestSpecialUsers

| Test | Skenario | Yang Dicek |
|---|---|---|
| `test_problem_user_can_login` | Login dengan `problem_user` | Berhasil masuk ke halaman inventory meskipun UI bermasalah |
| `test_problem_user_has_broken_images` | Login dengan `problem_user`, cek gambar produk | Semua gambar produk memiliki `src` yang sama (tanda gambar broken) |
| `test_performance_glitch_user_can_login` | Login dengan `performance_glitch_user` (login lambat) | Tetap berhasil masuk ke halaman inventory meskipun ada simulasi lag |

---

## 2. Inventory (`tests/test_inventory.py`)

Halaman: `/inventory.html`

| Test | Skenario | Yang Dicek |
|---|---|---|
| `test_product_count` | Buka halaman inventory | Jumlah produk yang tampil = 6 |
| `test_add_to_cart_updates_badge` | Tambah 1 produk (Sauce Labs Backpack) ke cart | Badge cart di pojok kanan atas menunjukkan angka 1 |
| `test_add_multiple_items_updates_badge` | Tambah 2 produk ke cart | Badge cart menunjukkan angka 2 |

---

## 3. Cart (`tests/test_cart.py`)

Halaman: `/cart.html`  
Precondition: sudah login dan sudah menambahkan **Sauce Labs Backpack** ke cart.

| Test | Skenario | Yang Dicek |
|---|---|---|
| `test_cart_loads` | Buka halaman cart | URL adalah `/cart.html` |
| `test_item_appears_in_cart` | Cek isi cart | Jumlah item = 1 dan nama "Sauce Labs Backpack" ada di cart |
| `test_remove_item_empties_cart` | Hapus item dari cart | Jumlah item di cart menjadi 0 |
| `test_continue_shopping_goes_back` | Klik tombol "Continue Shopping" | Kembali ke halaman inventory (`/inventory.html`) |

---

## 4. Checkout (`tests/test_checkout.py`)

Precondition: sudah login, ada item di cart, masuk ke halaman checkout.

### TestCheckoutStepOne

Halaman: `/checkout-step-one.html`

| Test | Skenario | Yang Dicek |
|---|---|---|
| `test_step_one_loads` | Masuk ke halaman checkout | URL adalah `/checkout-step-one.html` |
| `test_empty_form_shows_error` | Submit form tanpa mengisi apapun | Muncul pesan error "First Name is required" |
| `test_missing_last_name_shows_error` | Isi first name dan postal code, last name dikosongkan | Muncul pesan error "Last Name is required" |
| `test_missing_postal_code_shows_error` | Isi first name dan last name, postal code dikosongkan | Muncul pesan error "Postal Code is required" |
| `test_valid_info_goes_to_step_two` | Isi semua field dengan data valid (John / Doe / 12345) | Berpindah ke halaman `/checkout-step-two.html` |

### TestCheckoutStepTwo

Halaman: `/checkout-step-two.html`

| Test | Skenario | Yang Dicek |
|---|---|---|
| `test_finish_completes_order` | Isi data, lanjut ke step two, klik Finish | Berpindah ke `/checkout-complete.html` dan muncul teks "Thank you for your order!" |

---

## Cara Menjalankan

```bash
# Semua test
pytest --headed -v

# Per file
pytest tests/test_login2.py --headed -v
pytest tests/test_inventory.py --headed -v
pytest tests/test_cart.py --headed -v
pytest tests/test_checkout.py --headed -v

# Satu test spesifik
pytest tests/test_checkout.py::TestCheckoutStepTwo::test_finish_completes_order --headed -v
```

Screenshot otomatis tersimpan di folder `reports/` jika ada test yang gagal.
