import pytest
from playwright.sync_api import Page, sync_playwright
from framework.web_browser import BrowserType
from framework.web_pages.swag_labs.swag_labs import SwagLabs
from framework.logger import get_logger
from tests.config import Config
import json
import os

logger = get_logger()


@pytest.hookimpl
def pytest_runtest_setup(item):
    test_capture_path = f'{item.path.parent}/test_capture'
    os.makedirs(test_capture_path, exist_ok=True)
    item.config.cache.set("test_capture_path", test_capture_path)


@pytest.fixture(scope="function")
def test_capture_path(request) -> str:
    """Returns the test capture path"""
    return request.config.cache.get("test_capture_path", None)


@pytest.fixture(scope="function")
def page(browser_type, test_capture_path, **kwargs):
    with sync_playwright() as playwright:
        match browser_type:
            case BrowserType.FIREFOX:
                browser = playwright.firefox.launch(**kwargs)
            case _:
                browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(record_video_dir=test_capture_path)
        yield context.new_page()


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
    logger.info('Test information including params:{}'.format(json.dumps(test_info, indent=2)))
