import tkinter as tk
from PIL import Image, ImageTk
import math
import time
from CONST import *


class Rocket:
    def __init__(self, canvas, back_asteroids, start_window):
        # Ваш код __init__
        self.canvas = canvas
        self.back_asteroids = back_asteroids
        self.start_window = start_window
        self.last_shot_time = 0
        self.reload_time = 0.3
        self.bullets = []
        bullet_image = Image.open(PATH_BULLET_IMAGE)
        bullet_image = bullet_image.resize((10, 10), Image.LANCZOS)
        self.bullet_image = ImageTk.PhotoImage(bullet_image)
        self.x = WINDOW_WIDTH // 2
        self.y = WINDOW_HEIGHT - 50
        self.width = 50
        self.height = 50
        self.angle = 0
        rocket_image = Image.open(PATH_ROCKET_IMAGE)
        rocket_image = rocket_image.resize((50, 50), Image.LANCZOS)
        self.rocket_image = ImageTk.PhotoImage(rocket_image)
        self.rocket_id = self.canvas.create_image(self.x, self.y, image=self.rocket_image, anchor=tk.CENTER)

        self.is_moving = False  # Отслеживание движения
        self.fire_animation_id = None  # Для анимации огня
        self.current_rocket_image_index = 0  # Текущий индекс изображения
        self.speed = 5  # <-------------------- Инициализация speed
        self.rocket_images_pil = [
            Image.open(PATH_ROCKET_IMAGE).resize((50, 50)),
            Image.open(PATH_ROCKET_FIRE_IMAGE).resize((50, 50))
        ]
        self.rotated_images = [{}, {}]
        self.pressed_keys = set()  # Отслеживаем нажатые клавиши

        self.inertia_speed = 0  # Скорость для инерции
        self.inertia_decay = 0.95  # Коэффициент затухания инерции

        # Привязываем события key press and release
        self.canvas.bind_all("<KeyPress>", self.on_key_press)
        self.canvas.bind_all("<KeyRelease>", self.on_key_release)

        self.animate()  # Запускаем анимацию
        self.update()  # Запускаем цикл обработки нажатий

    def on_key_press(self, event):
        self.pressed_keys.add(event.keysym)

    def on_key_release(self, event):
        if event.keysym in self.pressed_keys:
            self.pressed_keys.remove(event.keysym)
            if event.keysym == "Up":  # Если отпустили кнопку вверх
                self.inertia_speed = self.speed  # Передаем текущую скорость в инерцию

    def update(self):
        if "Left" in self.pressed_keys:
            self.angle += 5
        if "Right" in self.pressed_keys:
            self.angle -= 5

        if "Up" in self.pressed_keys:
            self.start_fire()
            dx = self.speed * math.cos(math.radians(self.angle - 270))
            dy = self.speed * math.sin(math.radians(self.angle - 270))
            self.x += dx
            self.y -= dy

            # Проверка границ экрана
            if self.x < 0:
                self.x = 0
            elif self.x > self.canvas.winfo_width():
                self.x = self.canvas.winfo_width()
            if self.y < 0:
                self.y = 0
            elif self.y > self.canvas.winfo_height():
                self.y = self.canvas.winfo_height()
        else:
            self.stop_fire(None)

        # Обработка инерции
        if self.inertia_speed > 0.1:  # Проверяем чтобы скорость инерции была не сильно малой
            dx = self.inertia_speed * math.cos(math.radians(self.angle - 270))
            dy = self.inertia_speed * math.sin(math.radians(self.angle - 270))
            self.x += dx
            self.y -= dy

            # Проверка границ экрана
            if self.x < 0:
                self.x = 0
            elif self.x > self.canvas.winfo_width():
                self.x = self.canvas.winfo_width()
            if self.y < 0:
                self.y = 0
            elif self.y > self.canvas.winfo_height():
                self.y = self.canvas.winfo_height()

            self.inertia_speed *= self.inertia_decay  # уменьшаем скорость инерции

        self.update_rocket_position()

        if "space" in self.pressed_keys:
            self.shoot(None)

        self.canvas.after(20, self.update)  # Вызываем update каждые 20 миллисекунд

    def check_collisions(self):
        """Проверяет столкновения с астероидами и удаляет их при необходимости."""
        if not hasattr(self, 'rocket_id'): return  # Если ракета не создана, выходим из метода
        asteroid_index = self.back_asteroids.check_collision(self.x, self.y, self.width / 2)
        if asteroid_index is not None:
            self.start_window.update_lives(-1)
            self.x = WINDOW_WIDTH // 2
            self.y = WINDOW_HEIGHT - 50
            self.inertia_speed = 0
            asteroid_data = self.back_asteroids.asteroids[asteroid_index]  # Получаем астероид, перед удалением
            self.back_asteroids.show_explosion(asteroid_data["x"], asteroid_data["y"])
            self.back_asteroids.remove_asteroid(asteroid_index)  # Удаляем астероид

    def update_rocket_position(self):
        rotated_image = self.get_rotated_image(self.angle, self.current_rocket_image_index)
        self.canvas.itemconfig(self.rocket_id, image=rotated_image)
        x_offset = self.width / 2 * math.cos(math.radians(self.angle))
        y_offset = self.width / 2 * math.sin(math.radians(self.angle))
        self.canvas.coords(self.rocket_id, self.x - x_offset, self.y + y_offset)

    def get_rotated_image(self, angle, image_index):
        if angle not in self.rotated_images[image_index]:
            rotated_pil_image = self.rocket_images_pil[image_index].copy().rotate(angle)
            self.rotated_images[image_index][angle] = ImageTk.PhotoImage(rotated_pil_image)
        return self.rotated_images[image_index][angle]

    def start_fire(self):
        if not self.is_moving:
            self.is_moving = True
            self.current_rocket_image_index = 1  # Изображение с огнём
            self.update_rocket_position()

    def stop_fire(self, event):
        self.is_moving = False
        self.current_rocket_image_index = 0  # Обычное изображение ракеты
        self.update_rocket_position()

    def shoot(self, event):
        current_time = time.time()
        if current_time - self.last_shot_time > self.reload_time:
            bullet_x = self.x + 25 * math.cos(math.radians(self.angle - 270))
            bullet_y = self.y - 25 * math.sin(math.radians(self.angle - 270))
            bullet_id = self.canvas.create_image(bullet_x, bullet_y, image=self.bullet_image, anchor=tk.CENTER)
            self.bullets.append({"id": bullet_id, "x": bullet_x, "y": bullet_y, "angle": self.angle - 270})
            self.last_shot_time = current_time

    def animate(self):
        self.check_collisions()  # Check collisions first
        self.move_bullets()  # Двигаем пули
        self.check_bullet_collisions()  # Проверяем попадания
        self.canvas.after(30, self.animate)

    def move_bullets(self):
        for bullet in self.bullets:
            speed = 10
            bullet["x"] += speed * math.cos(math.radians(bullet["angle"]))
            bullet["y"] -= speed * math.sin(math.radians(bullet["angle"]))
            self.canvas.move(bullet["id"], speed * math.cos(math.radians(bullet["angle"])),
                             -speed * math.sin(math.radians(bullet["angle"])))

    def check_bullet_collisions(self):
        bullets_to_remove = []
        for bullet_index, bullet in enumerate(self.bullets):
            collision_result = self.back_asteroids.check_collision_with_bullet(bullet["x"], bullet["y"])
            if collision_result is not None:
                asteroid_index, remove_bullet = collision_result
                if remove_bullet:
                    try:
                        self.canvas.delete(bullet["id"])
                        bullets_to_remove.append(bullet_index)
                    except ValueError:
                        pass
                    asteroid_data = self.back_asteroids.asteroids[asteroid_index]
                    self.back_asteroids.show_explosion(asteroid_data["x"], asteroid_data["y"])
                    self.back_asteroids.remove_asteroid(asteroid_index)
                    self.start_window.update_score(50)  # Обновляем score
        for index in sorted(bullets_to_remove, reverse=True):
            del self.bullets[index]