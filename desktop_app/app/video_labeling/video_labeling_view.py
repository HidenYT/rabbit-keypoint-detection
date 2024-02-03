from core.mvc.view import View
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from core.widgets.scrollable_frame import VerticalScrolledFrame
from .data_saving.label_saver import LabelSaver
from .labeling_canvas import LabelingCanvas
from core.models.image import ImageFile
from core.models.skeleton import Skeleton
from core.filetypes import csv_ft, png_ft, jpg_ft, images_ft, json_ft, hd5_ft, webp_ft, seven_z_ft

from typing import TYPE_CHECKING, Any, Callable, List
if TYPE_CHECKING:
    from .video_labeling_controller import LabelingController

class LabelingView(View["LabelingController"]):
    def __init__(self, controller: "LabelingController"):
        super().__init__(controller)
        self.setup_content_frame()
        # Список кнопок изображений
        self.img_buttons_list: List[tk.Button] = []

        # Список LabelinCanvas-ов. Каждый отвечает за своё изображение, хранит его разметку
        self.canvases: List[LabelingCanvas] = []

        # Открытый Canvas
        self.active_canvas: LabelingCanvas | None = None

        # Скелет
        self.skeleton: Skeleton | None = None
    
    def setup_content_frame(self):
        # Frame для LabelingCanvas, находится слева
        self.canvas_frame = tk.Frame(self)

        # Frame для всех настроек и кнопок, находится справа
        self.configuration_frame = tk.Frame(self)
        self.setup_config_frame()

        self.grid_columnconfigure(0, weight=3, uniform="uniform")
        self.grid_columnconfigure(1, weight=2, uniform="uniform")
        self.grid_rowconfigure(0, weight=1)
        self.canvas_frame.grid(row=0, column=0, sticky="nsew")
        self.configuration_frame.grid(row=0, column=1, sticky="nsew")

    def setup_config_frame(self):
        config_frame = self.configuration_frame

        # Frame для списка изображений, находится вверху
        self.images_list_frame = images_list = self.create_images_list_frame()
        self.total_images_number = 0

        # Frame для всех кнопок, находится внизу
        action_menu = self.create_action_menu()
        
        config_frame.grid_rowconfigure(0, weight=1, uniform="uniform")
        config_frame.grid_rowconfigure(1, weight=1, uniform="uniform")
        config_frame.grid_columnconfigure(0, weight=1, uniform="uniform")
        images_list.grid(row=0, column=0, sticky="news")
        action_menu.grid(row=1, column=0, sticky="news")


    def create_images_list_frame(self) -> VerticalScrolledFrame:
        config_frame = self.configuration_frame
        images_list = VerticalScrolledFrame(config_frame)
        #images_list.interior.grid_columnconfigure(0, weight=1, uniform="u")
        return images_list
    
    def add_image_to_images_list(self, 
                                 image_path: str, 
                                 labels: dict[str, tuple[float, float]] | None = None):
        # ImageFile и LabelingCanvas, хранящий изображение
        image = ImageFile(image_path)
        canvas = LabelingCanvas(self.canvas_frame, image)

        # Отображаем скелет, если он есть
        if self.skeleton is not None: canvas.set_skeleton(self.skeleton, labels)
        
        def delete_image(frame: ImageButtonFrame):
            frame.pack_forget()
            frame.destroy()
            self.canvases.remove(canvas)
            canvas.pack_forget()
            canvas.destroy()

        frm_image = ImageButtonFrame(self.images_list_frame.interior, 
                                     image_path, 
                                     lambda: self.show_canvas(canvas),
                                     delete_image)
        canvas.frm_image_button = frm_image

        # Добавляем всё в списки
        self.canvases.append(canvas)
        self.total_images_number += 1

        # Отображаем
        frm_image.pack(fill=tk.BOTH)

    def show_canvas(self, canvas: LabelingCanvas):
        """Открыть и показать заданный `LabelingCanvas` в `Frame`-е для `LabelingCanvas`-ов"""
        # Убираем старый Canvas
        if self.active_canvas is not None:
            self.active_canvas.pack_forget()
            self.active_canvas.frm_image_button.btn_image.config(bg="#f0f0f0")
        # Ставим переданный
        self.active_canvas = canvas
        self.active_canvas.frm_image_button.btn_image.config(bg="yellow")
        canvas.pack(fill=tk.BOTH, expand=True)

    def create_action_menu(self) -> tk.Frame:
        menu = tk.Frame(self.configuration_frame)
        btn_add_image = ttk.Button(menu, text="Добавить изображения", command=self.add_images)
        btn_choose_skeleton = ttk.Button(menu, text="Выбрать скелет", command=self.choose_skeleton)
        btn_save_labels = ttk.Button(menu, text="Сохранить разметку", command=self.save_labels)
        btn_open_labels = ttk.Button(menu, text="Открыть разметку", command=self.open_labels)
        btn_save_all_dataset = ttk.Button(menu, text="Сохранить датасет", command=self.save_dataset)
        btn_check_labels = ttk.Button(menu, text="Проверить разметку", command=self.check_labels)
        btn_add_image.pack(fill=tk.BOTH, side=tk.BOTTOM)
        btn_choose_skeleton.pack(fill=tk.BOTH, side=tk.BOTTOM)
        btn_save_all_dataset.pack(fill=tk.BOTH, side=tk.BOTTOM)
        btn_save_labels.pack(fill=tk.BOTH, side=tk.BOTTOM)
        btn_open_labels.pack(fill=tk.BOTH, side=tk.BOTTOM)
        btn_check_labels.pack(fill=tk.BOTH, side=tk.BOTTOM)
        return menu
    
    def open_labels(self):
        labels_file = filedialog.askopenfilename(
            defaultextension="", 
            filetypes=[csv_ft]
        )
        if not labels_file: return
        self.delete_all_images()
        df = self.controller.open_labels(labels_file)
        # Пути к файлам изображений
        images: list[str] = df[LabelSaver.IMAGE_PATH_COL].iloc[:, 0].to_list()
        # Добавляем каждое изображение
        for img_path in images:
            self.add_image_to_images_list(img_path)
        # Названия точек
        kp_names = set(index[0] for index in df.columns if index[0] != LabelSaver.IMAGE_PATH_COL)

        # Скелет, полученный из названий точек (не имеет связей между точками)
        skeleton = Skeleton.from_node_names(kp_names)

        # Каждому канвасу ставим свой скелет и устанавливаем координаты точек
        for i, canvas in enumerate(self.canvases):
            coordinates = {}
            for kp in kp_names:
                coordinates[kp] = tuple(df.loc[i, kp].to_list())
            canvas.set_skeleton(skeleton, coordinates)

    def delete_all_images(self):
        for canvas in self.canvases:
            canvas.destroy()
        self.canvases.clear()
        self.active_canvas = None
        self.total_images_number = 0
        for widget in list(self.images_list_frame.interior.children.values()):
            widget.destroy()

    def add_images(self):
        images = filedialog.askopenfilenames(filetypes=[images_ft, png_ft, jpg_ft, webp_ft])
        if not images: return
        for img_path in images:
            self.add_image_to_images_list(img_path)
        
    def choose_skeleton(self):
        skeleton = filedialog.askopenfile(
            defaultextension=".csv", 
            filetypes=[csv_ft]
        )
        if not skeleton: return
        self.skeleton = skeleton = self.controller.open_skeleton(skeleton)
        if skeleton is not None:
            for canvas in self.canvases:
                canvas.set_skeleton(skeleton)
    
    def save_labels(self):
        file = filedialog.asksaveasfilename(
            defaultextension="", 
            filetypes=[csv_ft, json_ft, hd5_ft]
        )
        if not file: return
        # Сохраняем отметки
        with CanvasScaler(self.canvases):
            self.controller.save_labels(self.canvases, file)
    
    def save_dataset(self):
        file = filedialog.asksaveasfilename(
            defaultextension="", 
            filetypes=[seven_z_ft, hd5_ft]
        )
        if not file: return
        # Сохраняем отметки
        with CanvasScaler(self.canvases):
            self.controller.save_dataset(self.canvases, file)
    
    def check_labels(self):
        if self.active_canvas is None: return
        import matplotlib.pyplot as plt
        with CanvasScaler(self.active_canvas):
            kps = self.active_canvas.keypoint_manager.get_keypoints_coordinates()
        x, y = [], []
        for f, s in kps.values():
            x.append(f)
            y.append(s)
        plt.imshow(self.active_canvas.image.pil_image)
        plt.scatter(x, y)
        plt.show()

