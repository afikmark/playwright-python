from tests import expect
import pytest


@pytest.mark.swag_ui
def test_add_to_cart_button(swag_ui, app_config, reporter):
    """
    This test verifies the functionality of add to cart button.
    It finds the first item on the list, clicks on add to cart button
    and verifies it changes to 'Remove' and the item is added to the cart.
    Then it verifies the cart counter is updated.
    """
    reporter.step('Step', 'Open Sauce Demo and login')
    swag_ui.flows.open_and_login(login_page=swag_ui.login_page,
                                 user_name=app_config.user_name,
                                 password=app_config.user_password)

    inventory_page = swag_ui.inventory_page
    reporter.step('Step', 'Verify Cart is empty')
    expect(swag_ui.cart_container.locator('span')).to_be_hidden()

    reporter.step('Step', 'Locate the first item on the list and click on add to cart button')
    inventory_page.inventory_items.first.get_by_role('button', name='ADD TO CART').click()

    reporter.step('Step', 'Assert button text changed to "Remove"')
    inventory_page.inventory_items.first.get_by_role('button').text_content()
    expect(inventory_page.inventory_items.first.get_by_role('button')).to_have_text('Remove')

    reporter.step('Step', 'Assert cart counter updated')
    expect(swag_ui.cart_container.locator('span')).to_have_text('1')

    reporter.step('Step', 'Click on "Remove" button and verify cart is empty')
    inventory_page.inventory_items.first.get_by_role('button', name='Remove').click()
    expect(swag_ui.cart_container.locator('span')).to_be_hidden()

