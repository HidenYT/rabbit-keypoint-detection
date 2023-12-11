import tkinter as tk
from tkinter import ttk

def run_nn_learn_settings_window():
    root = tk.Tk()
    root.title("Настройки обучения")
    
    nn_select_list = ttk.Combobox(
        state="readonly",
        values=[
            "DeepLabCut", 
            "SLEAP", 
            "DeepPoseKit",
            "Self-made NN",
        ],
        master=root,
    )
    nn_select_list.current(0)
    nn_select_list.pack()
    test_btn1 = tk.Checkbutton(text="Опция 1", master=root)
    test_btn1.pack()

    test_label = tk.Label(text="Learning rate")
    test_entry = tk.Entry()

    root.mainloop()