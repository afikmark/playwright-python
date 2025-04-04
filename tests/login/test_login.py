import pytest
import allure
from tests import expect

@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.swag_ui
@pytest.mark.parametrize('user_name, password', [('standard_user', 'secret_sauce'),
                                                 pytest.param('locked_out_user', 'secret_sauce', marks=pytest.mark.xfail),
                                                 ])
def test_login(swag_ui, reporter, page, user_name, password):
    """
    This test validates the login functionality
    of the application.
    """
    login_page = swag_ui.login_page
    login_page.open()
    reporter.step('Step', 'Login to SwagLabs')
    login_page.login(user_name, password)
    inventory_page = swag_ui.inventory_page
    reporter.step('Step', 'Assert user is in inventory page after login')
    expect(page).to_have_url(inventory_page.url)