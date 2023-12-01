from PIL import Image, ImageTk
import tkinter as tk


class Peca_base:
    def __init__(self, canvas : tk.Canvas, x, y, image_path):
        self.image = Image.open(image_path)
        self.image = self.image.resize((75, 75))
        self.photo = ImageTk.PhotoImage(self.image)
        self.objeto = canvas.create_image(x, y, anchor=tk.NW, image=self.photo, tags="draggable")

class Hound(Peca_base):
    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y, "./hare_and_hounds/game_logic/images/hound.png")  # Substitua "objeto1.png" pelo caminho da sua imagem de objeto

class Hare(Peca_base):
    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y, "./hare_and_hounds/game_logic/images/hare.png")  # Substitua "objeto2.png" pelo caminho da sua imagem de objeto