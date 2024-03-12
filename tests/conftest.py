import time
import shutil
import pytest
from playwright.sync_api import Page, sync_playwright
from common.utils import ImageFileType, retry_on_false
from framework.web_browser import BrowserType
from framework.web_pages.swag_labs.swag_labs import SwagLabs
from framework.logger import get_logger
from framework.reporter import AllureReporter
from tests.config import Config
import json
import os

logger = get_logger()


@pytest.hookimpl
def pytest_runtest_setup(item):
    test_capture_path = fr'{item.path.parent}\test_capture'
    test_screenshot_capture_path = fr'{item.path.parent}\test_capture_screenshot'
    os.makedirs(test_capture_path, exist_ok=True)
    os.makedirs(test_screenshot_capture_path, exist_ok=True)
    item.config.cache.set("test_capture_path", test_capture_path)
    item.config.cache.set("test_capture_screenshot", test_screenshot_capture_path)


@pytest.fixture
def reporter():
    return AllureReporter()


@pytest.fixture(scope="function")
def test_capture_path(request) -> tuple:
    """Returns the test capture path"""
    return (request.config.cache.get("test_capture_path", None),
            request.config.cache.get("test_capture_screenshot", None))


@pytest.fixture(scope="function", autouse=True)
def attach_evidence(request, page: Page, test_capture_path, reporter):
    yield  # Allow the test to run
    screenshot_path = fr'{test_capture_path[1]}\{request.node.name}.{ImageFileType.PNG}'
    video_name = os.listdir(test_capture_path[0])[-1]
    video_path = fr'{test_capture_path[0]}\{video_name}'
    if request.node.session.testsfailed > 0:
        try:
            page.screenshot(path=screenshot_path, full_page=True)
            reporter.attach_img(screenshot=screenshot_path)
            page.close(reason="capture video")
            wait_for_page_to_close(page)  # wait for page to close
            reporter.attach_file(file=video_path, name="Video")
        except FileNotFoundError:
            logger.info("No screenshot or videos to attach")
        except PermissionError as e:
            logger.error(e)
    try:
        shutil.rmtree(test_capture_path[0])
        shutil.rmtree(test_capture_path[1])
    except Exception as e:
        logger.error(e)


@retry_on_false()
def wait_for_page_to_close(page: Page) -> bool:
    time.sleep(5)
    return page.is_closed()


@pytest.fixture(scope="function")
def page(browser_type, test_capture_path, launch_options):
    with sync_playwright() as playwright:
        match browser_type:
            case BrowserType.FIREFOX:
                browser = playwright.firefox.launch(**launch_options)
            case _:
                browser = playwright.chromium.launch(**launch_options)
        context = browser.new_context(
            record_video_dir=test_capture_path[0])  # todo: add video capture options to configuration file
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


@pytest.fixture(scope="session")
def launch_options(app_config):
    return app_config.launch_options


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

    parser.addoption("--allurdir",
                     action="store",
                     help="allure results directory",
                     default="allure-results")


def pytest_collection_modifyitems(items):
    test_info = {
        item.nodeid.split("::")[1]: item.function.__doc__
        for item in items
    }
    logger.info('Test information including params:{}'.format(json.dumps(test_info, indent=2)))
