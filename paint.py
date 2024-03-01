import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

class Paint(tk.Canvas):
    def __init__(self, master, width, height):
        super().__init__(master, width=width, height=height, bg="white", highlightthickness=0)
        self.canvas_width = width
        self.canvas_height = height
        self.drawing_type = None
        self.start_x = None
        self.start_y = None
        self.shapes = []
        self.init_opencv()

    def init_opencv(self):
        self.img = np.ones((self.canvas_height, self.canvas_width, 3), np.uint8) * 255
        self.cv2_photo = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(self.cv2_photo))
        self.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.bind("<ButtonPress-1>", self.start_draw)
        self.bind("<B1-Motion>", self.draw)
        self.bind("<ButtonRelease-1>", self.end_draw)

    def set_drawing_type(self, drawing_type):
        self.drawing_type = drawing_type

    def start_draw(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def draw(self, event):
        self.cv2_photo = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)

        if self.drawing_type == "line":
            self.delete("temp_line")
            cv2.line(self.cv2_photo, (self.start_x, self.start_y), (event.x, event.y), (0, 0, 0), 1)
        elif self.drawing_type == "circle":
            cv2.circle(self.cv2_photo, (self.start_x, self.start_y), int(np.sqrt((event.x - self.start_x) ** 2 + (event.y - self.start_y) ** 2)), (0, 0, 0), 1)
        elif self.drawing_type == "rectangle":
            cv2.rectangle(self.cv2_photo, (self.start_x, self.start_y), (event.x, event.y), (0, 0, 0), 1)
        elif self.drawing_type == "polyline":
            if self.start_x is not None and self.start_y is not None:
                cv2.line(self.img, (self.start_x, self.start_y), (event.x, event.y), (0, 0, 0), 1)
                self.start_x = event.x
                self.start_y = event.y
        elif self.drawing_type == "erase":
            cv2.line(self.img, (self.start_x, self.start_y), (event.x, event.y), (255, 255, 255), 20)
            self.start_x = event.x
            self.start_y = event.y

        self.photo = ImageTk.PhotoImage(image=Image.fromarray(self.cv2_photo))
        self.itemconfig(self.find_withtag("current"), image=self.photo)  # Actualizar la imagen en el lienzo

    def end_draw(self, event):
        if self.drawing_type in ["line", "circle", "rectangle"]:
            self.shapes.append(self.cv2_photo.copy())
        elif self.drawing_type == "polyline":
            self.shapes.append(self.cv2_photo.copy())

    def clear_canvas(self):
        self.img = np.ones((self.canvas_height, self.canvas_width, 3), np.uint8) * 255
        self.cv2_photo = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(self.cv2_photo))
