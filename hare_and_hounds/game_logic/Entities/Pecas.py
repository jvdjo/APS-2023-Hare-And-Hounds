from PIL import Image, ImageTk
import tkinter as tk
from enum import Enum


class Animal(Enum):
    Hare = 1
    Hound = 2


class Peca_base:
    _type: Animal

    def __init__(self, canvas: tk.Canvas, x, y, image_path, type):
        self.image = Image.open(image_path)
        self.image = self.image.resize((75, 75))
        self.photo = ImageTk.PhotoImage(self.image)
        self.objeto = canvas.create_image(
            x, y, anchor=tk.NW, image=self.photo, tags="draggable")
        self._type = type


class Hound(Peca_base):
    def __init__(self, canvas, x, y, type):
        # Substitua "objeto1.png" pelo caminho da sua imagem de objeto
        super().__init__(canvas, x, y, "./hare_and_hounds/game_logic/images/hound.png", type)


class Hare(Peca_base):
    def __init__(self, canvas, x, y, type):
        # Substitua "objeto2.png" pelo caminho da sua imagem de objeto
        super().__init__(canvas, x, y, "./hare_and_hounds/game_logic/images/hare.png", type)
