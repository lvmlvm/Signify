from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.graphics import Color, RoundedRectangle
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.utils import rgba
from kivymd.uix.behaviors import CommonElevationBehavior
from kivymd.uix.bottomnavigation import MDBottomNavigation
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatButton, MDFillRoundFlatIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.fitimage import FitImage
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.navigationdrawer import MDNavigationLayout
from kivymd.uix.navigationrail import MDNavigationRail
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.textfield import MDTextField
from kivymd.uix.widget import MDWidget
from kivy.core.window import Window
from kivy.uix.videoplayer import VideoPlayer

import question as qs
from scripts.settings import *

# Window.fullscreen = 'auto'
Builder.load_file('kvfiles/profile.kv')
Builder.load_file('kvfiles/learn.kv')
Builder.load_file('kvfiles/quiz.kv')
Builder.load_file('kvfiles/navigation.kv')
Builder.load_file('kvfiles/search.kv')
Builder.load_file('kvfiles/lesson.kv')
Builder.load_file('kvfiles/login.kv')
Builder.load_file('kvfiles/main.kv')


class IconListItem(OneLineIconListItem):
    icon = StringProperty()


class MainNavigation(MDFloatLayout):
    def switch_tabs(self, instance_navigation_rail, instance_navigation_rail_item):
        pages = {
            'nfc-search-variant': 'search_page',
            'account-circle': 'profile_page',
            'school': 'learn_page',
        }
        self.ids.nav_tabs.current = pages[instance_navigation_rail_item.icon]


class LearnScreen(MDScreenManager):
    pass


class Tab(MDFloatLayout, MDTabsBase):
    pass


