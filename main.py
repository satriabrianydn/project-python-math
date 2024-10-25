from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.clock import Clock
from random import randint, choice
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.uix.button import ButtonBehavior
from kivymd.uix.dialog import MDDialog
from random import shuffle, sample


Window.size = (800, 480)

# Daftar gambar
image_list = ['images/apple.png', 'images/banana.png', 'images/star.png']

class ImageButton(ButtonBehavior, Image):
    pass

class LoadingScreen(Screen):
    pass

class MainScreen(Screen):
    pass

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class MenuScreen(Screen):
    pass

class GameScreen(Screen):
    pass

class ResultScreen(Screen):
    pass

class MathGameApp(MDApp):
    def build(self):
        self.sm = ScreenManager()
        
        self.click_sound = SoundLoader.load('audio/button_click.mp3')
        self.click_sound.volume = 1
        
        # Tambahkan loading screen dan main screen ke ScreenManager
        self.sm.add_widget(LoadingScreen(name='loading'))
        self.sm.add_widget(MainScreen(name='main'))
        self.sm.add_widget(SettingsScreen(name='settings'))
        self.sm.add_widget(MenuScreen(name='menu'))
        self.sm.add_widget(GameScreen(name='game'))
        self.sm.add_widget(ResultScreen(name='result'))

        # Set layar awal ke loading screen
        self.sm.current = 'loading'

        # Pindahkan ke MainScreen setelah beberapa detik (misalnya 3 detik)
        Clock.schedule_once(self.switch_to_main, 15)
        
        self.sm = Builder.load_file('math.kv')
        self.sound = SoundLoader.load('audio/background.mp3')  # Muat file musik latar
        if self.sound:  # Jika file musik berhasil dimuat
            self.sound.loop = True  # Set agar musik diputar berulang
            self.sound.volume = 0.1
            self.sound.play()  # Putar musik
        
        # Panggil animate_welcome_label setelah screen dimuat
        # Clock.schedule_once(self.animate_welcome_label, 1)
        
        # Animasi Tombol
        Clock.schedule_once(lambda dt: self.animate_button_blink(self.sm.get_screen('main').ids.mulai_button), 0.5)

        return self.sm
    
    def play_click_sound(self):
        if self.click_sound:
            self.click_sound.play()
    
    def on_audio_switch(self, checkbox, value):
        if value:
            if self.sound:  # Pastikan sound berhasil dimuat
                self.sound.volume = 0.1  # Volume background lebih kecil
            if self.click_sound:  # Pastikan click_sound berhasil dimuat
                self.click_sound.volume = 1  # Volume penuh untuk klik
        else:
            if self.sound:  # Pastikan sound berhasil dimuat
                self.sound.volume = 0  # Matikan background music
            if self.click_sound:  # Pastikan click_sound berhasil dimuat
                self.click_sound.volume = 0  # Matikan suara klik
    
    def switch_to_main(self, *args):
        # Pindahkan layar dari loading screen ke main screen
        self.sm.current = 'main'
    
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
        
    def animate_button_blink(self, button):
        # Animasi zoom out (perkecil tombol)
        anim = Animation(size=(230, 90), duration=0.5)  
        
        # Animasi zoom in (perbesar tombol)
        anim += Animation(size=(270, 110), duration=0.5)  
        
        # Ulangi animasi terus menerus
        anim.repeat = True
        
        # Mulai animasi
        anim.start(button)

    def show_popup(self, message):
        dialog = MDDialog(
            title="Info",
            text=message,
            size_hint=(0.8, None),  # Sesuaikan lebar dialog
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()  # Menutup dialog saat tombol OK ditekan
                )
            ]
        )
        dialog.open()

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
        # Stop the timer
        Clock.unschedule(self.timer_event)

        # Show the result screen
        self.sm.current = 'result'
        result_text = f"TIME IS UP! SCORE: {self.score}"
        self.sm.get_screen('result').ids.result_label.text = result_text
        
        # Animasi Tombol
        Clock.schedule_once(lambda dt: self.animate_button_blink(self.sm.get_screen('result').ids.kembali_button), 0.5)

        # Handle showing the congrats image if necessary
        congrats_image = self.sm.get_screen('result').ids.congrats_image
        if self.score == 100:
            congrats_image.opacity = 1
            congrats_image.disabled = False
        else:
            congrats_image.opacity = 0
            congrats_image.disabled = True

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
        images_grid = self.sm.get_screen('game').ids.images_grid
        images_grid.clear_widgets()  # Bersihkan gambar sebelumnya

        # Pilih gambar acak dari daftar image_list
        image_choice = choice(image_list)

        total_images = 0
        if self.operation == '+':
            total_images = self.num1 + self.num2
        elif self.operation == '-':
            total_images = self.num1  # Menampilkan sebanyak num1 gambar
            transparent_images = self.num2  # Jumlah gambar yang akan ditransparasikan (dikurangi)
        elif self.operation == '*':
            total_images = self.num1 * self.num2
        elif self.operation == '/':
            total_images = self.num1  # Total gambar yang akan ditampilkan untuk pembagian
            group_size = self.num2  # Jumlah gambar dalam setiap grup

        num_transparent = self.num2 if self.operation == '-' else 0
        
        # Tampilkan gambar sesuai operasi
        if self.operation == '/':
            # Tampilkan gambar dalam grup untuk operasi pembagian
            for group in range(group_size):
                group_layout = MDBoxLayout(orientation='horizontal', spacing=1)  # Tambahkan spasi antar grup

                for _ in range(self.num1 // self.num2):  # Setiap grup akan memiliki sejumlah gambar
                    img = Image(source=image_choice)
                    img.size_hint = (1, 1)
                    img.size = (50, 50)
                    group_layout.add_widget(img)

                images_grid.add_widget(group_layout)  # Tambahkan grup gambar ke layout utama
        else:
            # Untuk operasi lain (penjumlahan, pengurangan, perkalian)
            for i in range(total_images):
                img = Image(source=image_choice)
                img.size_hint = (1, 1)
                img.size = (50, 50)

                # Jika operasi pengurangan, buat beberapa gambar menjadi transparan
                if self.operation == '-' and i >= (total_images - num_transparent):
                    img.opacity = 0.5

                images_grid.add_widget(img)

        # Sesuaikan tinggi dari kotak gambar berdasarkan jumlah grup
        if self.operation == '/':
            images_grid.height = (group_size * 60)  # Sesuaikan tinggi berdasarkan jumlah grup
            images_grid.size_hint = (1, 1)
            img.size = (50, 50)
        else:
            images_grid.height = ((total_images // 5) + 1) * 60  # Tinggi berdasarkan jumlah total gambar
            images_grid.size_hint = (1, 1)
            img.size = (50, 50)

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

    # def check_answer(self):
    #     self.play_click_sound()
    #     user_answer = self.sm.get_screen('game').ids.answer.text
    #     score_label = self.sm.get_screen('game').ids.score_label

    #     if user_answer.strip() == '':
    #         self.show_popup("Silakan masukkan jawaban!")  # Tampilkan pop-up jika tidak ada jawaban
    #         return

    #     try:
    #         if self.operation == '/':
    #             user_answer = float(user_answer)
    #             correct = abs(user_answer - self.answer) < 0.01
    #         else:
    #             user_answer = int(user_answer)
    #             correct = user_answer == self.answer

    #         if correct:
    #             self.score += 10
    #             self.show_popup("Jawaban Benar!")  # Tampilkan pop-up untuk jawaban benar
    #         else:
    #             self.show_popup("Jawaban Salah!")  # Tampilkan pop-up untuk jawaban salah
    #     except ValueError:
    #         self.show_popup("Jawaban Tidak Valid!")  # Tampilkan pop-up untuk jawaban tidak valid

    #     score_label.text = f"SCORE: {self.score}"
    #     Clock.schedule_once(self.show_result, 1)

    def show_result(self, *args):
        self.current_question += 1
        if self.current_question < self.total_questions:
            # self.sm.get_screen('game').ids.answer.text = ''
            self.generate_question()
        else:
        # Perbaiki bagian ini dengan mendefinisikan result_text
            result_text = f"SELAMAT! SCORE YANG KAMU DAPATKAN ADALAH {self.score}"
            self.sm.get_screen('result').ids.result_label.text = result_text
            self.sm.current = 'result'
            
            # Animasi Tombol
            Clock.schedule_once(lambda dt: self.animate_button_blink(self.sm.get_screen('result').ids.kembali_button), 0.5)

        # Periksa apakah seluruh soal dijawab benar
        congrats_image = self.sm.get_screen('result').ids.congrats_image
        if self.score == 100:
            # Tampilkan gambar congratulations jika seluruh soal dijawab benar
            congrats_image.opacity = 1  # Ubah opacity menjadi 1 (gambar tampil)
            congrats_image.disabled = False  # Aktifkan gambar
        else:
            # Sembunyikan gambar jika tidak semua soal benar
            congrats_image.opacity = 0  # Sembunyikan gambar
            congrats_image.disabled = True  # Nonaktifkan gambar

    def restart_game(self):
    # Reset skor dan jumlah soal
        self.play_click_sound()
        self.score = 0
        self.current_question = 0
        # self.sm.get_screen('game').ids.answer.text = ''  # Reset input field
        self.sm.get_screen('game').ids.feedback.text = ''  # Reset feedback text

        score_label = self.sm.get_screen('game').ids.score_label
        score_label.text = "SCORE: 0"  # Reset skor di label

    # Pindah ke screen menu
        self.sm.current = 'menu'

if __name__ == '__main__':
    MathGameApp().run()