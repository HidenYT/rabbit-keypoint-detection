import tkinter as tk
from tkinter import Misc
from typing import Dict
from core.image import ImageFile
from PIL import ImageTk
from core.skeleton import Skeleton, SkeletonNode

class LabelingCanvas(tk.Canvas):
    KP_TAG = "keypoint"
    SKELETON_LINE_TAG = "skeleton_line"

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
        
        # Скелет и координаты его точек: id точки -> Keypoint
        self.skeleton: Skeleton | None = None
        self.keypoints: Dict[int, Keypoint] = {}
        self.keypoint_names: Dict[str, Keypoint] = {}
        self.keypoint_text: Dict[int, int] = {}

        # Для перетаскивания точек
        self.drag_widget = None
        self.drag_x = 0
        self.drag_y = 0

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
            coords_kp = self.bbox(kpid)
            coords_kp = [(coords_kp[0]+coords_kp[2])/2, (coords_kp[1]+coords_kp[3])/2]
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
        # kps = self.find_withtag(self.KP_TAG)
        # if kps:
        #     for kp in kps:
        #         bbox = self.bbox(kp)
        #         x, y = (bbox[0]+bbox[2])/2, (bbox[1]+bbox[3])/2
        #         self.scale(kp, x, y, 1/factor, 1/factor)
        #         self
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
        for id in self.keypoints:
            self.delete(id)
            self.delete(self.keypoint_text[id])
        self.keypoints = {}
        self.keypoint_names = {}
        self.keypoint_text = {}
        from random import randint
        cont_x1, cont_y1, cont_x2, cont_y2 = self.bbox(self.container)
        for key in skeleton.nodes:
            r = int(10*self.imscale)
            print(r)
            pos_x = randint(cont_x1+r, cont_x2-r)
            pos_y = randint(cont_y1+r, cont_y2-r)
            col = lambda: randint(0,255)
            color = f'#{col():02X}{col():02X}{col():02X}'
            kpid = self.create_oval(pos_x-r, pos_y-r, pos_x+r, pos_y+r, fill=color, tags=self.KP_TAG)
            text_id = self.create_text(pos_x-r, pos_y-r, text=key)
            self.keypoint_text[kpid] = text_id
            kp = Keypoint(key, (pos_x, pos_y), skeleton.nodes[key])
            self.keypoints[kpid] = kp
            self.keypoint_names[key] = kp
        self.draw_skeleton()
    
    def draw_skeleton(self):
        if self.skeleton is None: return
        self.delete(self.SKELETON_LINE_TAG)
        for kpid, kp in self.keypoints.items():
            p_bbox = self.bbox(kpid)
            x1, y1 = (p_bbox[0]+p_bbox[2])/2, (p_bbox[1]+p_bbox[3])/2
            parent_node = kp.skeleton_node.parent
            if parent_node is None:
                continue
            for parent_id in self.keypoints:
                if self.keypoints[parent_id].name == parent_node.name:
                    break
            parent_bbox = self.bbox(parent_id)
            x2, y2 = (parent_bbox[0]+parent_bbox[2])/2, (parent_bbox[1]+parent_bbox[3])/2
            self.create_line(x1, y1, x2, y2, tags=self.SKELETON_LINE_TAG)

    def on_press_to_move(self, event):
        id = self.find_closest_kp(event.x, event.y, halo = 10)
        if not id: return
        id = id[0]
        self.drag_widget = id
        self.drag_x = event.x
        self.drag_y = event.y

    def on_mouse_lb_release(self, event):
        self.drag_widget = None
        self.drag_x = 0
        self.drag_y = 0

    def on_mous_lb_move(self, event):
        if self.drag_widget is None: return
        if self.drag_widget not in self.keypoints: return

        delta_x = event.x - self.drag_x
        delta_y = event.y - self.drag_y
        self.drag_x = event.x
        self.drag_y = event.y
        self.move(self.drag_widget, delta_x, delta_y)
        self.move(self.keypoint_text[self.drag_widget], delta_x, delta_y)
        self.keypoints[self.drag_widget].coordinates = self.bbox(self.drag_widget)[:2]
        self.draw_skeleton()
        
    def get_keypoints_coordinates(self) -> Dict[str, tuple[float, float]]:
        result = {}
        for key in self.keypoint_names:
            result[key] = self.get_keypoint_coordinates(self.keypoint_names[key])
        return result

    def get_keypoint_coordinates(self, kp: "Keypoint"):
        cont_x, cont_y, *_ = self.bbox(self.container)
        return ((kp.x-cont_x)/self.imscale, (kp.y-cont_y)/self.imscale)

class Keypoint:
    def __init__(self, name: str, coordinates: tuple[float, float], skeleton_node: SkeletonNode):
        self.name = name
        self.coordinates = coordinates
        self.skeleton_node = skeleton_node
    
    @property
    def x(self):
        return self.coordinates[0]
    
    @property
    def y(self):
        return self.coordinates[1]