from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
from kivy.clock import Clock
from random import randint, choice
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.uix.button import ButtonBehavior
from random import shuffle, sample

# Daftar gambar
image_list = ['images/apple.png', 'images/banana.png', 'images/star.png']

class ImageButton(ButtonBehavior, Image):
    pass

class LoadingScreen(Screen):
    pass

class MainScreen(Screen):
    def start_game(self):
        self.manager.get_screen('main')
        self.manager.current = 'main'
    
    def pulsate_button(self, button):
        min_size = (button.size[0] * 1, button.size[1] * 1)
        max_size = (button.size[0] * 1.2, button.size[1] * 1.2)
        anim = Animation(size=max_size, duration=0.5) + Animation(size=min_size, duration=0.5)
        anim.repeat = True  # Make it repeat indefinitely
        anim.start(button)

    def on_enter(self):
        self.pulsate_button(self.ids.mulai_button)
        self.pulsate_button(self.ids.settings_button)

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class MenuScreen(Screen):
    pass

class GameScreen(Screen):
    pass

class ResultScreen(Screen):
    pass

class MathGameApp(App):
    def build(self):
        self.sm = Builder.load_file('math.kv')
        
        self.click_sound = SoundLoader.load('audio/button_click.mp3')
        self.click_sound.volume = 1
        
        # Set layar awal ke loading screen
        self.sm.current = 'loading'

        # Pindahkan ke MainScreen setelah beberapa detik (misalnya 3 detik)
        Clock.schedule_once(self.switch_to_main, 5)
        
        
        self.sound = SoundLoader.load('audio/background.mp3')  # Muat file musik latar
        if self.sound:  # Jika file musik berhasil dimuat
            self.sound.loop = True  # Set agar musik diputar berulang
            self.sound.volume = 1
            self.sound.play()  # Putar musik
        
        # Animasi Tombol
        # Clock.schedule_once(lambda dt: self.animate_button_blink(self.sm.get_screen('main').ids.mulai_button), 0.5)
        # Clock.schedule_once(lambda dt: self.animate_button_blink(self.sm.get_screen('main').ids.settings_button), 0.5)

        return self.sm
    
    def play_click_sound(self):
        if self.click_sound:
            self.click_sound.play()
    
    def on_audio_switch(self, checkbox, value):
        if value:
            if self.sound: 
                self.sound.volume = 1 
            if self.click_sound:  
                self.click_sound.volume = 1  
        else:
            if self.sound:  
                self.sound.volume = 0  
            if self.click_sound:  
                self.click_sound.volume = 0  # Matikan suara klik
    
    def switch_to_main(self, *args):
        # Pindahkan layar dari loading screen ke main screen
        self.sm.current = 'main'
    
    def show_popup(self, message):
        popup = Popup(
            title="Info",
            content=Label(text=message),
            size_hint=(0.8, None),
            size=(400, 200)
        )
        popup.open()

    def start_game(self, level):
        self.play_click_sound()
        self.level = level
        self.score = 0
        self.current_question = 0
        self.total_questions = 10
        self.time_left = 60
        self.sm.current = 'game'

        self.timer_event = Clock.schedule_interval(self.update_timer, 1)
        self.generate_question()

    def update_timer(self, dt):
        if self.time_left > 0:
            self.time_left -= 1
            self.sm.get_screen('game').ids.timer_label.text = f"TIME: {self.time_left}"
        else:
            self.end_game()

    def end_game(self):
        if self.timer_event:
            Clock.unschedule(self.timer_event)
            self.timer_event = None

        score = self.sm.get_screen('result')  # Ganti self.manager dengan self.sm
        score.ids.score_label.text = f"SELAMAT! SKOR YANG KAMU DAPATKAN ADALAH {self.score}"
        self.sm.current = 'result'  # Ganti sm.current dengan self.sm.current

        congrats_images = score.ids.congrats_images
        star1 = score.ids.star1
        star2 = score.ids.star2
        star3 = score.ids.star3

        if self.score == 100:
            congrats_images.opacity = 1
            congrats_images.disabled = False
            star1.opacity = 1
            star2.opacity = 1
            star3.opacity = 1
            star1.disabled = False
            star2.disabled = False
            star3.disabled = False

        elif 50 <= self.score <= 90:
            congrats_images.opacity = 1
            congrats_images.disabled = False
            star1.opacity = 1
            star2.opacity = 0
            star3.opacity = 1
            star1.disabled = False
            star2.disabled = False
            star3.disabled = True

        elif 10 <= self.score <= 40:
            congrats_images.opacity = 1
            congrats_images.disabled = False
            star1.opacity = 0
            star2.opacity = 1
            star3.opacity = 0
            star1.disabled = False
            star2.disabled = True
            star3.disabled = True

        else:
            congrats_images.opacity = 0
            congrats_images.disabled = True
            star1.opacity = 0
            star2.opacity = 0
            star3.opacity = 0
            star1.disabled = True
            star2.disabled = True
            star3.disabled = True

        # congrats_images = self.sm.get_screen('result').ids.congrats_images

        # # Pastikan congrats_images tidak None
        # if congrats_images:
        #     star1 = congrats_images.ids.get('star1', None)
        #     star2 = congrats_images.ids.get('star2', None)
        #     star3 = congrats_images.ids.get('star3', None)

        #     if star1 is None or star2 is None or star3 is None:
        #         print("Salah satu gambar bintang tidak ditemukan")
        #         return

        #     # Pastikan congrats_images muncul (bisa mengatur opacity)
        #     congrats_images.opacity = 1
        #     congrats_images.disabled = False

        #     # Jika semua benar (10/10), tampilkan 3 bintang
        #     if self.score == 100:
        #         star1.opacity = 1
        #         star1.disabled = False
        #         star2.opacity = 1
        #         star2.disabled = False
        #         star3.opacity = 1
        #         star3.disabled = False
        #     # Jika benar antara 5 sampai 9, tampilkan 2 bintang
        #     elif 50 <= self.score < 100:
        #         star1.opacity = 1
        #         star1.disabled = False
        #         star2.opacity = 0
        #         star2.disabled = False
        #         star3.opacity = 1
        #         star3.disabled = True
        #     # Jika benar antara 1 sampai 4, tampilkan 1 bintang
        #     elif 10 <= self.score < 50:
        #         star1.opacity = 0
        #         star1.disabled = False
        #         star2.opacity = 1
        #         star2.disabled = True
        #         star3.opacity = 0
        #         star3.disabled = True
        #     # Jika tidak ada jawaban benar (0), jangan tampilkan bintang
        #     else:
        #         star1.opacity = 0
        #         star1.disabled = True
        #         star2.opacity = 0
        #         star2.disabled = True
        #         star3.opacity = 0
        #         star3.disabled = True
            
        #     congrats_images.canvas.ask_update()

    def generate_question(self):
        if self.level == 1:
            # Penambahan untuk Level 1
            self.num1 = randint(1, 5)
            self.num2 = randint(1, 5)
            self.operation = '+'
            question_text = f"{self.num1} + {self.num2} = ?"
            self.answer = self.num1 + self.num2
        
        elif self.level == 2:
            # Ekspresi dengan tanda kurung untuk Level 2
            self.num1 = randint(1, 5)
            self.num2 = randint(1, 5)
            self.num3 = randint(1, 5)
            question_text = f"{self.num1} + ({self.num2} * {self.num3}) = ?"
            self.answer = self.num1 + (self.num2 * self.num3)
        
        elif self.level == 3:
            # Ekspresi campuran tanpa tanda kurung untuk Level 3
            self.num1 = randint(1, 5)
            self.num2 = randint(1, 5)
            self.num3 = randint(1, 5)
            question_text = f"{self.num1} + {self.num2} * {self.num3} = ?"
            self.answer = self.num1 + (self.num2 * self.num3)

        # Tampilkan soal di layar
        self.sm.get_screen('game').ids.question.text = question_text
        self.sm.get_screen('game').ids.feedback.text = ''
        
        # Tampilkan gambar sesuai angka
        self.display_images()


    def display_images(self):
        images_grid = self.sm.get_screen('game').ids.images_grid
        images_grid.clear_widgets()  # Bersihkan gambar sebelumnya

        # Pilih gambar acak dari daftar image_list
        image_choice = choice(image_list)
        
        # Tentukan jumlah gambar berdasarkan hasil dari soal
        total_images = int(self.answer)  # Total gambar sesuai jawaban
       
        # Tampilkan gambar berdasarkan total_images
        for i in range(total_images):
            img = Image(source=image_choice)
            img.size_hint = (1,1)
            img.size = (500, 500)
            images_grid.add_widget(img)

        # Sesuaikan tinggi dari kotak gambar berdasarkan jumlah total gambar
        images_grid.height = ((total_images // 5) + 1) * 60  # Sesuaikan tinggi grid
        images_grid.size_hint = (1, 1)

        self.setup_answer_buttons()

    def setup_answer_buttons(self):
        correct_answer = self.answer

    # Buat range untuk pilihan jawaban salah
        range_start = int(correct_answer) - 10
        range_end = int(correct_answer) + 10

    # Pastikan ada cukup pilihan di rentang tersebut
        available_answers = list(range(range_start, range_end + 1))

    # Hapus jawaban yang benar dari daftar available_answers
        available_answers.remove(correct_answer)

    # Ambil dua jawaban salah unik dari available_answers
        wrong_answers = sample(available_answers, 2)

    # Gabungkan jawaban benar dan salah dalam satu list
        answer_options = [correct_answer] + wrong_answers
        shuffle(answer_options)

    # Set setiap tombol dengan jawaban acak
        self.sm.get_screen('game').ids.answer_button_1.text = str(answer_options[0])
        self.sm.get_screen('game').ids.answer_button_2.text = str(answer_options[1])
        self.sm.get_screen('game').ids.answer_button_3.text = str(answer_options[2])

    def check_button_answer(self, instance):
        self.play_click_sound()

    # Periksa apakah jawaban yang dipilih benar
        selected_answer = float(instance.text)
        if selected_answer == self.answer:
            self.score += 10
            self.show_popup("Jawaban Benar!")  # Tampilkan pop-up untuk jawaban benar
        else:
            self.show_popup("Jawaban Salah!")  # Tampilkan pop-up untuk jawaban salah

    # Update skor
        score_label = self.sm.get_screen('game').ids.score_label
        score_label.text = f"SCORE: {self.score}"

    # Tampilkan hasil setelah 1 detik
        Clock.schedule_once(self.show_result, 1)

    def show_result(self, *args):
        self.current_question += 1
        if self.current_question < self.total_questions:
            # Lanjut ke pertanyaan berikutnya jika belum selesai
            self.generate_question()
        else:
            # Tampilkan hasil jika semua pertanyaan selesai
            score_label = f"SELAMAT! SKOR YANG KAMU DAPATKAN ADALAH {self.score}"
            self.sm.get_screen('result').ids.score_label.text = score_label
            self.sm.current = 'result'

            # Tampilkan bintang berdasarkan jumlah skor
            congrats_images = self.sm.get_screen('result').ids.congrats_images
            star1 = self.sm.get_screen('result').ids.star1
            star2 = self.sm.get_screen('result').ids.star2
            star3 = self.sm.get_screen('result').ids.star3

            # Pastikan kontainer bintang muncul
            congrats_images.opacity = 1
            congrats_images.disabled = False

            # Tampilkan jumlah bintang berdasarkan skor
            if self.score == 100:  # 10/10 benar
                star1.opacity = 1
                star1.disabled = False
                star2.opacity = 1
                star2.disabled = False
                star3.opacity = 1
                star3.disabled = False
            elif 50 <= self.score < 100:  # 5 sampai 9 benar
                star1.opacity = 1
                star1.disabled = False
                star2.opacity = 0
                star2.disabled = True
                star3.opacity = 1
                star3.disabled = False
            elif 10 <= self.score < 50:  # 1 sampai 4 benar
                star1.opacity = 0
                star1.disabled = True
                star2.opacity = 1
                star2.disabled = False
                star3.opacity = 0
                star3.disabled = True
            else:  # Jika tidak ada jawaban yang benar (0 poin)
                star1.opacity = 0
                star1.disabled = True
                star2.opacity = 0
                star2.disabled = True
                star3.opacity = 0
                star3.disabled = True

            # Paksa pembaruan visual agar perubahan segera terlihat
            congrats_images.canvas.ask_update()

    def restart_game(self):
        self.play_click_sound()
        self.score = 0
        self.current_question = 0
        self.sm.get_screen('game').ids.feedback.text = ''  # Reset feedback text
        score_label = self.sm.get_screen('game').ids.score_label
        score_label.text = "SCORE: 0"  # Reset skor di label
        self.time_left = 60
        if hasattr(self, 'timer_event'):
            Clock.unschedule(self.timer_event)  # Hentikan timer
        self.sm.get_screen('game').ids.timer_label.text = f"TIME: {self.time_left}"  # Tampilkan waktu yang direset
        self.sm.current = 'menu'

if __name__ == '__main__':
    MathGameApp().run()