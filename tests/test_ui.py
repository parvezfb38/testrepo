"""
Selenium UI tests for the Mini E-Commerce app.
Requires the app to be running at http://localhost:8000
Run with: pytest tests/test_ui.py
"""
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# localhostUrl
BASE_URL = "http://localhost:8000"

@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    drv = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    drv.implicitly_wait(5)
    yield drv
    drv.quit()

def wait_toast(driver, text_fragment):
    WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element((By.ID, "toast"), text_fragment)
    )

# ── Users Configuration ──────────────────────────────────────────────────────────────────────

def test_page_loads(driver):
    driver.get(BASE_URL)
    assert "Mini E-Commerce" in driver.title

def test_create_user(driver):
    driver.get(BASE_URL)
    driver.find_element(By.ID, "user-name").send_keys("Alice")
    driver.find_element(By.ID, "user-email").send_keys("alice@example.com")
    driver.find_element(By.CSS_SELECTOR, "#user-form button").click()
    wait_toast(driver, "User created")
    table = driver.find_element(By.ID, "users-table").text
    assert "Alice" in table

def test_delete_user(driver):
    driver.get(BASE_URL)
    # Create a user to delete
    driver.find_element(By.ID, "user-name").send_keys("ToDelete")
    driver.find_element(By.ID, "user-email").send_keys("todelete@example.com")
    driver.find_element(By.CSS_SELECTOR, "#user-form button").click()
    wait_toast(driver, "User created")

    # Delete the last delete button
    del_buttons = driver.find_elements(By.CSS_SELECTOR, "#users-table .btn-del")
    del_buttons[-1].click()
    wait_toast(driver, "User deleted")

# ── Products ───────────────────────────────────────────────────────────────────

def test_create_product(driver):
    driver.get(BASE_URL)
    driver.find_element(By.ID, "tab-products").click()
    WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.ID, "product-name")))

    driver.find_element(By.ID, "product-name").send_keys("Widget")
    driver.find_element(By.ID, "product-desc").send_keys("A nice widget")
    driver.find_element(By.ID, "product-price").send_keys("9.99")
    driver.find_element(By.ID, "product-stock").send_keys("100")
    driver.find_element(By.CSS_SELECTOR, "#product-form button").click()
    wait_toast(driver, "Product created")
    table = driver.find_element(By.ID, "products-table").text
    assert "Widget" in table

def test_delete_product(driver):
    driver.get(BASE_URL)
    driver.find_element(By.ID, "tab-products").click()
    WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.ID, "product-name")))

    driver.find_element(By.ID, "product-name").send_keys("Temp Product")
    driver.find_element(By.ID, "product-price").send_keys("1.00")
    driver.find_element(By.ID, "product-stock").send_keys("10")
    driver.find_element(By.CSS_SELECTOR, "#product-form button").click()
    wait_toast(driver, "Product created")

    del_buttons = driver.find_elements(By.CSS_SELECTOR, "#products-table .btn-del")
    del_buttons[-1].click()
    wait_toast(driver, "Product deleted")

# ── Orders ─────────────────────────────────────────────────────────────────────

def test_create_order(driver):
    """Assumes user ID 1 and product ID 1 exist from previous tests."""
    driver.get(BASE_URL)
    driver.find_element(By.ID, "tab-orders").click()
    WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.ID, "order-user-id")))

    driver.find_element(By.ID, "order-user-id").send_keys("1")
    driver.find_element(By.ID, "order-product-id").send_keys("1")
    driver.find_element(By.ID, "order-quantity").send_keys("2")
    driver.find_element(By.CSS_SELECTOR, "#order-form button").click()
    wait_toast(driver, "Order placed")
    table = driver.find_element(By.ID, "orders-table").text
    assert "P1 x2" in table

def test_delete_order(driver):
    driver.get(BASE_URL)
    driver.find_element(By.ID, "tab-orders").click()
    WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.ID, "order-user-id")))

    del_buttons = driver.find_elements(By.CSS_SELECTOR, "#orders-table .btn-del")
    if del_buttons:
        del_buttons[-1].click()
        wait_toast(driver, "Order deleted")
