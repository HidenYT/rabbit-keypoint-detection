from math import ceil, floor
import tkinter as tk
from tkinter import Misc
from typing import TYPE_CHECKING
from PIL import Image
import numpy as np
from core.models.image import ImageFile
from PIL import ImageTk
from core.models.skeleton import Skeleton
from .keypoints import KeypointManager

if TYPE_CHECKING:
    from .video_labeling_view import ImageButtonFrame

class LabelingCanvas(tk.Canvas):
    KP_TAG = "keypoint"
    KP_TEXT_TAG = "keypoint_text"
    KP_CIRCLE_TAG = "kp_circle"
    SKELETON_LINE_TAG = "skeleton_line"
    KP_RADIUS = 10

    def __init__(self, 
                 master: Misc | None, 
                 image: ImageFile) -> None:
        super().__init__(master, bg="#ffffff")

        # Zoom изображения и перемещение по нему
        self.bind("<Control-MouseWheel>", self.on_zoom)
        self.bind('<ButtonPress-3>', self.on_mouse_rb_press)
        self.bind("<B3-Motion>", self.on_mouse_rb_move)

        # Перемещение точек
        self.bind('<ButtonPress-1>', self.on_press_to_move)
        self.bind("<B1-Motion>", self.on_mouse_lb_move)
        self.bind("<ButtonRelease-1>", self.on_mouse_lb_release)

        # Изменение видимости точки
        self.bind("<ButtonPress-2>", self.toggle_kp_visibility)

        # Изображение Canvas-а
        self.image: ImageFile = image
        self.imagetk = None
        self.imscale = 1.0
        self.width, self.height = image.pil_image.size

        # Контейнер для вычисления координат Canvas-а
        self.container = self.create_rectangle(0, 0, self.width, self.height, width=0)
        
        # Скелет
        self.skeleton: Skeleton | None = None

        # Для перетаскивания точек
        self.drag_widget = None
        self.drag_x = 0
        self.drag_y = 0

        # Менеджер точек
        self.keypoint_manager = KeypointManager(self)
        
        # Связанный с данным холстом фрейм для открытия холста
        self.frm_image_button: ImageButtonFrame | None = None

        self.bind("<Configure>", lambda x: self.update_image())

    # def update_image(self):
    #     pil_img = self.image.pil_image
    #     w, h = pil_img.size
    #     new_size = (int(w*self.imscale), int(h*self.imscale))
    #     img = pil_img.resize(new_size)
    #     self.imagetk = ImageTk.PhotoImage(img)
    #     self.img_id = self.create_image(self.coords(self.text), anchor='nw', image=self.imagetk)
    #     self.lower(self.img_id)
        
    def find_closest_kp(self, x, y, halo) -> tuple[int, ...]:
        x, y = self.canvasx(x), self.canvasy(y)
        objects = self.find_withtag(self.KP_TAG)
        def dist(kpid):
            coords_kp = self.coords(kpid)
            return ((coords_kp[0]-x)**2 + (coords_kp[1]-y)**2)**0.5
        s = sorted(objects, key=dist)
        if s:
            closest = s[0]
            if dist(closest) <= halo:
                return tuple([s[0]])
        return tuple()
        
    def on_zoom(self, event):
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)
        factor = 1.001 ** event.delta
        self.scale(tk.ALL, x, y, factor, factor)
        self.imscale *= factor
        self.update_image()
        self.draw_skeleton_lines()

    def on_mouse_rb_press(self, event):
        self.scan_mark(event.x, event.y)
    
    def on_mouse_rb_move(self, event):
        self.scan_dragto(event.x, event.y, gain=1)
        self.update_image()

    def update_image(self):
        bbox_container = self.coords(self.container)  # get image area
        # print(bbox1[2]-bbox1[0], self.width)
        # Remove 1 pixel shift at the sides of the bbox1
        bbox_container = (bbox_container[0] + 1, 
                          bbox_container[1] + 1, 
                          bbox_container[2] - 1, 
                          bbox_container[3] - 1)
        bbox_window = (self.canvasx(0),  # get visible area of the canvas
                 self.canvasy(0),
                 self.canvasx(self.winfo_width()),
                 self.canvasy(self.winfo_height()))
        #print(bbox1, bbox2)
        # bbox = [min(bbox1[0], bbox2[0]), min(bbox1[1], bbox2[1]),  # get scroll region box
        #         max(bbox1[2], bbox2[2]), max(bbox1[3], bbox2[3])]
        # #print(bbox)
        # if bbox[0] == bbox2[0] and bbox[2] == bbox2[2]:  # whole image in the visible area
        #     bbox[0] = bbox1[0]
        #     bbox[2] = bbox1[2]
        # if bbox[1] == bbox2[1] and bbox[3] == bbox2[3]:  # whole image in the visible area
        #     bbox[1] = bbox1[1]
        #     bbox[3] = bbox1[3]
        # #self.configure(scrollregion=bbox)  # set scroll region
        top_left_x = max(bbox_window[0] - bbox_container[0], 0)
        top_left_y = max(bbox_window[1] - bbox_container[1], 0)
        bottom_right_x = min(bbox_window[2], bbox_container[2]) - bbox_container[0]
        bottom_right_y = min(bbox_window[3], bbox_container[3]) - bbox_container[1]
        crop_top_left_x = ((floor(top_left_x / self.imscale)-1)/self.width)*(bbox_container[2]-bbox_container[0])+bbox_container[0]
        crop_top_left_y = ((floor(top_left_y / self.imscale)-1)/self.height)*(bbox_container[3]-bbox_container[1])+bbox_container[1]
        crop_bottom_right_x = (ceil(bottom_right_x / self.imscale)/self.width)*(bbox_container[2]-bbox_container[0])+bbox_container[0]
        crop_bottom_right_y = (ceil(bottom_right_y / self.imscale)/self.height)*(bbox_container[3]-bbox_container[1])+bbox_container[1]
        bbox_window = (crop_top_left_x, crop_top_left_y, crop_bottom_right_x, crop_bottom_right_y)
        
        top_left_x = max(bbox_window[0] - bbox_container[0], 0) 
        top_left_y = max(bbox_window[1] - bbox_container[1], 0)
        bottom_right_x = min(bbox_window[2], bbox_container[2]) - bbox_container[0]
        bottom_right_y = min(bbox_window[3], bbox_container[3]) - bbox_container[1]
        if int(bottom_right_x - top_left_x) > 0 and int(bottom_right_y - top_left_y) > 0:
            x = min(int(bottom_right_x / self.imscale)+1, self.width)
            y = min(int(bottom_right_y / self.imscale)+1, self.height)
            image = self.image.pil_image.crop((ceil(top_left_x / self.imscale), ceil(top_left_y / self.imscale), x, y))
            imagetk = ImageTk.PhotoImage(image.resize((ceil(bottom_right_x - top_left_x), ceil(bottom_right_y - top_left_y)), resample=Image.NEAREST))
            imageid = self.create_image(max(bbox_window[0], bbox_container[0])+0.5*self.imscale, max(bbox_window[1], bbox_container[1])+0.5*self.imscale,
                                               anchor='nw', image=imagetk)
            self.lower(imageid)  # set image into background
            self.imagetk = imagetk  # keep an extra reference to prevent garbage-collection
        
    def set_skeleton(self, skeleton: Skeleton, 
                     labels: dict[str, tuple[float, float]] | None = None):
        '''Устанавливает скелет, используемый для разметки изображения на холсте.
        После установки скелета на холсте создаются точки в соответствии со 
        скелетом. При отсутствии `labels` точки будут иметь случайные координаты.

        - `labels` - словарь, содержащий позиции для создаваемых точек.'''
        # Удаляем старые keypoint-ы
        for id in self.keypoint_manager.get_kp_ids(): self.delete(id)
        # Устанавливаем новый скелет, меняем его в менеджере точек
        self.skeleton = skeleton
        self.keypoint_manager.set_skeleton(skeleton)
        self.keypoint_manager.clear()
        
        # Генерируем создаём новые точки согласно скелету
        for key in skeleton.nodes:
            kp_visible = True
            if labels is None:
                kpid = self.create_kp_on_random_position()
            else:
                if np.isnan(labels[key][0]) or np.isnan(labels[key][1]):
                    kp_visible = False
                    kpid = self.create_kp_on_random_position()
                else:
                    kpid = self.create_kp_on_position(labels[key])
            kp = self.keypoint_manager.add_keypoint(kpid, key)
            if not kp_visible:
                kp.visible = False
        # Отрисовка
        self.draw_skeleton_lines()
    
    def draw_skeleton_lines(self):
        if self.skeleton is None: return
        self.delete(self.SKELETON_LINE_TAG)
        self.delete(self.KP_CIRCLE_TAG)
        self.delete(self.KP_TEXT_TAG)
        for kpid in self.keypoint_manager.get_kp_ids():
            kp = self.keypoint_manager.get_kp_by_id(kpid)
            x1, y1 = self.coords(kpid)
            color = "#00ff00" if kp.visible else "#ff0000"
            self.create_oval(x1-self.KP_RADIUS, y1-self.KP_RADIUS, x1+self.KP_RADIUS, y1+self.KP_RADIUS, fill=color, tags=self.KP_CIRCLE_TAG)
            
            self.create_text(x1-self.KP_RADIUS, y1-self.KP_RADIUS-10, text=kp.skeleton_node.name, font=("Helvetica", 10), tags=self.KP_TEXT_TAG, fill=color)

            parent_node = kp.skeleton_node.parent
            if parent_node is None: continue
            parent_id = self.keypoint_manager.get_id_by_name(parent_node.name)

            x2, y2 = self.coords(parent_id)
            self.create_line(x1, y1, x2, y2, tags=self.SKELETON_LINE_TAG)

    def on_press_to_move(self, event):
        id = self.find_closest_kp(event.x, event.y, halo=LabelingCanvas.KP_RADIUS)
        if not id: return
        id = id[0]
        # Сохраняем движимую точку и 
        self.drag_widget = id
        self.drag_x = event.x
        self.drag_y = event.y

    def on_mouse_lb_release(self, event):
        self.drag_widget = None
        self.drag_x = 0
        self.drag_y = 0

    def on_mouse_lb_move(self, event):
        if self.drag_widget is None: return
        if self.drag_widget not in self.keypoint_manager.get_kp_ids(): return

        delta_x = event.x - self.drag_x
        delta_y = event.y - self.drag_y
        self.drag_x = event.x
        self.drag_y = event.y
        self.move(self.drag_widget, delta_x, delta_y)
        self.draw_skeleton_lines()
    
    def get_containter_top_left(self) -> list[float]:
        return self.coords(self.container)[:2]
    
    def create_kp_on_random_position(self) -> int:
        """Создаёт точку на случайной позиции. 
        
        Возвращает id точки"""
        from random import randint
        cont_x1, cont_y1, cont_x2, cont_y2 = self.bbox(self.container)
        pos_x = randint((cont_x1*3+cont_x2)//4, (cont_x1+cont_x2*3)//4)
        pos_y = randint((cont_y1*3+cont_y2)//4, (cont_y1+cont_y2*3)//4)
        return self.create_kp_on_position((pos_x, pos_y))
    
    def create_kp_on_position(self, position: tuple[float, float]) -> int:
        """Создаёт точку на заданной позиции. 
        
        Возвращает id точки"""
        return self.create_text(*position, text="", tags=self.KP_TAG)
    
    def toggle_kp_visibility(self, event):
        id = self.find_closest_kp(event.x, event.y, halo=LabelingCanvas.KP_RADIUS)
        if not id: return
        self.keypoint_manager.get_kp_by_id(id[0]).toggle_visibility()
        self.draw_skeleton_lines()
    
    def pack_forget(self) -> None:
        super().pack_forget()
        self.image.close_pil_image()
        self.imagetk = None 
    
    def pack(self, *args, **kwargs):
        super().pack(*args, **kwargs)
        self.update_image()
    
    def destroy(self) -> None:
        super().destroy()
        self.imagetk = None 
        self.image.close_pil_image()