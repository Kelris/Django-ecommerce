import time
from django.contrib.auth.models import User

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

# https://chromedriver.chromium.org/downloads
# browser = webdriver.Chrome("C:\Program Files (x86)\chromedriver.exe")
# browser = webdriver.Chrome(ChromeDriverManager().install())
from Ecommerce.models import Product


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        self.browser.implicitly_wait(10)
        User.objects.create_user(username='john_smith', password='test123*')

    def tearDown(self):
        self.browser.quit()

    def ecommerce_login(self):
        self.browser = webdriver.Chrome(ChromeDriverManager().install())

        self.browser.get('%s%s' % (self.live_server_url, '/users/login/'))

        self.browser.find_element_by_name("username").send_keys("john_smith")
        self.browser.find_element_by_name("password").send_keys("test123*")
        self.browser.find_element_by_name("login").click()


class TestHomePage(FunctionalTest):
    def test_social_links(self):
        browser = self.browser
        browser.get(self.live_server_url)

        WebDriverWait(browser, 10).until(                                                                               # https://selenium-python.readthedocs.io/waits.html#explicit-waits
            EC.presence_of_element_located((By.CLASS_NAME, "fa"))
        )

        social_links = browser.find_elements_by_class_name("fa")

        for link in social_links:
            link.click()

        li_tab = browser.window_handles[1]
        yt_tab = browser.window_handles[2]
        fb_tab = browser.window_handles[3]

        browser.switch_to.window(fb_tab)
        self.assertIn('Facebook', browser.title)

        browser.switch_to.window(yt_tab)
        self.assertIn('YouTube', browser.title)

        browser.switch_to.window(li_tab)
        self.assertIn('LinkedIn', browser.title)


class TestNavBarAnonymous(FunctionalTest):
    def test_navbar_links_anonymous_user(self):
        browser = self.browser
        browser.get(self.live_server_url)

        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "nav-link"))
        )

# Navbar - Home Page
        home_link = browser.find_element_by_link_text("Home")
        home_link.click()
        time.sleep(1)
        home_header = browser.find_element_by_tag_name("h1").text
        self.assertIn('Tapas Bar', home_header)

# Navbar - Store Page
        store_link = browser.find_element_by_link_text("Store")
        store_link.click()
        time.sleep(2)
        self.assertEqual(browser.current_url, ('%s%s' % (self.live_server_url, '/store/')))

# Navbar - Login Page
        login_link = browser.find_element_by_link_text("Login")
        login_link.click()
        time.sleep(2)
        self.assertEqual(browser.current_url, ('%s%s' % (self.live_server_url, '/users/login/')))

# Navbar - Register Page
        register_link = browser.find_element_by_link_text("Register")
        register_link.click()
        time.sleep(2)
        self.assertEqual(browser.current_url, ('%s%s' % (self.live_server_url, '/users/register/')))


class TestRegistrationPage(FunctionalTest):
    def test_register_page(self):
        browser = self.browser
        browser.get('%s%s' % (self.live_server_url, '/users/register/'))
        time.sleep(1)

        browser.find_element_by_link_text("Sign in").click()
        time.sleep(1)
        browser.back()

        browser.find_element_by_name("username").send_keys("john_smith2")
        browser.find_element_by_name("password1").send_keys("test123*")
        browser.find_element_by_name("password2").send_keys("test123*")
        browser.find_element_by_name("email").send_keys("jsmith@gmail.com")

        time.sleep(1)
        browser.find_element_by_name("register").click()
        time.sleep(2)

        home_header = browser.find_element_by_tag_name("h1").text
        self.assertIn('Tapas Bar', home_header)


class TestLoginPage(FunctionalTest):
    def test_login_page(self):
        browser = self.browser
        browser.get('%s%s' % (self.live_server_url, '/users/login/'))
        time.sleep(1)

        browser.find_element_by_link_text("Sign up").click()
        time.sleep(1)
        browser.back()

        browser.find_element_by_name("username").send_keys("john_smith")
        browser.find_element_by_name("password").send_keys("test123*")
        time.sleep(1)
        browser.find_element_by_name("login").click()
        time.sleep(1)

        home_header = browser.find_element_by_tag_name("h1").text
        self.assertIn('Tapas Bar', home_header)


class TestNavBarLoggedIn(FunctionalTest):
    def test_navbar_links_logged_in_user(self):
        self.ecommerce_login()

        browser = self.browser

        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "nav-link"))
        )

# Navbar - Cart Page
        cart_link = browser.find_element_by_class_name("bi-cart4")
        cart_link.click()
        time.sleep(2)
        self.assertEqual(browser.current_url, ('%s%s' % (self.live_server_url, '/checkout/')))

# Navbar - Dropdown menu (person)
        person_link = browser.find_element_by_class_name("dropdown")
        self.assertTrue(person_link)
        person_link.click()
        time.sleep(1)

