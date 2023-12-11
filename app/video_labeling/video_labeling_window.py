import tkinter as tk

def run_video_labeling():
    root = tk.Tk()
    root.geometry("600x400")
    root.title("Разметка видео")

    main_menu = tk.Menu(root)
    root.config(menu=main_menu)

    file_menu = tk.Menu(main_menu, tearoff=0)
    file_menu.add_command(label="Выбрать кадры вручную")
    file_menu.add_command(label="Автоматический выбор кадров")
    file_menu.add_command(label="Добавить скелет")
    file_menu.add_command(label="Создать скелет")
    file_menu.add_command(label="Сохранить скелет")
    file_menu.add_command(label="Сохранить всё")
    file_menu.add_command(label="Сохранить кадры")
    file_menu.add_command(label="Сохранить разметку json")
    file_menu.add_command(label="Сохранить разметку csv")
    file_menu.add_command(label="Сохранить разметку h5")
    main_menu.add_cascade(label="Файл", menu=file_menu)

    # settings_menu = tk.Menu(main_menu)
    # settings_menu.add_command(label="Добавить видео")
    # settings_menu.add_command(label="Добавить скелет")
    # settings_menu.add_command(label="Создать скелет")
    # main_menu.add_cascade(label="Настройки", menu=file_menu)

    
    root.mainloop()