class ImageButtonFrame(tk.Frame):
    def __init__(self, 
                 master, 
                 image_path: str, 
                 open_image_command: Callable,
                 close_callback: Callable[["ImageButtonFrame"], Any]):
        super().__init__(master)
        btn_image = self.btn_image = tk.Button(
            self, 
            text=f"{image_path}", 
            command=open_image_command,
            anchor="e",
        )
        btn_del = self.btn_del = tk.Button(
            self,
            text = "X",
            command=lambda:close_callback(self),
        )
        btn_del.pack(fill=tk.BOTH, side=tk.RIGHT)
        btn_image.pack(fill=tk.BOTH, side=tk.RIGHT,  expand=True)
    
class CanvasScaler:
    '''Менеджер контекста для изменения масштаба изображений при получении координат ключевых точек (при сохранении или проверке разметки).
    
    При сохранении разметки координаты точек сильно зависят от масштаба. Например, 
    если расставить точки и сильно отдалить изображение, то при сохранении все 
    точки будут иметь почти одинаковые координаты (так как при отдалении на самом
    деле меняется масштаб, а стало быть координаты становятся ближе друг к другу).
    
    Чтобы этого не происходило, перед сохранением масштаб изображения на Canvas
    делается таким, каким он был изначально. При этом после сохранения масштаб
    необходимо восстановить. 
    
    В начале менеджер контекста переводит изображения на всех Canvas-ах в исходный
    масштаб. По окончании возвращает масштаб таким, каким он был.'''
    def __init__(self, canvases: List[LabelingCanvas] | LabelingCanvas) -> None:
        if isinstance(canvases, LabelingCanvas): canvases = [canvases]
        self.__canvases = canvases 

    def __enter__(self):
        # Запоминаем текущий масштаб на каждом канвасе в список scales
        # и меняем масштаб на исходный, чтобы изображение было в исходную величину 
        self.__scales = scales = []
        for canvas in self.__canvases:
            s = canvas.imscale
            scales.append(canvas.imscale)
            canvas.scale(tk.ALL, 0, 0, 1/s, 1/s)
            canvas.imscale = 1
            canvas.update_image()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        # Возвращаем масштаб на каждом холсте, как было
        for i, canvas in enumerate(self.__canvases):
            canvas.scale(tk.ALL, 0, 0, self.__scales[i], self.__scales[i])
            canvas.imscale = self.__scales[i]
            canvas.update_image()