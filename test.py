from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

KV = '''
ScreenManager:
    FirstScreen:
    SecondScreen:

<FirstScreen>:
    name: 'first'
    BoxLayout:
        orientation: 'vertical'
        MDRaisedButton:
            text: 'Go to Second Screen'
            on_release: app.root.current = 'second'

<SecondScreen>:
    name: 'second'
    BoxLayout:
        orientation: 'vertical'
        MDRaisedButton:
            text: 'Go to First Screen'
            on_release: app.root.current = 'first'
'''

class FirstScreen(MDScreen):
    def on_leave(self):
        print(f'Leaving {self.name} screen, parent: {self.parent}')

class SecondScreen(MDScreen):
    def on_leave(self):
        print(f'Leaving {self.name} screen, parent: {self.parent}')

class TestApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

if __name__ == '__main__':
    TestApp().run()