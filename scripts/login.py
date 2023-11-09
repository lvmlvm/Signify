import flet as ft


class LoginPage:
    def __init__(self, app):
        self.app = app
        self.content = None

        introduce = ft.Container(
            ft.Container(
                ft.Column(
                    [
                        ft.Text('Học ASL miễn phí'),
                        ft.Text('Tương tác giữa người khiếm thính chưa bao giờ d dàng hơn thông qua phiên dịch ASL và '
                                'hệ thống học')
                    ]
                ),
            ),
            bgcolor='#3DB2FF',
            height=1024,
            # alignment=
        )

        login_form = ft.Container(
            ft.Container(
                ft.Column(
                    [
                        ft.Image(src='assets/images/logo.png')
                    ]
                )
            ),
            bgcolor='#FFFFFF'
        )

        # self.content = introduce

        self.content = ft.Row(
            [introduce, login_form]
        )
