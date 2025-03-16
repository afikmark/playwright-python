from tests import expect
import pytest

@pytest.mark.swag_ui
def test_shopping_cart_remove_item(swag_ui, reporter, app_config, page):
    """
    This test verifies the following flow:
    login to sauceDemo with standard user
    add items to the shopping cart
    remove an item from the shopping cart
    Continue shopping and assert
    cart items are removed from the shopping cart counter
    """
    reporter.step('Step', 'Open Sauce Demo and login')
    swag_ui.flows.open_and_login(login_page=swag_ui.login_page,
                                 user_name=app_config.user_name,
                                 password=app_config.user_password)

    inventory_page = swag_ui.inventory_page
    reporter.step('Step','Add all items to the cart')
    for item in inventory_page.inventory_items.all():
        item.get_by_role('button', name='ADD TO CART').click()
    expect(swag_ui.cart_container.locator('span')).to_have_text('6')

    reporter.step('Step', 'Click on the cart button')
    swag_ui.cart_container.click()
    reporter.step('Step', 'Assert redirected to cart page')
    expect(page).to_have_url(swag_ui.shopping_cart_page.url)

    reporter.step('Step','Remove an item from the shopping cart and assert it was removed')
    cart_page = swag_ui.shopping_cart_page
    cart_items_count = cart_page.cart_items.count()
    cart_page.cart_items.first.get_by_role('button', name='REMOVE').click()
    expect(cart_page.cart_items).to_have_count(cart_items_count - 1)

    reporter.step('Step','Click on Continue shopping button and verify redirected to inventory page')
    swag_ui.shopping_cart_page.continue_shopping_button.click()
    expect(page).to_have_url(swag_ui.inventory_page.url)

    reporter.step('Step','Assert number of items in the shopping cart was updated')
    expect(swag_ui.cart_container.locator('span')).to_have_text('5')


