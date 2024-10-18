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
from kivy.uix.button import ButtonBehavior

# Daftar gambar
image_list = ['images/apple.png', 'images/banana.png', 'images/star.png']

class ImageButton(ButtonBehavior, Image):
    pass

class LoadingScreen(Screen):
    pass

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
        self.sm = ScreenManager()
        
        # Tambahkan loading screen dan main screen ke ScreenManager
        self.sm.add_widget(LoadingScreen(name='loading'))
        self.sm.add_widget(MainScreen(name='main'))
        self.sm.add_widget(MenuScreen(name='menu'))
        self.sm.add_widget(GameScreen(name='game'))
        self.sm.add_widget(ResultScreen(name='result'))

        # Set layar awal ke loading screen
        self.sm.current = 'loading'

        # Pindahkan ke MainScreen setelah beberapa detik (misalnya 3 detik)
        Clock.schedule_once(self.switch_to_main, 3)
        
        self.sm = Builder.load_file('math.kv')
        self.sound = SoundLoader.load('audio/background.mp3')  # Muat file musik latar
        if self.sound:  # Jika file musik berhasil dimuat
            self.sound.loop = True  # Set agar musik diputar berulang
            self.sound.volume = 1
            self.sound.play()  # Putar musik
        
        # Panggil animate_welcome_label setelah screen dimuat
        # Clock.schedule_once(self.animate_welcome_label, 1)
        # Animasi Tombol
        Clock.schedule_once(lambda dt: self.animate_button_blink(self.sm.get_screen('main').ids.mulai_button), 0.5)

        return self.sm
    
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
        images_box.clear_widgets()  # Bersihkan gambar sebelumnya

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

                images_box.add_widget(group_layout)  # Tambahkan grup gambar ke layout utama
        else:
            # Untuk operasi lain (penjumlahan, pengurangan, perkalian)
            for i in range(total_images):
                img = Image(source=image_choice)
                img.size_hint = (1, 1)
                img.size = (50, 50)

                # Jika operasi pengurangan, buat beberapa gambar menjadi transparan
                if self.operation == '-' and i >= (total_images - num_transparent):
                    img.opacity = 0.5

                images_box.add_widget(img)

        # Sesuaikan tinggi dari kotak gambar berdasarkan jumlah grup
        if self.operation == '/':
            images_box.height = (group_size * 60)  # Sesuaikan tinggi berdasarkan jumlah grup
            images_box.size_hint = (1, 1)
            img.size = (50, 50)
        else:
            images_box.height = ((total_images // 5) + 1) * 60  # Tinggi berdasarkan jumlah total gambar
            images_box.size_hint = (1, 1)
            img.size = (50, 50)

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
        # Perbaiki bagian ini dengan mendefinisikan result_text
            result_text = f"KAMU MENJAWAB {self.score} DARI {self.total_questions} SOAL DENGAN BENAR"
            self.sm.get_screen('result').ids.result_label.text = result_text
            self.sm.current = 'result'
            
            # Animasi Tombol
            Clock.schedule_once(lambda dt: self.animate_button_blink(self.sm.get_screen('result').ids.kembali_button), 0.5)

        # Periksa apakah seluruh soal dijawab benar
        congrats_image = self.sm.get_screen('result').ids.congrats_image
        if self.score == self.total_questions:
            # Tampilkan gambar congratulations jika seluruh soal dijawab benar
            congrats_image.opacity = 1  # Ubah opacity menjadi 1 (gambar tampil)
            congrats_image.disabled = False  # Aktifkan gambar
        else:
            # Sembunyikan gambar jika tidak semua soal benar
            congrats_image.opacity = 0  # Sembunyikan gambar
            congrats_image.disabled = True  # Nonaktifkan gambar

    def restart_game(self):
    # Reset skor dan jumlah soal
        self.score = 0
        self.current_question = 0
        self.sm.get_screen('game').ids.answer.text = ''  # Reset input field
        self.sm.get_screen('game').ids.feedback.text = ''  # Reset feedback text

    # Pindah ke screen menu
        self.sm.current = 'menu'

if __name__ == '__main__':
    MathGameApp().run()
