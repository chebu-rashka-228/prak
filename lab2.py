import tkinter as tk
import math
import random
from tkinter import RIGHT, LEFT, TOP

step_size = 1
gravitaion = 0.0
priority_direction = 90
x, y = 500, 300

root = tk.Tk()
root.title("Пьяная точка")
c = tk.Canvas(root, width=1000, height=600, bg='black')
c.pack()


def motion():
    global gravitaion, priority_direction, step_size, x, y
    random_angle = random.uniform(0, 2 * math.pi)
    angle = (1 - gravitaion) * random_angle + gravitaion * priority_direction
    x += step_size * math.cos(angle)
    y += step_size * math.sin(angle)
    last_x, last_y = x, y
    c.create_oval(last_x, last_y, x, y, fill='white')

    if x < 0:
        x = 0
    if x > 800:
        x = 800
    if y < 0:
        y = 0
    if y > 600:
        y = 600

    root.after(200, motion)


def update_step_size(val):
    global step_size
    step_size = int(val)


def update_gravitaion(val):
    global gravitaion
    gravitaion = float(val)


def update_priority_direction(val):
    global priority_direction
    priority_direction = int(val)


step_size_label = tk.Label(root, text="Слайдер шага")
step_size_label.pack()
step_size_scale = tk.Scale(root,
                           from_=0,
                           to=10,
                           resolution=1,
                           relief="solid",
                           orient=tk.HORIZONTAL,
                           command=update_step_size)
step_size_scale.set(0)
step_size_scale.pack(side=TOP, padx=300)

gravity_label = tk.Label(root, text="Сладер гравитации")
gravity_label.pack(side=LEFT, padx=5, pady=5)
gravity = tk.Scale(root,
                   from_=0,
                   to=1,
                   resolution=0.01,
                   relief="solid",
                   orient=tk.HORIZONTAL,
                   command=update_gravitaion)
gravity.set(0.0)
gravity.pack(side=LEFT, padx=5, pady=5)

priority_direction_label = tk.Label(root, text="Слайдер направления")
priority_direction_label.pack(side=RIGHT, padx=5)
priority_direction_scale = tk.Scale(root,
                                    from_=0,
                                    to=360,
                                    relief="solid",
                                    orient=tk.HORIZONTAL,
                                    command=update_priority_direction)
priority_direction_scale.set(90)
priority_direction_scale.pack(side=RIGHT, padx=5)

motion()
root.mainloop()
