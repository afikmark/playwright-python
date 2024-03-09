from playwright.sync_api import sync_playwright, Browser


class BrowserType:
    CHROME: str = 'chrome'
    FIREFOX: str = 'firefox'


def _create_browser(browser_type: str, **kwargs) -> Browser:
    match browser_type:
        case BrowserType.FIREFOX:
            browser = sync_playwright().start().firefox.launch(**kwargs)
        case _:
            browser = sync_playwright().start().chromium.launch(**kwargs)

    return browser


class WebBrowser:
    def __init__(self, browser_type: str, **kwargs):
        self.browser = _create_browser(browser_type, **kwargs)
        self.page = self.browser.new_context().new_page()

    def close_browser(self) -> None:
        self.browser.close()
