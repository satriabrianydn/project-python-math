from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.clock import Clock
from random import randint, choice
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.core.audio import SoundLoader
from kivy.animation import Animation 

# Daftar gambar
image_list = ['images/apple.png', 'images/banana.png', 'images/star.png']

class MainScreen(Screen):
    pass

class MenuScreen(Screen):
    pass

class GameScreen(Screen):
    pass

class ResultScreen(Screen):
    pass

class MathGameApp(MDApp):
    def build(self):
        self.sm = Builder.load_file('math.kv')
        self.sound = SoundLoader.load('audio/background.mp3')  # Muat file musik latar
        if self.sound:  # Jika file musik berhasil dimuat
            self.sound.loop = True  # Set agar musik diputar berulang
            self.sound.volume = 0.1
            self.sound.play()  # Putar musik
        
        # Panggil animate_welcome_label setelah screen dimuat
        Clock.schedule_once(self.animate_welcome_label, 1)

        return self.sm
    
    def animate_welcome_label(self, *args):
        # Ambil label dari MainScreen menggunakan ID yang sudah ditambahkan
        welcome_label = self.sm.get_screen('main').ids.welcome_label

        # Animasi fade in
        anim = Animation(opacity=1, duration=1)  # Fade in (muncul)
        anim.start(welcome_label)

        # Animasi loop naik turun
        loop_anim = Animation(y=200, duration=2)  # Gerakan naik
        loop_anim += Animation(y=100, duration=2)  # Gerakan turun
        loop_anim.repeat = True  # Loop animasi naik-turun
        loop_anim.start(welcome_label)


    def start_game(self, level):
        self.level = level
        self.score = 0
        self.current_question = 0
        self.total_questions = 10
        self.sm.current = 'game'
        self.generate_question()

    def generate_question(self):
        if self.level == 1:
            self.num1 = randint(1, 5)  # Angka untuk Kelas 1
            self.num2 = randint(1, 5)
            self.operation = choice(['+', '-'])
        elif self.level == 2:
            self.num1 = randint(1, 10)
            self.num2 = randint(1, 5)  # Batas pengurangan lebih kecil
            self.operation = '*'
        elif self.level == 3:
            self.num2 = randint(1, 10)
            self.num1 = self.num2 * randint(1, 5)  # Pastikan hasil tetap dalam batas yang lebih besar
            self.operation = '/'

        # Pastikan tidak mengurangi lebih dari yang ada
        if self.operation == '-':
            if self.num1 < self.num2:
                self.num1, self.num2 = self.num2, self.num1  # Menukar agar num1 selalu lebih besar

        if self.operation == '/':
            self.answer = self.num1 / self.num2
        else:
            self.answer = eval(f"{self.num1} {self.operation} {self.num2}")

        question_text = f"{self.num1} {self.operation} {self.num2} = ?"
        self.sm.get_screen('game').ids.question.text = question_text
        self.sm.get_screen('game').ids.feedback.text = ''

        # Menampilkan gambar sesuai angka
        self.display_images()

    def display_images(self):
        images_box = self.sm.get_screen('game').ids.images_box
        images_box.clear_widgets()  # Clear previous images

        # Determine which image to use based on the operation
        image_choice = choice(image_list)

        total_images = 0
        if self.operation == '+':
            total_images = self.num1 + self.num2
        elif self.operation == '-':
            total_images = self.num1
        elif self.operation == '*':
            total_images = self.num1 * self.num2
        elif self.operation == '/':
            total_images = self.num1  # Total images to show for division
            group_size = self.num2  # Number of images in each group

        # Display images according to the total
        if self.operation == '/':
            # Display images in groups for division
            for group in range(group_size):
                group_layout = MDBoxLayout(orientation='horizontal', spacing=1)  # Add spacing between groups

                for _ in range(self.num1 // self.num2):  # Each group should have a portion of images
                    img = Image(source=image_choice)
                    img.size_hint = (None, None)
                    img.size = (50, 50)

                    # Make images transparent if the operation is subtraction
                    if self.operation == '-':
                        img.opacity = 0.5  # Set opacity to 50% for transparency

                    group_layout.add_widget(img)

                images_box.add_widget(group_layout)  # Add the group of images to the main layout
        else:
            # For other operations
            for i in range(total_images):
                img = Image(source=image_choice)
                img.size_hint = (None, None)
                img.size = (50, 50)

                # Make images transparent if the operation is subtraction
                if self.operation == '-':
                    img.opacity = 0.5  # Set opacity to 50% for transparency

                images_box.add_widget(img)

        # Adjust the height of the images box based on the number of groups
        if self.operation == '/':
            images_box.height = (group_size * 60)  # Adjust height based on the number of groups
        else:
            images_box.height = ((total_images // 5) + 1) * 60

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
        Clock.schedule_once(self.show_result, 1)

    def show_result(self, *args):
        self.current_question += 1
        if self.current_question < self.total_questions:
            self.sm.get_screen('game').ids.answer.text = ''
            self.generate_question()
        else:
            result_text = f"Kamu menjawab {self.score} dari {self.total_questions} soal dengan benar!"
            self.sm.get_screen('result').ids.result_label.text = result_text
            self.sm.current = 'result'

    def restart_game(self):
        self.sm.current = 'menu'

if __name__ == '__main__':
    MathGameApp().run()
