from tests import expect
import pytest


@pytest.mark.swag_ui
def test_add_to_cart_button(swag_ui, app_config):
    """
    This test verifies the functionality of add to cart button
    """
    swag_ui.flows.open_and_login(login_page=swag_ui.login_page,
                                 user_name=app_config.user_name,
                                 password=app_config.user_password)
    inventory_page = swag_ui.inventory_page
    inventory_page.item = inventory_page.inventory_items.BIKE_LIGHT
    inventory_page.add_to_cart_button.click()
    # assert tha button changed to "remove" after clicking add to cart
    expect(inventory_page.remove_from_cart_btn).to_have_text("Remove")
