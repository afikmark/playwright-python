import pathlib
import allure
import pytest
from allure_commons.types import AttachmentType
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


@pytest.fixture
def reporter():
    return AllureReporter()


# Write a hook that creates a capture folder if the test fails

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_teardown(item, nextitem):
    yield

    try:
        # Get the output directory for the test
        artifacts_dir = item.path.parent
        if artifacts_dir:
            artifacts_dir_path = pathlib.Path(artifacts_dir).joinpath('videos')


            if artifacts_dir_path.is_dir():
                for file in artifacts_dir_path.iterdir():
                    # Find the video file and attach it to Allure Report
                    if file.is_file() and file.suffix == ".webm":
                        allure.attach.file(
                            file,
                            name=file.name,
                            attachment_type=allure.attachment_type.WEBM,
                        )

    except Exception as e:
        print(f"Error attaching video: {e}")



@pytest.fixture(scope="function")
def page(browser_type, launch_options):
    with sync_playwright() as playwright:
        match browser_type:
            case BrowserType.FIREFOX:
                browser = playwright.firefox.launch(**launch_options)
            case _:
                browser = playwright.chromium.launch(**launch_options)
        context = browser.new_context(record_video_dir='videos')
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
