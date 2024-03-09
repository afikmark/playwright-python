from framework import Page


class BasePage:

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.url = base_url

    @property
    def is_in_page(self) -> bool:
        """ Validates the browser is on the current page """
        current_url = self.page.url
        return current_url == self.url

    def open(self) -> None:
        """ Opens the page URL """
        self.page.goto(self.url)
