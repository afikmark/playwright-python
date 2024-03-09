from .login import LoginPage
from .inventory import InventoryPage
from framework import Page
from .web_flows.swag_web_flows import SwagFlows


class SwagLabs:

    def __init__(self, page: Page, base_url: str):
        self.url = base_url
        self.login_page = LoginPage(page, self.url)
        self.inventory_page = InventoryPage(page, self.url)
        self.flows = SwagFlows()
