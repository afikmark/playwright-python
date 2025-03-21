from common.utils import ImageFileType
from framework import Page, Frame, Locator
from settings import ROOT_DIR


class BasePage:

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.url = base_url

    def open(self) -> None:
        """ Opens the page URL """
        self.page.goto(self.url)

    def get_frame(self, value: str) -> Frame:
        """
        get frame by value.
        e.g:
        >>> 'frame-login'
        """
        return self.page.frame(value)

    def take_screenshot(self, path: str, file_type: ImageFileType, full_page=True) -> None:
        """
        Takes screenshot of the page and stores it to path given
        if full_page is True, takes full page screenshot.
        Full page screenshot is a screenshot of a full scrollable page,
        as if you had a very tall screen and the page could fit it entirely.
        """
        screenshot_path = f'{ROOT_DIR}/{path}.{file_type}'
        self.page.screenshot(path=screenshot_path, full_page=full_page)

    @staticmethod
    def take_element_screenshot(path: str, element_locator: Locator) -> None:
        """
        Takes element screenshot
        """
        element_locator.screenshot(path=path)
