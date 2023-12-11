import tkinter as tk
from tkinter import ttk

def run_nn_inference_window():
    root = tk.Tk()
    root.geometry("600x400")
    root.title("Запуск нейросети")

    main_menu = tk.Menu(root)
    root.config(menu=main_menu)

    file_menu = tk.Menu(main_menu, tearoff=0)
    file_menu.add_command(label="Добавить видео")
    file_menu.add_command(label="Выбрать нейросеть")
    main_menu.add_cascade(label="Файл", menu=file_menu)
    
    lbl_save_option = tk.Label(root, text="Сохранить результаты в виде...")
    lbl_save_option.pack()

    cmb_save_options = ttk.Combobox(
        root, 
        state="readonly",
        values=[
            "Файл разметки json",
            "Файл разметки csv",
            "Файл разметки h5",
            "Видео с разметкой",
            "Кадры с разметкой",
        ]
    )
    cmb_save_options.current(0)
    cmb_save_options.pack()

    lbl_save_name = tk.Label(root, text="Название файла (каталога при сохранении кадров)")
    lbl_save_name.pack()
    ent_save_name = tk.Entry(root)
    ent_save_name.pack()

    lbl_save_path = tk.Label(root, text="Сохранить в...")
    lbl_save_path.pack()
    ent_save_path = tk.Entry(root)
    ent_save_path.pack()

    root.mainloop()