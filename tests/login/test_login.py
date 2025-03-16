import pytest
import allure
from tests import expect


@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.swag_ui
def test_login(swag_ui, app_config, reporter, page):
    """
    This test validates the login functionality
    of the application.
    """
    login_page = swag_ui.login_page
    login_page.open()
    reporter.step('Step', 'Login to SwagLabs')
    login_page.login(app_config.user_name, app_config.user_password)
    inventory_page = swag_ui.inventory_page
    reporter.step('Step', 'Assert user is in inventory page after login')
    expect(page).to_have_url(inventory_page.url)


# @pytest.mark.skip("This test is for testing the video and screenshot capture on failure")
def test_login_fail(swag_ui, app_config, reporter, page):
    """
    This test verifies login with invalid credentials
    """
    login_page = swag_ui.login_page
    login_page.open()
    reporter.step('Step', 'Login to SwagLabs')
    login_page.login(user_name='wrong', password='password')
    inventory_page = swag_ui.inventory_page
    expect(page).to_have_url(inventory_page.url)
