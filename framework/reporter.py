import allure
from allure_commons.types import AttachmentType


class Reporter:
    """
    Abstract class for all reporters
    """

    def step(self, name='', message='', *args, **kwargs):
        raise NotImplementedError("Please implement step function")

    def attach_img(self, screenshot, *args, **kwargs):
        raise NotImplementedError("Please implement attach_img function")

    def attach_file(self, file, name, *args, **kwargs):
        raise NotImplementedError("Please implement attach_file function")


class AllureReporter(Reporter):

    def step(self, name='', message='', *args, **kwargs) -> None:
        with allure.step(message):
            pass

    def attach_img(self, screenshot, *args, **kwargs):
        allure.attach.file(screenshot, attachment_type=AttachmentType.PNG, name="Screenshot", **kwargs)

    def attach_file(self, file, name, *args, **kwargs):
        allure.attach.file(file, name="attachment", attachment_type=AttachmentType.WEBM, **kwargs)