# Navbar - Logout Page
        change_account_link = browser.find_element_by_link_text("Logout")
        change_account_link.click()
        time.sleep(2)
        self.assertEqual(browser.current_url, ('%s%s' % (self.live_server_url, '/users/logout/')))


# Navbar - Change account Page
        browser.get('%s%s' % (self.live_server_url, '/users/login/'))

        browser.find_element_by_name("username").send_keys("john_smith")
        browser.find_element_by_name("password").send_keys("test123*")
        time.sleep(1)
        browser.find_element_by_name("login").click()
        time.sleep(1)

        person_link = browser.find_element_by_class_name("dropdown")
        self.assertTrue(person_link)
        person_link.click()
        time.sleep(1)

        change_account_link = browser.find_element_by_link_text("Change account")
        change_account_link.click()
        time.sleep(1)
        self.assertEqual(browser.current_url, ('%s%s' % (self.live_server_url, '/users/change_account/')))


class TestStoreFunctionalityPage(FunctionalTest):
    def test_update_cart_anonymous_user(self):
        browser = self.browser
        Product.objects.create(name='Cheese', price=5)
        browser.get('%s%s' % (self.live_server_url, '/store/'))

        add_cart_btn = browser.find_element_by_name("add_btn")
        add_cart_btn.click()
        time.sleep(1)

        alert = browser.switch_to.alert

        self.assertEqual("You are not logged in.", alert.text)

        alert.accept()
        time.sleep(1)

        add_cart_btn = browser.find_element_by_name("remove_btn")
        add_cart_btn.click()
        time.sleep(1)

        alert = browser.switch_to.alert

        self.assertEqual("You are not logged in.", alert.text)

        alert.accept()
        time.sleep(1)

    def test_update_cart_logged_in_user(self):
        self.ecommerce_login()

        browser = self.browser
        Product.objects.create(name='Cheese', price=5)
        browser.get('%s%s' % (self.live_server_url, '/store/'))

        time.sleep(1)
        add_cart_btn = browser.find_element_by_name("add_btn")
        add_cart_btn.click()
        time.sleep(1)

        add_cart_btn = browser.find_element_by_name("remove_btn")
        add_cart_btn.click()
        time.sleep(2)

    def test_Cart_area_update_cart(self):
        self.ecommerce_login()

        browser = self.browser
        Product.objects.create(name='Cheese', price=5)
        browser.get('%s%s' % (self.live_server_url, '/store/'))

        time.sleep(1)
        add_cart_btn = browser.find_element_by_name("add_btn")
        add_cart_btn.click()

        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "bi-caret-up-fill"))
        )

        add_cart_arrow = browser.find_element_by_class_name("bi-caret-up-fill")
        add_cart_arrow.click()

        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "bi-caret-down-fill"))
        )

        rmv_cart_arrow = browser.find_element_by_class_name("bi-caret-down-fill")
        rmv_cart_arrow.click()
        time.sleep(2)

    def test_Cart_area_continue_btn(self):
        self.ecommerce_login()

        browser = self.browser
        Product.objects.create(name='Cheese', price=5)
        browser.get('%s%s' % (self.live_server_url, '/store/'))

        time.sleep(1)
        add_cart_btn = browser.find_element_by_name("add_btn")
        add_cart_btn.click()
        time.sleep(1)

        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Continue"))
        )

        continue_btn = browser.find_element_by_link_text("Continue")
        continue_btn.click()
        time.sleep(1)

        self.assertEqual(browser.current_url, ('%s%s' % (self.live_server_url, '/checkout/')))


class TestCheckoutPage(FunctionalTest):
    def test_checkout_valid_form(self):
        self.ecommerce_login()

        browser = self.browser
        Product.objects.create(name='Cheese', price=5)
        browser.get('%s%s' % (self.live_server_url, '/store/'))

        time.sleep(1)
        add_cart_btn = browser.find_element_by_name("add_btn")
        add_cart_btn.click()
        time.sleep(1)

        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Continue"))
        )

        continue_btn = browser.find_element_by_link_text("Continue")
        continue_btn.click()
        time.sleep(1)

        browser.find_element_by_name("address_type").send_keys("Billing")
        browser.find_element_by_name("first_name").send_keys("John")
        browser.find_element_by_name("last_name").send_keys("Smith")
        browser.find_element_by_name("address_line_1").send_keys("TestStreet")
        browser.find_element_by_name("postal_code").send_keys("123456")
        browser.find_element_by_name("city").send_keys("Washington")
        browser.find_element_by_name("country").send_keys("United States")

        time.sleep(2)

        browser.find_element_by_id("btn_confirm_order").click()

        time.sleep(2)

        self.assertIn("Choose your payment method:", browser.page_source)

