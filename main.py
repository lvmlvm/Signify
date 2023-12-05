from kivy.config import Config
Config.set('graphics', 'window_state', 'maximized')
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.graphics import Color, RoundedRectangle
from kivy.graphics.texture import Texture
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
from kivymd.uix.chip import MDChip
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

import dictionary
import question as qs
from scripts.settings import *
import cv2
import tensorflow
import numpy as np
import mediapipe as mp
import model.model_loader as md_loader
import camera
import pf

# Window.fullscreen = 'auto'
# Window.size = RESOLUTION
# Window.top = 100
# Window.left = 100
Builder.load_file('kvfiles/profile.kv')
Builder.load_file('kvfiles/learn.kv')
Builder.load_file('kvfiles/quiz.kv')
Builder.load_file('kvfiles/navigation.kv')
Builder.load_file('kvfiles/search.kv')
Builder.load_file('kvfiles/lesson.kv')
Builder.load_file('kvfiles/login.kv')
Builder.load_file('kvfiles/video.kv')
Builder.load_file('kvfiles/main.kv')

# Model
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (0, 0, 0)]


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

        self.word = None

        self.current_region = "Miền Bắc"
        self.current_word = 0
        self.words = []
        self.questions = []
        self.current_q = 0
        self.true_cnt = 0

        # Action detection
        self.show_capture = False
        Clock.schedule_interval(self.load_image, 1.0 / 300)

        self.image = None
        self.capture = None

        self.model = None
        self.model_checkpoints = 0
        self.actions = []

        self.sequence = []
        self.sentence = []
        self.predictions = []
        self.threshold = 0.9
        self.cap = cv2.VideoCapture(0)
        self.holistic = mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def show_simulate(self):
        self.ids.learn_screen.current = 'model'
        self.ids.learn_screen.transition.direction = 'left'

        self.cap = cv2.VideoCapture(0)

        content = qs.subjects[self.topic]['content'][self.word]
        self.model_checkpoints = content['model_checkpoints']
        self.model = md_loader.load_model(content['model_path'], self.model_checkpoints)
        self.actions = camera.convert_to_str(list(range(0, self.model_checkpoints)))

        self.show_capture = True

    def exit_simulate(self):
        self.cap.release()
        self.show_capture = False
        self.sentence = []
        self.sequence = []

        widget = self.ids.learn_screen.get_screen('model')
        widget.ids.simulate_success.text = ""

    def removes_marks_all_chips(self, selected_instance_chip):
        for instance_chip in self.ids.chip_box.children:
            if instance_chip != selected_instance_chip:
                instance_chip.active = False

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
            view.add_widget(ContentCard(self.subjects[topic]['content'], word, topic))

        self.ids.learn_screen.current = 'lesson'
        self.ids.learn_screen.transition.direction = 'left'

    def choose_word(self, card):
        for i in range(len(self.words)):
            if self.words[i] == card.word:
                self.current_word = i
                break

        self.show_flash_card()

    def show_flash_card(self):
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
        self.word = cur_word
        content = self.subjects[self.topic]['content'][cur_word]

        widget.ids.word.text = cur_word
        widget.ids.description.text = content['description']

        region = 'Toàn quốc' if 'Toàn quốc' in content['videoURL'].keys() else self.current_region

        widget.ids.video_source.source = content['videoURL'][region]

    def show_multiple_choice(self):
        widget = self.ids.learn_screen.get_screen('multiple_choice')
        widget.ids.topic_name.text = self.topic

        self.questions_content = qs.genQuestionaire(self.topic)

        self.questions = []

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
        if self.current_q == len(self.questions):
            score_widget = self.ids.learn_screen.get_screen('score')
            score_widget.ids.score.text = str(self.true_cnt) + '/10 điểm'

            self.ids.learn_screen.current = 'score'
            return

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

        region = 'Toàn quốc' if 'Toàn quốc' in self.questions[self.current_q]['videoURL'] else self.current_region
        widget.ids.video.source = self.questions[self.current_q]['videoURL'][region]

    def check_answer(self, obj):
        widget = self.ids.learn_screen.get_screen('multiple_choice')
        answer = self.questions[self.current_q]['answer']

        self.answer_card = None

        if obj.text == answer:
            self.true_cnt += 1
            self.answer_card = AnswerCard(True, answer)
        else:
            self.answer_card = AnswerCard(False, answer)

        widget.add_widget(self.answer_card)
    
    def load_image(self, *args):

        if not self.show_capture:
            return

        ret, frame = self.cap.read()
        self.image, results = camera.mediapipe_detection(frame, self.holistic)

        camera.draw_styled_landmarks(self.image, results)

        keypoints = camera.extract_keypoints(results)
        self.sequence.append(keypoints)
        self.sequence = self.sequence[-5:]

        if len(self.sequence) == 5:
            res = self.model.predict(np.expand_dims(self.sequence, axis=0))[0]
            self.predictions.append(np.argmax(res))

            if res[np.argmax(res)] > self.threshold:
                if np.unique(self.predictions[-3:])[0] == np.argmax(res):
                    if len(self.sentence) > 0:
                        if (self.actions[np.argmax(res)] != self.sentence[-1] and np.argmax(res) != 0 and
                                self.actions[np.argmax(res)] not in self.sentence):
                            self.sentence.append(self.actions[np.argmax(res)])
                    else:
                        if np.argmax(res) != 0:
                            self.sentence.append(self.actions[np.argmax(res)])

            if len(self.sentence) > 5:
                self.sentence = self.sentence[-5:]

            self.image = camera.prob_viz(res, self.actions, self.image, colors)

        cv2.rectangle(self.image, (0, 0), (640, 40), (245, 117, 16), -1)
        cv2.putText(self.image, ' '.join(self.sentence), (3, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        self.image = cv2.resize(self.image, (int(float(self.image.shape[1]) * 1.5), int(float(self.image.shape[0]) * 1.5)))
        self.image_frame = self.image
        buffer = cv2.flip(self.image_frame, 0).tostring()
        texture = Texture.create(size=(self.image_frame.shape[1], self.image_frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')

        widget = self.ids.learn_screen.get_screen('model')
        widget.ids.image.texture = texture

        if len(self.sentence) == self.model_checkpoints - 1 and np.unique(self.predictions[-5:])[0] == 0:
            widget.ids.simulate_success.text = "Success"


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
        self.word = word
        self.topic = args[2]

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


class SearchCard(MDCard):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        content = args[0]
        word = args[1]
        self.word = word
        self.topic = args[2]

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


class Score(MDScreen):
    pass


class SearchPage(MDScreen):
    def __init__(self, **kwargs):        
        super().__init__(**kwargs)
        self.trie = dictionary.Trie()
        self.num_word = 15

        self.menu = None
        self.cnt = 0

        # Card content
        self.topic = None
        self.word = None

        # Model
        self.show_capture = False
        Clock.schedule_interval(self.load_image, 1.0 / 300)

        self.image = None
        self.capture = None

        self.model = None
        self.model_checkpoints = 0
        self.actions = []

        self.sequence = []
        self.sentence = []
        self.predictions = []
        self.threshold = 0.9
        self.cap = cv2.VideoCapture(0)

        self.holistic = mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def show_suggestion(self, word):
        if self.menu is not None: self.menu.dismiss()

        words = sorted(self.trie.get_child_words(word))[:self.num_word]

        menu_items = [
            {
                'viewclass': 'OneLineListItem',
                'text': w,
                'on_release': lambda x=w: self.search_act(x)
            }
            for w in words
        ]

        self.menu = MDDropdownMenu(
            caller=self.ids.text_input,
            items=menu_items,
            width_mult=4,
        )
        self.menu.dismiss()

        self.menu.open()

    def search_act(self, word):
        self.menu.dismiss()
        words = self.trie.get_child_words(word)

        flag = len(words)

        self.ids.box_card.clear_widgets()
        for word in words:
            if word not in self.trie.topic:
                flag -= 1
                continue

            topic = self.trie.topic[word]
            if word in qs.subjects[topic]['content']:
                self.ids.box_card.add_widget(SearchCard(qs.subjects[topic]['content'], word, topic))

        if flag == 0:
            self.ids.screen_manager.current = 'nothing'
            self.ids.screen_manager.transition.direction = 'left'
        else:
            self.ids.screen_manager.current = 'show'
            self.ids.screen_manager.transition.direction = 'left'

    def show_video(self, card):
        self.topic = card.topic
        self.word = card.word

        widget = self.ids.result.get_screen('video')
        content = qs.subjects[self.topic]['content'][self.word]

        region = 'Toàn quốc' if 'Toàn quốc' in content['videoURL'] else 'Miền Bắc'

        widget.ids.video_source.source = content['videoURL'][region]
        widget.ids.word.text = self.word
        widget.ids.description.text = content['description']

        if 'model_path' in content:
            widget.ids.simulate_button.opacity = 1.0
            widget.ids.simulate_button.disabled = False
        else:
            widget.ids.simulate_button.opacity = 0.0
            widget.ids.simulate_button.disabled = True

        self.ids.result.current = 'video'
        self.ids.result.transition.direction = 'left'

    def start_camera(self):
        self.cap = cv2.VideoCapture(0)

        content = qs.subjects[self.topic]['content'][self.word]
        self.model_checkpoints = content['model_checkpoints']
        self.model = md_loader.load_model(content['model_path'], self.model_checkpoints)
        self.actions = camera.convert_to_str(list(range(0, self.model_checkpoints)))

    def stop_camera(self):
        self.cap.release()
        widget = self.ids.result.get_screen('model')
        widget.ids.simulate_success.text = ""

        self.sentence = []
        self.sequence = []

    def simulate(self):
        pass

    def load_image(self, *args):

        if not self.show_capture:
            return

        ret, frame = self.cap.read()
        self.image, results = camera.mediapipe_detection(frame, self.holistic)

        camera.draw_styled_landmarks(self.image, results)

        keypoints = camera.extract_keypoints(results)
        self.sequence.append(keypoints)
        self.sequence = self.sequence[-5:]

        if len(self.sequence) == 5:
            res = self.model.predict(np.expand_dims(self.sequence, axis=0))[0]
            self.predictions.append(np.argmax(res))

            if res[np.argmax(res)] > self.threshold:
                if np.unique(self.predictions[-3:])[0] == np.argmax(res):
                    if len(self.sentence) > 0:
                        if (self.actions[np.argmax(res)] != self.sentence[-1] and np.argmax(res) != 0 and
                                self.actions[np.argmax(res)] not in self.sentence):
                            self.sentence.append(self.actions[np.argmax(res)])
                    else:
                        if np.argmax(res) != 0:
                            self.sentence.append(self.actions[np.argmax(res)])

            if len(self.sentence) > 5:
                self.sentence = self.sentence[-5:]

            self.image = camera.prob_viz(res, self.actions, self.image, colors)

        cv2.rectangle(self.image, (0, 0), (640, 40), (245, 117, 16), -1)
        cv2.putText(self.image, ' '.join(self.sentence), (3, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        self.image = cv2.resize(self.image, (int(float(self.image.shape[1]) * 1.5), int(float(self.image.shape[0]) * 1.5)))
        self.image_frame = self.image
        buffer = cv2.flip(self.image_frame, 0).tostring()
        texture = Texture.create(size=(self.image_frame.shape[1], self.image_frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')

        widget = self.ids.result.get_screen('model')
        widget.ids.image.texture = texture

        if len(self.sentence) == self.model_checkpoints - 1 and np.unique(self.predictions[-5:])[0] == 0:
            widget.ids.simulate_success.text = "Success"


class VideoDisplay(MDScreen):
    pass

class VideoSimulate(MDScreen):
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

        self.profile_manager = pf.pm
        self.user = None
        self.main_screen = None
        self.subjects = qs.subjects

    def login(self):
        widget = self.main_screen.get_screen('login')

        login_email = widget.ids.login_email.text
        login_password = widget.ids.login_password.text

        login_status = self.profile_manager.login(login_email, login_password)

        if login_status == "Sai mật khẩu. Vui lòng nhập lại.":
            widget.ids.login_password.text = ""
            widget.ids.login_status.text = login_status
        elif login_status == "Tài khoản không tồn tại.":
            widget.ids.login_email.text = ""
            widget.ids.login_password.text = ""
            widget.ids.login_status.text = login_status
        else:
            self.user = login_status
            self.main_screen.current = 'home'
            self.main_screen.transition.direction = 'left'
    
    def register(self):
        widget = self.main_screen.get_screen('signup')
        
        register_name = widget.ids.register_name.text
        register_email = widget.ids.register_email.text
        register_password = widget.ids.register_password.text

        print("Main's register function called!")

        register_status = self.profile_manager.register(register_name, register_email, register_password)

        if register_status == "Email đã tồn tại. Vui lòng chọn email khác.":
            widget.ids.register_email.text = ""
            widget.ids.register_password.text = ""
            widget.ids.register_status.text = register_status
        else:
            self.user = register_status
            self.main_screen.current = 'home'
            self.main_screen.transition.direction = 'left'

    def logout(self):
        self.main_screen.current = 'login'
        self.user = "None"
        self.profile_manager.logout()

    def build(self):
        self.title = TITLE
        self.icon = ICON
        self.theme_cls.theme_style = 'Light'

        self.main_screen = MainScreen()

        return self.main_screen


if __name__ == '__main__':
    Signify().run()
    pf.pm.save()
