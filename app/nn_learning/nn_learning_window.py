import tkinter as tk
from .nn_learning_settings_window import run_nn_learn_settings_window

def run_nn_learning_window():
    root = tk.Tk()
    root.geometry("600x400")
    root.title("Обучение нейросети")

    main_menu = tk.Menu(root)
    root.config(menu=main_menu)

    file_menu = tk.Menu(main_menu, tearoff=0)
    file_menu.add_command(label="Выбрать папку с кадрами и разметкой")
    file_menu.add_command(label="Выбрать кадры для обучения")
    file_menu.add_command(label="Выбрать разметку для обучения")
    main_menu.add_cascade(label="Файл", menu=file_menu)

    main_menu.add_command(label="Настройки", command=run_nn_learn_settings_window)
    root.mainloop()