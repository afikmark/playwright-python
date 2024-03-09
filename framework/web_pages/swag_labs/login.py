from .base_page import BasePage
from framework import Page


class LoginPage(BasePage):
    USER_NAME_SELECTOR = '#user-name'
    PASSWORD_SELECTOR = '#password'
    LOGIN_BUTTON_SELECTOR = '[data-test="login-button"]'

    def __init__(self, page: Page, base_url):
        super().__init__(page, base_url)
        self.url = base_url
        self.user_name_input = self.page.locator(self.USER_NAME_SELECTOR)
        self.password_input = self.page.locator(self.PASSWORD_SELECTOR)
        self.login_button = self.page.locator(self.LOGIN_BUTTON_SELECTOR)

    def login(self, user_name: str, password: str) -> None:
        """ fill username and password and submit the login button """
        self.user_name_input.fill(user_name)
        self.password_input.fill(password)
        self.login_button.click()
