from tests import expect
import pytest


@pytest.mark.api
def test_get_pet_by_id(setup_teardown_pet_store, reporter, add_pet_data):
    """
    This test verifies the following flow:
    Add a pet to the store
    Get the pet by id
    assert the pet id and name
    Delete the pet
    """
    pet_store = setup_teardown_pet_store
    pet_name, pet_id = add_pet_data["name"], add_pet_data["id"]
    reporter.step("Step", "Get a pet by id")
    response = pet_store.get_pet_by_id(pet_id)
    expect(response).to_be_ok()
    reporter.step("Step", "assert pet id")
    assert response.json()["id"] == pet_id
    reporter.step("Step", "assert pet name")
    assert response.json()["name"] == pet_name
