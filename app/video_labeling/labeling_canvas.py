import tkinter as tk
from tkinter import Misc
from typing import Dict
from core.models.image import ImageFile
from PIL import ImageTk
from core.models.skeleton import Skeleton, SkeletonNode
from .keypoints import Keypoint, KeypointManager

class LabelingCanvas(tk.Canvas):
    KP_TAG = "keypoint"
    SKELETON_LINE_TAG = "skeleton_line"
    KP_RADIUS = 10

    def __init__(self, master: Misc | None, image: ImageFile) -> None:
        super().__init__(master, bg="#ffffff")
        # TODO Сделать так, чтобы вершины можно было делать невидимыми

        # Zoom изображения и перемещение по нему
        self.bind("<Control-MouseWheel>", self.on_zoom)
        self.bind('<ButtonPress-3>', self.on_mouse_rb_press)
        self.bind("<B3-Motion>", self.on_mouse_rb_move)

        # Перемещение точек
        self.bind('<ButtonPress-1>', self.on_press_to_move)
        self.bind("<B1-Motion>", self.on_mous_lb_move)
        self.bind("<ButtonRelease-1>", self.on_mouse_lb_release)

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

        self.bind("<Configure>", lambda x: self.update_image())

    # def update_image(self):
    #     pil_img = self.image.pil_image
    #     w, h = pil_img.size
    #     new_size = (int(w*self.imscale), int(h*self.imscale))
    #     img = pil_img.resize(new_size)
    #     self.imagetk = ImageTk.PhotoImage(img)
    #     self.img_id = self.create_image(self.coords(self.text), anchor='nw', image=self.imagetk)
    #     self.lower(self.img_id)
        
    def find_closest_kp(self, x, y, halo = None) -> tuple[int, ...]:
        x, y = self.canvasx(x), self.canvasy(y)
        objects = self.find_withtag(self.KP_TAG)
        def dist(kpid):
            coords_kp = Keypoint.get_coordinates_from_bbox(self.bbox(kpid))
            return ((coords_kp[0]-x)**2 + (coords_kp[1]-y)**2)**0.5
        s = sorted(objects, key=dist)
        if s:
            closest = s[0]
            if dist(closest) <= halo*self.imscale:
                return tuple([s[0]])
        return tuple()
        
    def on_zoom(self, event):
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)
        factor = 1.001 ** event.delta
        self.scale(tk.ALL, x, y, factor, factor)
        self.imscale *= factor
        self.update_image()

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
        
    def set_skeleton(self, skeleton: Skeleton):
        self.skeleton = skeleton
        for id in self.keypoint_manager.get_kp_ids():
            self.delete(id)
        for id in self.keypoint_manager.get_text_ids():
            self.delete(id)
        self.keypoint_manager.set_skeleton(skeleton)
        self.keypoint_manager.clear()
        
        for key in skeleton.nodes:
            kpid, text_id = self.create_kp_on_random_position(key)
            self.keypoint_manager.add_keypoint(kpid, key)
            self.keypoint_manager.add_kp_text(kpid, text_id)
        self.draw_skeleton_lines()
    
    def draw_skeleton_lines(self):
        if self.skeleton is None: return
        self.delete(self.SKELETON_LINE_TAG)
        for kpid in self.keypoint_manager.get_kp_ids():
            kp = self.keypoint_manager.get_kp_by_id(kpid)
            parent_node = kp.skeleton_node.parent
            if parent_node is None: continue
            parent_id = self.keypoint_manager.get_id_by_name(parent_node.name)

            x1, y1 = Keypoint.get_coordinates_from_bbox(self.bbox(kpid))
            x2, y2 = Keypoint.get_coordinates_from_bbox(self.bbox(parent_id))
            self.create_line(x1, y1, x2, y2, tags=self.SKELETON_LINE_TAG)

    def on_press_to_move(self, event):
        id = self.find_closest_kp(event.x, event.y, halo = 10)
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

    def on_mous_lb_move(self, event):
        if self.drag_widget is None: return
        if self.drag_widget not in self.keypoint_manager.get_kp_ids(): return

        delta_x = event.x - self.drag_x
        delta_y = event.y - self.drag_y
        self.drag_x = event.x
        self.drag_y = event.y
        self.move(self.drag_widget, delta_x, delta_y)
        self.move(self.keypoint_manager.get_text_id_by_kp_id(self.drag_widget), delta_x, delta_y)
        self.draw_skeleton_lines()
    
    def get_containter_top_left(self) -> tuple[int, int]:
        return self.bbox(self.container)[:2]
    
    def create_kp_on_random_position(self, key: str) -> tuple[int, int]:
        """Создаём точку на случайной позиции со случайным цветом. 
        
        Возвращает id точки и текста"""
        from random import randint
        cont_x1, cont_y1, cont_x2, cont_y2 = self.bbox(self.container)
        r = int(self.KP_RADIUS*self.imscale)
        pos_x = randint(cont_x1+r, cont_x2-r)
        pos_y = randint(cont_y1+r, cont_y2-r)
        col = lambda: randint(0,255)
        color = f'#{col():02X}{col():02X}{col():02X}'
        kpid = self.create_oval(pos_x-r, pos_y-r, pos_x+r, pos_y+r, fill=color, tags=self.KP_TAG)
        text_id = self.create_text(pos_x-r, pos_y-r, text=key)

        return kpid, text_id