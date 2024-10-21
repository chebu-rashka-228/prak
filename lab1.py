import tkinter as tk
import math

root = tk.Tk()
c = tk.Canvas(root, width=600, height=600, bg="white")
c.pack()

ball = c.create_oval(295, 295, 305, 305, fill='green')
ball1 = c.create_oval(100, 100, 500, 500)
ugol = 0
direction = 1
speed = 1


def motion():
    global ugol
    ugol += speed * direction
    x = 300 + 200 * math.cos(math.radians(ugol))
    y = 300 + 200 * math.sin(math.radians(ugol))
    c.coords(ball, x - 5, y - 5, x + 5, y + 5)

    root.after(20, motion)


def change_direction():
    global direction
    direction *= -1


def change_speed_up():
    global speed
    speed += 1


def change_speed_down():
    global speed
    speed -= 1


direction_button = tk.Button(root,
                             text="Изменить направление",
                             command=change_direction)
direction_button.pack()

speed_up_button = tk.Button(root,
                            text="Быстрее",
                            command=change_speed_up)
speed_up_button.pack()

speed_down_button = tk.Button(root,
                              text="Медленнее",
                              command=change_speed_down)
speed_down_button.pack()

motion()

root.mainloop()
