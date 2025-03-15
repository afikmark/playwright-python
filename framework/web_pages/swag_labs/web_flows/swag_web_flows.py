from ..login import LoginPage

class SwagFlows:

    @staticmethod
    def open_and_login(login_page: LoginPage, user_name, password):
        login_page.open()
        login_page.login(user_name=user_name, password=password)
