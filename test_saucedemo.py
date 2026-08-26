# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time

# # 1. Chrome Browser ဖွင့်၍ Website သို့ သွားခြင်း 🌐
# def test_saucedemo_e2e():
#     options = webdriver.ChromeOptions()
#     options.add_experimental_option("prefs", {
#         "credentials_enable_service": False,
#         "profile.password_manager_enabled": False,
#         "profile.password_manager_leak_detection": False
#     })
#     driver = webdriver.Chrome(options=options)
#     driver.get("https://www.saucedemo.com/")
#     driver.maximize_window()

#     # 2. Login အချက်အလက်များ အလိုအလျောက် ဖြည့်ခြင်း 🔑
#     driver.find_element(By.ID, "user-name").send_keys("standard_user")
#     driver.find_element(By.ID, "password").send_keys("secret_sauce")

# # 3. Login Button ကို နှိပ်ခြင်း 🖱️
#     driver.find_element(By.ID, "login-button").click()
#     time.sleep(2)

#     driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
#     time.sleep(2)

#     driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
#     time.sleep(2)

#     driver.find_element(By.ID, "checkout").click()
#     time.sleep(2)

#     driver.find_element(By.ID, "first-name").send_keys("John")
#     driver.find_element(By.ID, "last-name").send_keys("Doe")
#     driver.find_element(By.ID, "postal-code").send_keys("12345")
#     time.sleep(2)
#     driver.find_element(By.ID, "continue").click()
#     time.sleep(2)
#     driver.find_element(By.ID, "finish").click()
#     time.sleep(2)

#     # complete_header = driver.find_element(By.CLASS_NAME, "complete-header")
#     # print(complete_header.text)
#     # print(driver.find_element(By.CLASS_NAME, "complete-header").text)
#     # ၁။ လက်တွေ့ ရရှိသည့် စာသားကို ယူခြင်း
#     actual_text = driver.find_element(By.CLASS_NAME, "complete-header").text

#     # ၂။ စစ်ဆေးလိုသည့် မျှော်လင့်ထားသော စာသား
#     expected_text = "Thank you for your order!"

#     assert actual_text == expected_text, "Test Failed: Text does not match"
#     print("🟢 Test Passed: " + actual_text)
#     # # 4. ရလဒ် စောင့်ကြည့်၍ Browser ပိတ်ခြင်း ⏱️
#     # time.sleep(5)
#     # driver.quit()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_saucedemo_e2e():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False
    })
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.saucedemo.com/")
    driver.maximize_window()

    # ⏱️ Explicit Wait Object ပြင်ဆင်ခြင်း (အများဆုံး ၁၀ စက္ကန့် စောင့်ဆိုင်းရန်)
    wait = WebDriverWait(driver, 10)

    # 🔑 ၁။ Login ဝင်ခြင်း
    wait.until(EC.presence_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
    wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys("secret_sauce")
    wait.until(EC.element_to_be_clickable((By.ID, "login-button"))).click()

    # 🎒 ၂။ Cart ထဲ ပစ္စည်း ထည့်ခြင်း
    wait.until(EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))).click()

    # 🛒 ၃။ Cart Page ထဲသို့ ဝင်ရောက်ခြင်း
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link"))).click()

    # 💳 ၄။ Checkout စတင်ခြင်း
    wait.until(EC.element_to_be_clickable((By.ID, "checkout"))).click()

    # 📝 ၅။ ဝယ်ယူသူ အချက်အလက်များ ဖြည့်သွင်းခြင်း
    wait.until(EC.presence_of_element_located((By.ID, "first-name"))).send_keys("John")
    wait.until(EC.presence_of_element_located((By.ID, "last-name"))).send_keys("Doe")
    wait.until(EC.presence_of_element_located((By.ID, "postal-code"))).send_keys("12345")
    
    wait.until(EC.element_to_be_clickable((By.ID, "continue"))).click()
    wait.until(EC.element_to_be_clickable((By.ID, "finish"))).click()

    # 🧪 ၆။ ရလဒ် စစ်ဆေးခြင်း (Assertion)
    complete_header = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "complete-header")))
    actual_text = complete_header.text
    expected_text = "Thank you your order!"

    assert actual_text == expected_text, "Test Failed: Text does not match"
    print("🟢 Test Passed: " + actual_text)

    driver.quit()