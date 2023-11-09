import flet as ft
from scripts.settings import *


class App:
    def __init__(self):
        self.content = ft.Container(
            ft.Text('Hello', color='#000000')
        )

    def run(self, page: ft.Page):

        page.title = TITLE
        page.bgcolor = ft.colors.WHITE
        page.vertical_alignment = ft.MainAxisAlignment.CENTER

        page.add(self.content)


if __name__ == '__main__':
    app = App()
    ft.app(target=app.run, assets_dir='assets')
    # ft.app(target=app.run, view=ft.WEB_BROWSER, assets_dir="assets")
