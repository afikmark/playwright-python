from .base_page import BasePage
from framework import Page

class ShoppingCartPage(BasePage):
    URL = "cart.html"

    def __init__(self, page: Page, base_url):
        super().__init__(page, base_url)
        self.url = f'{base_url}{self.URL}'
        self.cart_items = page.locator('.cart_item')
        self.continue_shopping_button = page.get_by_role('button', name='CONTINUE SHOPPING')
        self.checkout_button = page.get_by_role('button', name='CHECKOUT')