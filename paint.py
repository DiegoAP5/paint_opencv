import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

class Shape:
    def __init__(self, shape_type, coordinates):
        self.shape_type = shape_type
        self.coordinates = coordinates

class Paint(tk.Canvas):
    def __init__(self, master, width, height):
        super().__init__(master, width=width, height=height, bg="white", highlightthickness=0)
        self.canvas_width = width
        self.canvas_height = height
        self.drawing_type = None
        self.start_x = None
        self.start_y = None
        self.shapes = []
        self.polyline_points = []  # Lista para almacenar los puntos de la polilínea
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
        temp_img = self.cv2_photo.copy()  # Crear una copia temporal de la imagen actual
    
        if self.drawing_type == "line":
            cv2.line(temp_img, (self.start_x, self.start_y), (event.x, event.y), (0, 0, 0), 1)
        elif self.drawing_type == "circle":
            cv2.circle(temp_img, (self.start_x, self.start_y), int(np.sqrt((event.x - self.start_x) ** 2 + (event.y - self.start_y) ** 2)), (0, 0, 0), 1)
        elif self.drawing_type == "rectangle":
            cv2.rectangle(temp_img, (self.start_x, self.start_y), (event.x, event.y), (0, 0, 0), 1)
        elif self.drawing_type == "polyline":
            if self.start_x is not None and self.start_y is not None:
                cv2.line(self.cv2_photo, (self.start_x, self.start_y), (event.x, event.y), (0, 0, 0), 1)
                self.polyline_points.append((event.x, event.y))  # Agregar el punto actual a la lista
                self.start_x = event.x
                self.start_y = event.y

        self.photo = ImageTk.PhotoImage(image=Image.fromarray(temp_img))
        self.itemconfig(self.find_withtag("current"), image=self.photo)  # Actualizar la imagen en el lienzo

    def end_draw(self, event):
        if self.drawing_type == "polyline":
            if self.start_x is not None and self.start_y is not None:
                # Agregar la polilínea a la lista de formas
                self.shapes.append(Shape("polyline", self.polyline_points))
                self.polyline_points = []  # Reiniciar la lista de puntos
        elif self.drawing_type == "erase":
            # Agregar el borrado como una forma a la lista de formas
            self.shapes.append(Shape("erase", (self.start_x, self.start_y, event.x, event.y)))

        elif self.drawing_type != None:
            # Agregar la forma a la lista de formas (excepto para la herramienta de borrado)
            self.shapes.append(Shape(self.drawing_type, (self.start_x, self.start_y, event.x, event.y)))

        # Dibujar todas las formas almacenadas
        self.redraw_shapes()

    def redraw_shapes(self):
        temp_img = np.ones((self.canvas_height, self.canvas_width, 3), np.uint8) * 255
        for shape in self.shapes:
            if shape.shape_type == "line":
                cv2.line(temp_img, (shape.coordinates[0], shape.coordinates[1]), (shape.coordinates[2], shape.coordinates[3]), (0, 0, 0), 1)
            elif shape.shape_type == "circle":
                cv2.circle(temp_img, (shape.coordinates[0], shape.coordinates[1]), int(np.sqrt((shape.coordinates[2] - shape.coordinates[0]) ** 2 + (shape.coordinates[3] - shape.coordinates[1]) ** 2)), (0, 0, 0), 1)
            elif shape.shape_type == "rectangle":
                cv2.rectangle(temp_img, (shape.coordinates[0], shape.coordinates[1]), (shape.coordinates[2], shape.coordinates[3]), (0, 0, 0), 1)
            elif shape.shape_type == "polyline":
                points = np.array(shape.coordinates, np.int32)
                points = points.reshape((-1, 1, 2))
                cv2.polylines(temp_img, [points], False, (0, 0, 0), 1)
            elif shape.shape_type == "erase":
                # Borrar las partes correspondientes de la imagen
                cv2.line(temp_img, (shape.coordinates[0], shape.coordinates[1]), (shape.coordinates[2], shape.coordinates[3]), (255, 255, 255), 20)

        self.cv2_photo = temp_img
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(self.cv2_photo))
        self.itemconfig(self.find_withtag("current"), image=self.photo)  # Actualizar la imagen en el lienzo

    def clear_canvas(self):
        self.shapes = []  # Limpiar todas las formas
        self.img = np.ones((self.canvas_height, self.canvas_width, 3), np.uint8) * 255
        self.cv2_photo = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(self.cv2_photo))
