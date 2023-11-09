import flet as ft

from scripts.login import LoginPage
from scripts.settings import *


class App:
    def __init__(self):
        self.content = None

        self.login = LoginPage(self)

    def run(self, page: ft.Page):

        page.title = TITLE
        page.bgcolor = ft.colors.WHITE
        page.vertical_alignment = ft.MainAxisAlignment.CENTER

        self.content = self.login.content

        page.add(self.content)


if __name__ == '__main__':
    app = App()
    ft.app(target=app.run, assets_dir='assets')
    # ft.app(target=app.run, view=ft.WEB_BROWSER, assets_dir="assets")
