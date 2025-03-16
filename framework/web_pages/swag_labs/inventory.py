from .base_page import BasePage
from framework import Page


class InventoryItems:
    BACKPACK = 'Backpack'
    BIKE_LIGHT = 'Bike Light'
    BOLT_T_SHIRT = 'Bolt T-Shirt'
    FLEECE_JACKET = 'Fleece Jacket',
    ONESIE = 'Onesie'


class InventoryPage(BasePage):
    URL = "inventory.html"

    def __init__(self, page: Page, base_url):
        super().__init__(page, base_url)
        self.url = f'{base_url}{self.URL}'
        self.inventory_items = page.locator('.inventory_item')
