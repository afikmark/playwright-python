from tests import expect
import pytest

@pytest.mark.api
def test_get_pet_by_id(api_request_context):
    response = api_request_context.get(url='pet/1')
    expect(response).to_be_ok()
    assert response.json()["id"] == 1