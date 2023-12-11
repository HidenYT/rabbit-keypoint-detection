import tkinter as tk
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)
from video_labeling import run_video_labeling
from nn_learning import run_nn_learning_window
from nn_inference import run_nn_inference_window


root = tk.Tk()
root.geometry("600x400")
root.title("Animal keypoint detector")

main_menu = tk.Menu(root)
root.config(menu=main_menu)

file_menu = tk.Menu(main_menu, tearoff=0)
file_menu.add_command(label="Разметить видео", command=run_video_labeling)
file_menu.add_command(label="Обучить нейросеть", command=run_nn_learning_window)
file_menu.add_command(label="Запустить обученную нейросеть", command=run_nn_inference_window)

main_menu.add_cascade(label="Файл", menu=file_menu)

root.mainloop()