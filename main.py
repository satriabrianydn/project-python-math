from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.clock import Clock
from random import randint, choice

KV = '''
ScreenManager:
    MenuScreen:
    GameScreen:
    ResultScreen:

<MenuScreen>:
    name: 'menu'

    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20

        MDLabel:
            text: 'Pilih Level Kelas'
            halign: 'center'
            font_style: 'H4'

        MDRaisedButton:
            text: 'Kelas 1'
            pos_hint: {'center_x': 0.5}
            on_release: app.start_game(1)

        MDRaisedButton:
            text: 'Kelas 2'
            pos_hint: {'center_x': 0.5}
            on_release: app.start_game(2)

        MDRaisedButton:
            text: 'Kelas 3'
            pos_hint: {'center_x': 0.5}
            on_release: app.start_game(3)

<GameScreen>:
    name: 'game'

    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20

        MDBoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: "48dp"
            padding: [0, 10, 0, 0]
            spacing: 10

        MDBoxLayout:
            orientation: 'vertical'
            padding: [0, 10, 0, 0]
            spacing: 20

            MDLabel:
                id: question
                text: ''
                halign: 'center'
                font_style: 'H4'

            MDTextField:
                id: answer
                hint_text: 'Masukkan jawaban'
                mode: 'rectangle'
                halign: 'center'

            MDRaisedButton:
                text: 'Submit'
                pos_hint: {'center_x': 0.5}
                on_release: app.check_answer()

        MDLabel:
            id: feedback
            text: ''
            halign: 'center'
            font_style: 'Subtitle1'
            theme_text_color: 'Secondary'

<ResultScreen>:
    name: 'result'

    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20

        MDLabel:
            id: result_label
            text: ''
            halign: 'center'
            font_style: 'H4'

        MDLabel:
            id: feedback_label
            text: ''
            halign: 'center'
            font_style: 'Subtitle1'
            theme_text_color: 'Secondary'

        MDRaisedButton:
            text: 'Main lagi'
            pos_hint: {'center_x': 0.5}
            on_release: app.restart_game()
'''

class MenuScreen(Screen):
    pass

class GameScreen(Screen):
    pass

class ResultScreen(Screen):
    pass

class MathGameApp(MDApp):
    def build(self):
        self.sm = Builder.load_string(KV)
        return self.sm

    def start_game(self, level):
        self.level = level
        self.score = 0
        self.current_question = 0
        self.total_questions = 5
        self.sm.current = 'game'
        self.generate_question()

    def generate_question(self):
        if self.level == 1:
            operations = ['+', '-']
            self.operation = choice(operations)
            self.num1 = randint(1, 10)
            self.num2 = randint(1, 10)
        elif self.level == 2:
            self.operation = '*'
            self.num1 = randint(1, 10)
            self.num2 = randint(1, 10)
        elif self.level == 3:
            self.operation = '/'
            self.num1 = randint(10, 50)
            self.num2 = randint(1, 10)
            while self.num1 % self.num2 != 0:
                self.num1 = randint(10, 50)
                self.num2 = randint(1, 10)

        if self.operation == '/':
            self.answer = self.num1 / self.num2
        else:
            self.answer = eval(f"{self.num1} {self.operation} {self.num2}")

        question_text = f"{self.num1} {self.operation} {self.num2} = ?"
        self.sm.get_screen('game').ids.question.text = question_text
        self.sm.get_screen('game').ids.feedback.text = ''

    def check_answer(self):
        user_answer = self.sm.get_screen('game').ids.answer.text
        feedback_label = self.sm.get_screen('game').ids.feedback

        if user_answer.strip() == '':
            feedback_label.text = "Silakan masukkan jawaban!"
            return

        try:
            if self.operation == '/':
                user_answer = float(user_answer)
                correct = abs(user_answer - self.answer) < 0.01
            else:
                user_answer = int(user_answer)
                correct = user_answer == self.answer

            if correct:
                self.score += 1
                feedback_message = "Jawaban Benar!"
            else:
                feedback_message = "Jawaban Salah!"

        except ValueError:
            feedback_message = "Jawaban Tidak Valid!"

        feedback_label.text = feedback_message

        # Kirim pesan feedback ke layar hasil
        Clock.schedule_once(self.show_result, 1)

    def show_result(self, *args):
        self.current_question += 1

        if self.current_question < self.total_questions:
            self.sm.get_screen('game').ids.answer.text = ''
            self.generate_question()
        else:
            result_text = f"Kamu menjawab {self.score} dari {self.total_questions} soal dengan benar!"
            result_screen = self.sm.get_screen('result')
            result_screen.ids.result_label.text = result_text
            self.sm.current = 'result'

    def restart_game(self):
        self.sm.current = 'menu'

if __name__ == '__main__':
    MathGameApp().run()
