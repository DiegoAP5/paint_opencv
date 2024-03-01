import tkinter as tk
from paint import Paint

class DrawingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Drawing App")

        self.canvas_width = 640
        self.canvas_height = 480

        self.canvas = Paint(self.master, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        self.button_line = tk.Button(self.master, text="Line", command=lambda: self.canvas.set_drawing_type("line"), bg="white", relief=tk.FLAT)
        self.button_line.pack(side=tk.LEFT)

        self.button_circle = tk.Button(self.master, text="Circle", command=lambda: self.canvas.set_drawing_type("circle"), bg="white", relief=tk.FLAT)
        self.button_circle.pack(side=tk.LEFT)

        self.button_rectangle = tk.Button(self.master, text="Rectangle", command=lambda: self.canvas.set_drawing_type("rectangle"), bg="white", relief=tk.FLAT)
        self.button_rectangle.pack(side=tk.LEFT)
        
        self.button_rectangle = tk.Button(self.master, text="Polyline", command=lambda: self.canvas.set_drawing_type("polyline"), bg="white", relief=tk.FLAT)
        self.button_rectangle.pack(side=tk.LEFT)

        self.button_erase = tk.Button(self.master, text="Eraser", command=lambda: self.canvas.set_drawing_type("erase"), bg="white", relief=tk.FLAT)
        self.button_erase.pack(side=tk.LEFT)
