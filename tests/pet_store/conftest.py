import pytest

from framework.api_requests import PetStoreAPI
from framework.logger import get_logger
from tests import expect
logger = get_logger()



@pytest.fixture
def add_pet_data(request) -> dict:
    return {
        "id": 11,
        "category": {
            "id": 5,
            "name": "Wolf"
        },
        "name": "Sif",
        "photoUrls": [
            "string"
        ],
        "tags": [
            {
                "id": 5,
                "name": "Wolves"
            }
        ],
        "status": "available"
    }

@pytest.fixture
def pet_store_api(api_request_context):
    return PetStoreAPI(api_request_context)

@pytest.fixture
def setup_teardown_pet_store(pet_store_api, add_pet_data, reporter):
    post_response = pet_store_api.post_pet(add_pet_data)
    expect(post_response).to_be_ok()
    logger.info("Added a pet to the store")
    yield pet_store_api
    delete_response = pet_store_api.delete_pet(add_pet_data['id'])
    expect(delete_response).to_be_ok()
    logger.info("Deleted the pet from the store")
