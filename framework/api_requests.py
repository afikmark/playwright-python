from playwright.async_api import APIRequestContext

from framework.utils import retry_on_404


class PetStoreAPI:

    def __init__(self, pet_store: APIRequestContext):
        self.pet_store = pet_store

    @retry_on_404()
    def get_pet_by_id(self, pet_id):
        return self.pet_store.get(url=f'pet/{pet_id}')

    @retry_on_404()
    def post_pet(self, data):
        return self.pet_store.post(url='pet', data=data)

    @retry_on_404()
    def delete_pet(self, pet_id):
        return self.pet_store.delete(url=f'pet/{pet_id}')

