import pytest
from tests import expect


@pytest.mark.swag_ui
def test_login(swag_ui, app_config):
    """
    This test validates the login functionality
    of the application.
    """
    login_page = swag_ui.login_page
    login_page.open()
    login_page.login(app_config.user_name, app_config.user_password)
    inventory_page = swag_ui.inventory_page
    expect(inventory_page.page).to_have_url(inventory_page.url)
