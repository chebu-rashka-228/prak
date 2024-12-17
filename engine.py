import tkinter as tk
import math
from PIL import Image, ImageTk
import random
from CONST import *


class Asteroids:  # Пример базового класса Asteroids
    def __init__(self, c):
        self.c = c
        self.asteroid_big_size = ASTEROID_BIG_SIZE
        self.asteroid_small_size = ASTEROID_SMALL_SIZE
        explosion_image = Image.open(PATH_EXPLOSION_IMAGE)
        explosion_image = explosion_image.resize((50, 50), Image.LANCZOS)
        self.explosion_image = ImageTk.PhotoImage(explosion_image)

        self.asteroid_images = [
            Image.open(PATH_ASTEROID1_IMAGE).resize(self.asteroid_big_size, Image.LANCZOS),
            Image.open(PATH_ASTEROID2_IMAGE).resize(self.asteroid_big_size, Image.LANCZOS)

        ]
        self.asteroids = []

    def create_asteroids(self):
        num_asteroids = 10  # Увеличиваем количество астероидов
        for i in range(num_asteroids):
            side = random.randint(0, 3)  # 0: top, 1: right, 2: bottom, 3: left
            if side == 0:  # Top side
                x = random.randint(0, self.c.winfo_width())
                y = -50  # Start above the canvas
            elif side == 1:  # Right side
                x = self.c.winfo_width() + 50
                y = random.randint(0, self.c.winfo_height())
            elif side == 2:  # Bottom side
                x = random.randint(0, self.c.winfo_width())
                y = self.c.winfo_height() + 50
            else:  # Left side
                x = -50
                y = random.randint(0, self.c.winfo_height())

            angle = random.uniform(0, 2 * math.pi)
            rotation = random.uniform(-0.05, 0.05)
            speed = random.uniform(1, 3)
            image_index = random.randint(0, 1)

            asteroid_id = self.c.create_image(x, y,
                                              image=ImageTk.PhotoImage(self.asteroid_images[image_index]),
                                              anchor=tk.CENTER)

            self.asteroids.append({
                "id": asteroid_id,
                "x": x,
                "y": y,
                "angle": angle,
                "rotation": rotation,
                "speed": speed,
                "image_index": image_index
            })


