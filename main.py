import tkinter as tk
from start_window import StartWindow

def main():
    root = tk.Tk()
    root.title("АСТЕРОИДЫ")
    root.geometry("800x600")
    root.resizable(False, False)

    game = StartWindow(root) # Создаем экземпляр класса StartWindow, передавая root

    root.mainloop()

if __name__ == "__main__":
    main()