class LessonView(MDScrollView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Lesson(MDScreen):
    pass


class MainScreen(MDScreenManager):
    pass


class LearnPage(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.answer_card = None
        self.questions_content = None
        self.subjects = None
        self.topic = None

        self.current_word = 0
        self.words = []
        self.questions = []
        self.current_q = 0

    def show_lesson(self, topic):
        self.subjects = qs.subjects
        self.topic = topic

        self.ids.learn_screen.get_screen('lesson').ids.topic_name.text = topic
        self.ids.learn_screen.get_screen('lesson').ids.topic_description.text = self.subjects[topic]['description']

        view = self.ids.learn_screen.get_screen('lesson').ids.content_view
        view.clear_widgets()
        self.words.clear()
        for word in self.subjects[topic]['content'].keys():
            self.words.append(word)
            view.add_widget(ContentCard(self.subjects[topic]['content'], word))

        self.ids.learn_screen.current = 'lesson'
        self.ids.learn_screen.transition.direction = 'left'

    def show_flash_card(self):
        self.current_word = 0
        self.change_flash_card()

        self.ids.learn_screen.current = 'flash_card'
        self.ids.learn_screen.transition.direction = 'left'

    def next_flash_card(self, inc):
        self.current_word += inc + len(self.words)
        self.current_word %= len(self.words)

        self.change_flash_card()

    def change_flash_card(self):
        widget = self.ids.learn_screen.get_screen('flash_card')
        widget.ids.topic_name.text = self.topic

        cur_word = self.words[self.current_word]
        content = self.subjects[self.topic]['content'][cur_word]

        widget.ids.word.text = cur_word
        widget.ids.description.text = content['description']

        region = 'Toàn quốc' if 'Toàn quốc' in content['videoURL'].keys() else 'Miền Bắc'

        widget.ids.video_source.source = content['videoURL'][region]

    def show_multiple_choice(self):
        widget = self.ids.learn_screen.get_screen('multiple_choice')
        widget.ids.topic_name.text = self.topic

        self.questions_content = qs.genQuestionaire(self.topic)

        for i in self.questions_content['content'].keys():
            self.questions.append(
                {
                    'answer': self.questions_content['content'][i]['answer'],
                    'A': self.questions_content['content'][i]['choices']['A'],
                    'B': self.questions_content['content'][i]['choices']['B'],
                    'C': self.questions_content['content'][i]['choices']['C'],
                    'D': self.questions_content['content'][i]['choices']['D'],
                    'videoURL': self.questions_content['content'][i]['videoURL']
                }
            )

        self.current_q = -1
        self.change_question()

        self.ids.learn_screen.current = 'multiple_choice'
        self.ids.learn_screen.transition.direction = 'left'

    def change_question(self):
        self.current_q += 1
        self.current_q %= len(self.questions)

        widget = self.ids.learn_screen.get_screen('multiple_choice')
        if self.answer_card is not None:
            widget.remove_widget(self.answer_card)
            self.answer_card = None

        widget.ids.a.text = self.questions[self.current_q]['A']
        widget.ids.b.text = self.questions[self.current_q]['B']
        widget.ids.c.text = self.questions[self.current_q]['C']
        widget.ids.d.text = self.questions[self.current_q]['D']

        widget.ids.bar.value = (self.current_q + 1) * 10

        region = 'Toàn quốc' if 'Toàn quốc' in self.questions[self.current_q]['videoURL'] else 'Miền Bắc'
        widget.ids.video.source = self.questions[self.current_q]['videoURL'][region]

    def check_answer(self, obj):
        widget = self.ids.learn_screen.get_screen('multiple_choice')
        answer = self.questions[self.current_q]['answer']

        self.answer_card = None

        if obj.text == answer:
            self.answer_card = AnswerCard(True, answer)
        else:
            self.answer_card = AnswerCard(False, answer)

        widget.add_widget(self.answer_card)


class AnswerCard(MDCard):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        var = args[0]
        answer = args[1]

        if var:
            self.md_bg_color = 'b0ffd4'
            self.ids.button.md_bg_color = '09b858'
        else:
            self.md_bg_color = 'f0b4b4'
            self.ids.button.md_bg_color = 'f50707'

        self.ids.answer.text = answer


class ContentCard(MDCard):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        content = args[0]
        word = args[1]

        self.orientation = 'vertical'
        self.padding = '8dp'
        self.size_hint = (1, None)
        self.height = 250
        self.elevation = 2
        self.border_radius = 20
        self.radius = [15]

        first_layer = MDBoxLayout(
            orientation='horizontal',
            spacing='30dp',
        )

        first_layer.add_widget(
            Image(
                size_hint=(None, None),
                size=(240, 240),
                pos_hint={'center_y': .5},
                source=content[word]['imageURL']
            )
        )

        second_layer = MDBoxLayout(orientation='vertical')
        second_layer.add_widget(
            Word(text=word)
        )
        second_layer.add_widget(
            Description(text=content[word]['description'])
        )
        first_layer.add_widget(second_layer)

        self.add_widget(first_layer)


class Word(MDLabel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = 'Bold'
        self.font_size = '26sp'


class Description(MDLabel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = 'Light'
        self.font_size = '13sp'


class TopicCard(MDCard):
    topic = StringProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.md_bg_color = 'f0f0f0'
        self.orientation = 'horizontal'
        self.spacing = 30
        self.padding = (20, 0)


class RecentLearn(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class FlashCard(MDScreen):
    pass


class MultipleChoice(MDScreen):
    pass


class Signify(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        LabelBase.register(name='Medium', fn_regular='assets/fonts/Lexend-Medium.ttf')
        LabelBase.register(name='Light', fn_regular='assets/fonts/Lexend-Light.ttf')
        LabelBase.register(name='Regular', fn_regular='assets/fonts/Lexend-Regular.ttf')
        LabelBase.register(name='Bold', fn_regular='assets/fonts/Lexend-Medium.ttf')
        LabelBase.register(name='ExtraBold', fn_regular='assets/fonts/Lexend-ExtraBold.ttf')
        LabelBase.register(name='SemiBold', fn_regular='assets/fonts/Lexend-SemiBold.ttf')

        self.main_screen = None

        self.subjects = qs.subjects

    def build(self):
        self.title = TITLE
        self.icon = ICON
        self.theme_cls.theme_style = 'Light'

        self.main_screen = MainScreen()

        return self.main_screen


if __name__ == '__main__':
    Signify().run()
