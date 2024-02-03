import tkinter as tk
from tkinter import Misc
from typing import TYPE_CHECKING
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
        bbox1 = self.bbox(self.container)  # get image area
        # Remove 1 pixel shift at the sides of the bbox1
        bbox1 = (bbox1[0] + 1, bbox1[1] + 1, bbox1[2] - 1, bbox1[3] - 1)
        bbox2 = (self.canvasx(0),  # get visible area of the canvas
                 self.canvasy(0),
                 self.canvasx(self.winfo_width()),
                 self.canvasy(self.winfo_height()))
        #print(bbox1, bbox2)
        bbox = [min(bbox1[0], bbox2[0]), min(bbox1[1], bbox2[1]),  # get scroll region box
                max(bbox1[2], bbox2[2]), max(bbox1[3], bbox2[3])]
        #print(bbox)
        if bbox[0] == bbox2[0] and bbox[2] == bbox2[2]:  # whole image in the visible area
            bbox[0] = bbox1[0]
            bbox[2] = bbox1[2]
        if bbox[1] == bbox2[1] and bbox[3] == bbox2[3]:  # whole image in the visible area
            bbox[1] = bbox1[1]
            bbox[3] = bbox1[3]
        #self.configure(scrollregion=bbox)  # set scroll region
        x1 = max(bbox2[0] - bbox1[0], 0)  # get coordinates (x1,y1,x2,y2) of the image tile
        y1 = max(bbox2[1] - bbox1[1], 0)
        x2 = min(bbox2[2], bbox1[2]) - bbox1[0]
        y2 = min(bbox2[3], bbox1[3]) - bbox1[1]
        #print(x1, y1, x2, y2)
        if int(x2 - x1) > 0 and int(y2 - y1) > 0:  # show image if it in the visible area
            x = min(int(x2 / self.imscale), self.width)   # sometimes it is larger on 1 pixel...
            y = min(int(y2 / self.imscale), self.height)  # ...and sometimes not
            image = self.image.pil_image.crop((int(x1 / self.imscale), int(y1 / self.imscale), x, y))
            imagetk = ImageTk.PhotoImage(image.resize((int(x2 - x1), int(y2 - y1))))
            imageid = self.create_image(max(bbox2[0], bbox1[0]), max(bbox2[1], bbox1[1]),
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
                kpid = self.create_kp_on_position(labels[key])
                if np.isnan(labels[key][0]) or np.isnan(labels[key][1]):
                    kp_visible = False
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
    
    def get_containter_top_left(self) -> tuple[int, int]:
        return self.bbox(self.container)[:2]
    
    def create_kp_on_random_position(self) -> int:
        """Создаёт точку на случайной позиции. 
        
        Возвращает id точки"""
        from random import randint
        cont_x1, cont_y1, cont_x2, cont_y2 = self.bbox(self.container)
        r = int(self.KP_RADIUS*self.imscale)
        pos_x = randint(cont_x1+r, cont_x2-r)
        pos_y = randint(cont_y1+r, cont_y2-r)
        return self.create_kp_on_position((pos_x, pos_y))
    
    def create_kp_on_position(self, position: tuple[float, float]) -> int:
        """Создаёт точку на заданной позиции. 
        
        Возвращает id точки"""
        if np.isnan(position[0]) or np.isnan(position[1]):
            return self.create_text(0, 0, text="", tags=self.KP_TAG)
        return self.create_text(*position, text="", tags=self.KP_TAG)
    
    def toggle_kp_visibility(self, event):
        id = self.find_closest_kp(event.x, event.y, halo=LabelingCanvas.KP_RADIUS)
        if not id: return
        self.keypoint_manager.get_kp_by_id(id[0]).toggle_visibility()
        self.draw_skeleton_lines()