class BackAsteroids(Asteroids):
    def __init__(self, c):
        super().__init__(c)
        super().create_asteroids()
        self.rotated_images = [{}, {}]
        self.animate()

    def animate(self):
        canvas_width = self.c.winfo_width()
        canvas_height = self.c.winfo_height()

        for i, asteroid_data in enumerate(self.asteroids):
            x, y = self.move_asteroid(asteroid_data, canvas_width, canvas_height)
            self.c.coords(asteroid_data["id"], x, y)
            asteroid_data["x"], asteroid_data["y"] = x, y

            self.handle_collisions(i, asteroid_data)
            self.rotate_asteroid(asteroid_data)  # Вызываем rotation после обработки столкновений

        self.c.after(30, self.animate)

    def move_asteroid(self, asteroid_data, canvas_width, canvas_height):
        x = asteroid_data["x"]
        y = asteroid_data["y"]
        speed = asteroid_data["speed"]
        angle = asteroid_data["angle"]

        x -= speed * math.cos(angle)
        y -= speed * math.sin(angle)

        # Toroidal geometry
        x = x % canvas_width
        y = y % canvas_height

        return x, y

    def handle_collisions(self, i, asteroid_data):
        for j, other_asteroid_data in enumerate(self.asteroids):
            if i == j:
                continue  # Don't check collision with itself

            distance = self.distance(asteroid_data, other_asteroid_data)
            if distance < self.asteroid_big_size[0]:  # Check if distance is less than the diameter of an asteroid
                self.resolve_collision(asteroid_data, other_asteroid_data)

    def distance(self, asteroid1, asteroid2):
        x1, y1 = asteroid1["x"], asteroid1["y"]
        x2, y2 = asteroid2["x"], asteroid2["y"]
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def resolve_collision(self, asteroid1, asteroid2):
        dx = asteroid2["x"] - asteroid1["x"]
        dy = asteroid2["y"] - asteroid1["y"]
        distance = self.distance(asteroid1, asteroid2)

        # Normalize the vector
        dx /= distance
        dy /= distance

        # Adjust positions to prevent overlap
        overlap = (self.asteroid_big_size[0] - distance) / 2
        asteroid1["x"] -= dx * overlap
        asteroid1["y"] -= dy * overlap
        asteroid2["x"] += dx * overlap
        asteroid2["y"] += dy * overlap

        # Update angles to cause some deflection
        angle1_new = math.atan2(dy, dx)
        angle2_new = math.atan2(-dy, -dx)

        # Apply some small random rotation change to prevent repetition
        asteroid1["angle"] = angle1_new + random.uniform(-0.2, 0.2)
        asteroid2["angle"] = angle2_new + random.uniform(-0.2, 0.2)

        # Apply some speed changes
        speed_change = random.uniform(0.5, 1.5)
        asteroid1["speed"] *= speed_change
        asteroid2["speed"] *= speed_change
        # Ensure new speed is within a reasonable range
        asteroid1["speed"] = max(1, min(asteroid1["speed"], 5))
        asteroid2["speed"] = max(1, min(asteroid2["speed"], 5))

    def rotate_asteroid(self, asteroid_data):
        asteroid_data['angle'] += asteroid_data["rotation"]
        angle_degrees = math.degrees(asteroid_data['angle']) % 360
        self.c.itemconfig(asteroid_data['id'],
                          image=self.get_rotated_image(angle_degrees, asteroid_data['image_index']))

    def get_rotated_image(self, angle, image_index):
        if angle not in self.rotated_images[image_index]:
            rotated_pil_image = self.asteroid_images[image_index].copy().rotate(angle)
            self.rotated_images[image_index][angle] = ImageTk.PhotoImage(rotated_pil_image)
            # Limit the size of rotated_images by removing the oldest entry
            if len(self.rotated_images[image_index]) > 20:
                oldest_angle = list(self.rotated_images[image_index].keys())[0]
                del self.rotated_images[image_index][oldest_angle]
        return self.rotated_images[image_index][angle]

    def check_collision_with_bullet(self, bullet_x, bullet_y):
        for i, asteroid_data in enumerate(self.asteroids):
            distance = math.sqrt((bullet_x - asteroid_data["x"]) ** 2 + (bullet_y - asteroid_data["y"]) ** 2)
            if distance < self.asteroid_big_size[0] / 2:
                return i, True  # Возвращаем индекс пораженного астероида
        return None  # Если ни один астероид не поражен

    def remove_asteroid(self, index):
        try:
            self.c.delete(self.asteroids[index]["id"])
            del self.asteroids[index]
        except IndexError:
            pass  # Handle the case where the asteroid index is out of range (e.g., after remove).

    def check_collision(self, rocket_x, rocket_y, rocket_radius):
        """Checks if the rocket at (rocket_x, rocket_y) with radius rocket_radius collides with any asteroid and returns its index"""
        for i, asteroid_data in enumerate(self.asteroids):
            distance = math.sqrt((rocket_x - asteroid_data["x"]) ** 2 + (rocket_y - asteroid_data["y"]) ** 2)
            if distance < rocket_radius + self.asteroid_big_size[0] / 2:
                return i  # Collision detected, return asteroid index
        return None  # No collision

    def show_explosion(self, x, y):
        """Отображает взрыв на месте астероида и удаляет его через 0.7 секунды."""
        explosion_id = self.c.create_image(x, y, image=self.explosion_image, anchor=tk.CENTER)
        self.c.after(700, lambda: self.c.delete(explosion_id))