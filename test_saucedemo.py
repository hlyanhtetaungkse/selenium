from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def login_status(driver, wait):
    username = wait.until(EC.presence_of_element_located((By.ID, "user-name")))
    password = wait.until(EC.presence_of_element_located((By.ID, "password")))

    username.clear()
    username.send_keys("standard_user")
    password.clear()
    password.send_keys("secret_sauce")

    wait.until(EC.element_to_be_clickable((By.ID, "login-button"))).click()

    try:
        wait.until(EC.url_contains("/inventory.html"))
        print("Sub testcase: Login - PASS")
        return True
    except TimeoutException:
        error_box = driver.find_elements(By.CLASS_NAME, "error-message-container")
        error_text = error_box[0].text if error_box else "Unknown login error"
        print(f"Sub testcase: Login - FAIL -> {error_text}")
        return False


def _make_driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False
    })
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.saucedemo.com/")
    driver.maximize_window()
    return driver


def test_login():
    """Standalone test for login (extracted from the previous sub-test)."""
    driver = _make_driver()
    wait = WebDriverWait(driver, 10)

    assert login_status(driver, wait), "Login process failed."

    driver.quit()


def test_checkout_partial():
    """Test the checkout flow up to the point before final order completion.
    This test performs its own login and setup so it is independent.
    It asserts that the Finish button is present on the final overview page.
    """
    driver = _make_driver()
    wait = WebDriverWait(driver, 10)

    # login
    assert login_status(driver, wait), "Login process failed."

    # add to cart
    wait.until(EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))).click()

    # go to cart
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link"))).click()

    # start checkout
    wait.until(EC.element_to_be_clickable((By.ID, "checkout"))).click()

    # fill buyer info and continue
    wait.until(EC.presence_of_element_located((By.ID, "first-name"))).send_keys("John")
    wait.until(EC.presence_of_element_located((By.ID, "last-name"))).send_keys("Doe")
    wait.until(EC.presence_of_element_located((By.ID, "postal-code"))).send_keys("12345")

    wait.until(EC.element_to_be_clickable((By.ID, "continue"))).click()

    # assert the Finish button is present on the overview page
    finish_btn = wait.until(EC.presence_of_element_located((By.ID, "finish")))
    assert finish_btn is not None, "Finish button not present after filling checkout info"

    driver.quit()


def test_order_complete():
    """Complete the full order flow and assert the completion message.
    This is an independent test that performs its own login and checkout steps.
    """
    driver = _make_driver()
    wait = WebDriverWait(driver, 10)

    # login
    assert login_status(driver, wait), "Login process failed."

    # add to cart
    wait.until(EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))).click()

    # go to cart
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link"))).click()

    # start checkout
    wait.until(EC.element_to_be_clickable((By.ID, "checkout"))).click()

    # fill buyer info and continue
    wait.until(EC.presence_of_element_located((By.ID, "first-name"))).send_keys("John")
    wait.until(EC.presence_of_element_located((By.ID, "last-name"))).send_keys("Doe")
    wait.until(EC.presence_of_element_located((By.ID, "postal-code"))).send_keys("12345")

    wait.until(EC.element_to_be_clickable((By.ID, "continue"))).click()
    wait.until(EC.element_to_be_clickable((By.ID, "finish"))).click()

    # assertion
    complete_header = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "complete-header")))
    actual_text = complete_header.text
    expected_text = "Thank you for your order!"

    assert actual_text == expected_text, "Test Failed: Text does not match"
    print("🟢 Test Passed: " + actual_text)

    driver.quit()
