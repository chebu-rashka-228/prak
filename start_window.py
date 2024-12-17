import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
from CONST import *
from engine import BackAsteroids
from rocket import Rocket


class StartWindow:
    def __init__(self, root):
        self.root = root
        self.score = SCORE_DEFAULT
        self.lives = LIVES_DEFAULT

        # загрузка изображения для фона
        self.background_image = ImageTk.PhotoImage(Image.open(PATH_BACK_FONE))

        # Создание объекта канваса
        self.canvas = tk.Canvas(self.root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.canvas.pack()

        # Установка заднего фона
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)

        # Создание полупрозрачной кнопки
        self.button_image = self.create_button_image("START", BUTTON_FONT, BUTTON_COLOR, BUTTON_BORDER_COLOR)
        self.button = tk.Button(self.root, image=self.button_image, command=self.clear_canvas, borderwidth=0,
                                highlightthickness=0, relief=tk.FLAT)  # Убираем рельеф

        # Центровка кнопки
        button_x = (WINDOW_WIDTH - self.button_image.width()) // 2
        button_y = (WINDOW_HEIGHT - self.button_image.height()) // 2
        self.button.place(x=button_x, y=button_y)

        # Создание и размещение заголовка
        try:
            title_font = ImageFont.truetype(BUTTON_FONT, 48)
            title_font_tuple = (title_font.font.family, title_font.size)
        except Exception:
            title_font_tuple = ("Arial", 48)

        self.title_label = tk.Label(self.root, text="АСТЕРОИДЫ", font=title_font_tuple, fg="lime green", bg="black")
        title_x = (WINDOW_WIDTH - self.title_label.winfo_reqwidth()) // 2
        title_y = button_y - self.title_label.winfo_reqheight() - 20
        self.title_label.place(x=title_x, y=title_y)

        try:
            label_font = ImageFont.truetype(BUTTON_FONT, 16)
            label_font_tuple = (label_font.font.family, label_font.size)
        except Exception:
            label_font_tuple = ("Arial", 16)

        self.lives_label = tk.Label(self.root, text=f"LIVES: {self.lives}", font=label_font_tuple, fg="lime green",
                                    bg="#313131")
        self.lives_label.place(x=10, y=10)

        self.score_label = tk.Label(self.root, text=f"SCORE: {self.score}", font=label_font_tuple, fg="lime green",
                                    bg="#313131")
        self.score_label.place(x=10, y=40)
        self.root.config(bg="#313131")  # Устанавливаем общий фон для окна

        # подключение класса с начальным фоном
        self.back_asteroids = BackAsteroids(self.canvas)

    def update_score(self, add_score):
        self.score += add_score
        self.score_label.config(text=f"SCORE: {self.score}")

    def update_lives(self, change_lives):
        self.lives += change_lives
        self.lives_label.config(text=f"LIVES: {self.lives}")
        if self.lives <= 0:
            self.game_over()

    def game_over(self):
        """Показывает экран 'Game Over' и кнопку 'Начать сначала'."""
        # Уничтожаем старые элементы
        self.clear_canvas(False)
        # Создаем и размещаем надпись "Game Over"
        try:
            game_over_font = ImageFont.truetype(BUTTON_FONT, 48)
            game_over_font_tuple = (game_over_font.font.family, game_over_font.size)
        except Exception:
            game_over_font_tuple = ("Arial", 48)

        self.game_over_label = tk.Label(self.root, text="GAME OVER", font=game_over_font_tuple, fg="red", bg="black")
        game_over_x = (WINDOW_WIDTH - self.game_over_label.winfo_reqwidth()) // 2
        game_over_y = (WINDOW_HEIGHT - self.game_over_label.winfo_reqheight()) // 2 - 20
        self.game_over_label.place(x=game_over_x, y=game_over_y)

        # Создаем и размещаем кнопку "Начать сначала"
        self.restart_button_image = self.create_button_image("RESTART", BUTTON_FONT, BUTTON_COLOR, BUTTON_BORDER_COLOR)
        self.restart_button = tk.Button(self.root, image=self.restart_button_image, command=self.restart_game,
                                        borderwidth=0,
                                        highlightthickness=0, relief=tk.FLAT)
        restart_button_x = (WINDOW_WIDTH - self.restart_button_image.width()) // 2
        restart_button_y = game_over_y + self.game_over_label.winfo_reqheight() + 20
        self.restart_button.place(x=restart_button_x, y=restart_button_y)

    def restart_game(self):
        """Перезапускает игру."""
        self.score = SCORE_DEFAULT  # Сначала нужно сбросить счет
        self.lives = LIVES_DEFAULT  # <---- устанавливаем начальное кол-во жизней
        self.game_over_label.destroy()
        self.restart_button.destroy()
        self.clear_canvas()

    def clear_canvas(self, start_game=True):
        if start_game:
            for asteroid_data in self.back_asteroids.asteroids:
                self.canvas.delete(asteroid_data["id"])
            self.button.destroy()
            self.lives_label.destroy()
            self.score_label.destroy()
            self.title_label.destroy()

            try:
                label_font = ImageFont.truetype(BUTTON_FONT, 16)
                label_font_tuple = (label_font.font.family, label_font.size)
            except Exception:
                label_font_tuple = ("Arial", 16)

            # создаем новую метку score
            self.score_label = tk.Label(self.root, text=f"SCORE: {self.score}", font=label_font_tuple, fg="lime green",
                                        bg="#313131")
            self.score_label.place(x=10, y=40)

            self.lives_label = tk.Label(self.root, text=f"LIVES: {self.lives}", font=label_font_tuple, fg="lime green",
                                        bg="#313131")
            self.lives_label.place(x=10, y=10)

            self.back_asteroids.asteroids = []  # Очистим список астероидов
            self.back_asteroids.create_asteroids()  # Создадим астероиды для игрового режима
            self.rocket = Rocket(self.canvas, self.back_asteroids, self)  # Создаем ракету
            self.canvas.focus_set()
        else:
            for asteroid_data in self.back_asteroids.asteroids:
                self.canvas.delete(asteroid_data["id"])
            try:
                self.rocket.canvas.delete(self.rocket.rocket_id)  # убираем ракету с экрана
            except AttributeError:
                pass

    def create_button_image(self, text, font_name, text_color, border_color):
        # Создаем PIL изображение для кнопки
        button_width = 200
        button_height = 60
        image = Image.new("RGBA", (button_width, button_height), (0, 0, 0, 0))  # Прозрачный фон
        draw = ImageDraw.Draw(image)

        # Рисуем рамку
        draw.rectangle((5, 5, button_width - 5, button_height - 5), outline=border_color, width=2)

        # Загрузка шрифта и вычисление размеров текста
        try:
            font = ImageFont.truetype(font_name, 24)  # Указываем шрифт и размер
        except Exception:
            font = ImageFont.load_default()

        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        text_x = (button_width - text_width) // 2
        text_y = (button_height - text_height) // 2

        # Рисуем текст
        draw.text((text_x, text_y), text, font=font, fill=text_color)

        # Делаем кнопку полупрозрачной
        alpha = 200  # Полупрозрачность (0 - прозрачный, 255 - непрозрачный), увеличили до 200
        image = image.convert("RGBA")  # Convert to RGBA to use transparency
        for x in range(image.width):
            for y in range(image.height):
                r, g, b, a = image.getpixel((x, y))
                if a > 0:  # Do not modify fully transparent pixels
                    image.putpixel((x, y), (r, g, b, alpha))

        return ImageTk.PhotoImage(image)