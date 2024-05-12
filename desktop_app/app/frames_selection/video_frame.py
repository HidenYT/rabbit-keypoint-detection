import tkinter as tk
from tkinter import ttk
from PIL import Image
from frames_selection.frames_selection_manager import FramesSelectionManager
from .video_frame_canvas import VideoFrameCanvas
from .video_frame_change_listener import VideoFrameChangeListener
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .frames_selection_controller import FramesSelectionController

class VideoFrame(tk.Frame):
    '''Фрейм, содержащий Canvas с кадрами из видео, и кнопки для управления видео:
    Пуск, Пауза, слайдер для перемотки. Также содержит кнопку для выбора кадра.'''
    FRAME_CHANGE_DELTA = 1

    def __init__(self, 
                 master,
                 controller: "FramesSelectionController", 
                 frame_selection_manager: "FramesSelectionManager",
                 frame_change_listener: VideoFrameChangeListener,
                 frames_n: int = 100, ):
        super().__init__(master)
        self.controller = controller
        self.frames_n = frames_n
        self.frame_selection_manager = frame_selection_manager
        self.frame_change_listener = frame_change_listener
        self.playing = False
        
        self.video_frame = self.setup_video_frame()
        self.bottom_bar = self.setup_bottom_bar()
        self.video_frame.pack(side='top', fill='both', expand=True)
        self.bottom_bar.pack(side='bottom', fill='x')
    
    def set_frames_n(self, frames_n: int):
        self.frames_n = frames_n
        self.slider.config(to=frames_n-1, value=0)

    def setup_video_frame(self) -> tk.Frame:
        '''Возвращает Canvas, отображающий текущий кадр видео.'''
        frm = tk.Frame(self)
        self.canvas = canvas = VideoFrameCanvas(frm)
        canvas.pack(fill='both', expand=True)
        return frm

    def setup_bottom_bar(self) -> tk.Frame:
        '''Возвращает Frame, хранящий кнопки управления видео.'''
        self.bottom_frame = frm = tk.Frame(self)
        self.frame_n_label = ttk.Label(frm, text="0", style="default.TLabel", anchor="center")
        self.frame_n_label.pack(fill='x')

        frm_controls = self.create_controls_frame(frm)
        frm_controls.pack(fill='x')

        frm_playpause = self.create_playpause_frame(frm)
        frm_playpause.pack(fill='x')

        return frm
    
    def create_controls_frame(self, root) -> tk.Frame:
        '''Возвращает фрейм, содержащий слайдер и кнопки для перемотки кадра на 1.'''
        frm = tk.Frame(root)
        self.btn_slider_left = ttk.Button(
            frm, 
            text="<", 
            command=lambda: self.move_video_pos(-self.FRAME_CHANGE_DELTA),
        )
        self.btn_slider_left.pack(side='left', fill='x')

        self.slider = slider = ttk.Scale(
            frm, 
            from_=0, 
            to=self.frames_n-1, 
            value=0,
            command=self.on_slider_move,
        )
        slider.bind("<ButtonRelease-1>", self.on_slider_changing_complete)
        slider.pack(fill='both', side='left', expand=True)
        
        self.btn_slider_right = ttk.Button(
            frm, 
            text=">", 
            command=lambda: self.move_video_pos(self.FRAME_CHANGE_DELTA),
        )
        self.btn_slider_right.pack(side='left', fill='x')
        return frm
    
    def create_playpause_frame(self, root) -> tk.Frame:
        '''Возвращает Frame, содержащий кнопки Пуск, Пауза, и кнопку для выбора кадра.'''
        frm = tk.Frame(root)
        frm.grid_columnconfigure(list(range(3)), weight=1, uniform="uniform")
        btn_play = ttk.Button(frm, text="Пуск", command=self.play_video, style="default.TButton")
        btn_pause = ttk.Button(frm, text="Пауза", command=self.pause_video, style="default.TButton")
        self.btn_select = tk.Button(frm, 
                                    text="Выбрать", 
                                    command=self.toggle_current_frame_selection,
                                    bg='red',
                                    relief='flat',
                                    padx=5,
                                    pady=5,
                                    font=('Helvetica', 10),
                                    borderwidth=1,)
        btn_play.grid(column=0, row=0, sticky="news")
        btn_pause.grid(column=1, row=0, sticky="news")
        self.btn_select.grid(column=2, row=0, sticky="news")
        return frm
    
    def on_slider_move(self, value):
        self.frame_n_label.config(text=str(int(round(self.slider.get()))))

    def on_slider_changing_complete(self, event):
        '''Функция, срабатывающая после того, как слайдер был отпущен, 
        то есть после окончательного изменения кадра видео.'''
        frame_n = int(round(float(self.slider.get())))
        if self.frame_change_listener is not None and not self.playing:
            self.frame_change_listener.on_video_frame_change_complete(frame_n)
        
    def play_video(self):
        '''Функция, начинающая проигрывать видео с текущего кадра.'''
        if self.playing: return
        if self.controller.video_capture is None: return 
        # Иначе всё работает, несмотря на ошибки
        delay = int(1000/self.controller.get_video_fps())
        
        def play():
            if not self.playing: return
            try:
                self.update_frame()
            except IndexError as e:
                print(e)
                self.pause_video()
                return
            self.master.after(delay, play)
        self.disable_control()
        self.playing = True
        play()

    def pause_video(self):
        '''Функция, ставящая воспроизведение видео на паузу.'''
        self.playing = False
        self.enable_control()
    
    def set_video_pos(self, pos: int):
        '''Устанавливает видео на определённый кадр №`pos`. Меняет информацию в `VideoCapture`, 
        а также в слайдере, тексте и кнопке выбора кадра.'''
        pos = max(0, min(pos, self.frames_n-1))
        self.slider.config(value=pos)
        self.on_slider_changing_complete(None)
    
    def move_video_pos(self, delta: int):
        '''Меняет текущий кадр на значение `delta`. Меняет информацию в `VideoCapture`, 
        а также в слайдере, тексте и кнопке выбора кадра. 
        
        Например, если текущий кадр равен 60, и `delta` равно -4, то текущий кадр видео
        станет 56.'''
        frame_n = self.controller.get_showing_frame_n()
        if frame_n is None: return
        self.set_video_pos(frame_n+delta)
    
    def disable_control(self):
        '''Отключает кнопки для изменения кадра на 1, а также слайдер.'''
        self.slider.config(state='disabled')
        self.btn_slider_left.config(state='disabled')
        self.btn_slider_right.config(state='disabled')
    
    def enable_control(self):
        '''Включает кнопки для изменения кадра на 1, а также слайдер.'''
        self.slider.config(state='normal')
        self.btn_slider_left.config(state='normal')
        self.btn_slider_right.config(state='normal')

    def toggle_current_frame_selection(self):
        '''Инвертирует выбор текущего кадра. Если кадр не выбран, он добавляется в список выбранных кадров. Иначе удаляется оттуда.'''
        frame_n = self.controller.get_showing_frame_n()
        if frame_n is None: return
        self.frame_selection_manager.toggle(frame_n)
        self.update_select_button_bg()

    def update_select_button_bg(self):
        '''Обновляет фон кнопки выбора кадра'''
        frame_n = int(round(float(self.slider.get())))
        if self.frame_selection_manager.selected(frame_n):
            self.btn_select.config(bg='green', text="Выбран")
        else:
            self.btn_select.config(bg='red', text="Выбрать")
        
    def update_frame(self):
        '''Обновляет текущий кадр, отображаемый № кадра, позицию слайдера и цвет кнопки выбора кадра.'''
        if self.controller.get_showing_frame_n() is None: return
        self.canvas.set_image(self.controller.get_current_frame())
        frame_n = int(self.controller.get_showing_frame_n())
        self.slider.config(value=frame_n)
        self.frame_n_label.config(text=str(frame_n))
        self.update_select_button_bg()