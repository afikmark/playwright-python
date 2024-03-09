import pytest
from playwright.sync_api import Page, sync_playwright
from framework.web_browser import BrowserType
from framework.web_pages.swag_labs.swag_labs import SwagLabs
from framework.logger import get_logger
from tests.config import Config
import json

logger = get_logger()


@pytest.fixture(scope="function")
def page(browser_type, **kwargs):
    with sync_playwright() as playwright:
        match browser_type:
            case BrowserType.FIREFOX:
                browser = playwright.firefox.launch(**kwargs)
            case _:
                browser = playwright.chromium.launch(headless=False)
        yield browser.new_page()


@pytest.fixture(scope="function")
def swag_ui(page: Page, app_config):
    return SwagLabs(page, app_config.base_url)


@pytest.fixture(scope='session')
def env(request):
    return request.config.getoption("--env")


@pytest.fixture(scope='session')
def browser_type(request):
    return request.config.getoption("--browser_type")


@pytest.fixture(scope='session')
def app_config(env):
    cfg = Config(env)
    return cfg


def pytest_addoption(parser):
    parser.addoption("--env",
                     action="store",
                     help="Environment to run tests",
                     default="qa"
                     )
    parser.addoption("--browser_type",
                     action="store",
                     help="Browser type for UI testing",
                     default='chrome')


def pytest_collection_modifyitems(items):
    test_info = {
        item.nodeid.split("::")[1]: item.function.__doc__
        for item in items
    }
    logger.info('Test information including params:\n{}'.format(json.dumps(test_info, indent=2)))
