import pathlib
import allure
import pytest
from allure_commons.types import AttachmentType
from playwright.sync_api import Page, sync_playwright
from pytest_playwright.pytest_playwright import output_path, launch_browser

from common.utils import ImageFileType, retry_on_false
from framework.web_browser import BrowserType
from framework.web_pages.swag_labs.swag_labs import SwagLabs
from framework.logger import get_logger
from framework.reporter import AllureReporter
from settings import ROOT_DIR
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
        node_id_parts = item.nodeid.split("/")
        file_path = f'{node_id_parts[0]}-{node_id_parts[1]}'
        test_name_parts = node_id_parts[2].split("::")
        test_name = f'{test_name_parts[0].replace(".", "-")}-{test_name_parts[1]}'
        artifacts_dir = pathlib.Path(ROOT_DIR, 'tests/test-results', f'{file_path}-{test_name.replace('_', '-')}')
        if artifacts_dir.is_dir():
            for file in artifacts_dir.iterdir():
                # Find the video/PNG file and attach it to Allure Report
                if file.is_file() and file.suffix == ".webm":
                    allure.attach.file(
                        file,
                        name=file.name,
                        attachment_type=allure.attachment_type.WEBM,
                    )
                elif file.suffix == ".png":
                    allure.attach.file(
                        file,
                        name=file.name,
                        attachment_type=allure.attachment_type.PNG)

    except Exception as e:
        print(f"Error attaching video: {e}")


@pytest.fixture(scope="function")
def page(page: Page):
    page.goto("https://www.saucedemo.com/")
    yield page


@pytest.fixture(scope="function")
def swag_ui(page: Page, app_config):
    return SwagLabs(page, app_config.base_url)


@pytest.fixture(scope='session')
def env(request):
    return request.config.getoption("--env")


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


def pytest_collection_modifyitems(items):
    test_info = {
        item.nodeid.split("::")[1]: item.function.__doc__
        for item in items
    }
    logger.info('Test information including params:{}'.format(json.dumps(test_info, indent=2)))
