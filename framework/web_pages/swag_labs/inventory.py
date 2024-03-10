from settings import ROOT_DIR
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
        self.inventory_items = InventoryItems()
        self.current_item_name = self.inventory_items.BACKPACK
        self.item_locator = self.page.get_by_text(f'Sauce Labs {self.current_item_name}')
        self.formatted_item_name = self.current_item_name.lower().replace(" ", "-")

    @property
    def item(self):
        return self.item_locator

    @item.setter
    def item(self, value):
        self.current_item_name = value
        self.item_locator = self.page.locator('.inventory_list >.inventory_item').filter(
            has_text=f'Sauce Labs {self.current_item_name}')

    @property
    def add_to_cart_button(self):
        return self.page.locator(f'#add-to-cart-sauce-labs-{self.formatted_item_name}')

    @property
    def remove_from_cart_btn(self):
        return self.page.locator(f'#remove-sauce-labs-{self.formatted_item_name}')

    def record(self):
        self.page.close()
        self.page.video.save_as(f'{ROOT_DIR}/videos')
