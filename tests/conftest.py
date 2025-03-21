import pathlib
import allure
import pytest
from playwright.sync_api import Page, Playwright
from framework.web_pages.swag_labs.swag_labs import SwagLabs
from framework.logger import get_logger
from framework.reporter import AllureReporter
from settings import ROOT_DIR
from tests.config import Config

logger = get_logger()


@pytest.fixture
def reporter():
    return AllureReporter()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_teardown(item):
    yield

    try:
        # Get the output directory for the test
        node_id_parts = item.nodeid.split("/")
        file_path = f'{node_id_parts[0]}-{node_id_parts[1]}'
        test_name_parts = node_id_parts[2].split("::")
        test_name = f'{test_name_parts[0].replace(".", "-")}-{test_name_parts[1]}'
        artifacts_dir = pathlib.Path(ROOT_DIR, 'tests/test-results', f"{file_path}-{test_name.replace('_', '-')}")
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
def page(page: Page, request, app_config):
    page.goto("https://www.saucedemo.com/")
    def fin():
        print("Page closed")
    request.addfinalizer(fin)
    return page


@pytest.fixture(scope="function")
def swag_ui(page: Page):
    return SwagLabs(page, "https://www.saucedemo.com/")


@pytest.fixture(scope='function')
def app_config():
    cfg = Config()
    return cfg

@pytest.fixture(scope="function")
def api_request_context(
    playwright: Playwright,
    app_config,
    request):
    headers = {
        "Authorization": f"token {app_config.pet_store_api_token}",
    }
    request_context = playwright.request.new_context(
        base_url="https://petstore.swagger.io/v2/", extra_http_headers=headers
    )
    yield request_context
    request_context.dispose()

