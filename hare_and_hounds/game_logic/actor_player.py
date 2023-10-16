import tkinter as tk
from PIL import Image, ImageTk
from py_netgames_client.tkinter_client.PyNetgamesServerProxy import PyNetgamesServerProxy
from py_netgames_client.tkinter_client.PyNetgamesServerListener import PyNetgamesServerListener
from py_netgames_model.messaging.message import MatchStartedMessage, MoveMessage

class Objeto:
    def __init__(self, canvas, x, y, image_path):
        self.canvas = canvas
        self.image = Image.open(image_path)
        self.image = self.image.resize((75, 75))
        self.photo = ImageTk.PhotoImage(self.image)
        self.objeto = self.canvas.create_image(x, y, anchor=tk.NW, image=self.photo, tags="draggable")

class Objeto1(Objeto):
    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y, "./hare_and_hounds/game_logic/images/hound.png")  # Substitua "objeto1.png" pelo caminho da sua imagem de objeto

class Objeto2(Objeto):
    def __init__(self, canvas, x, y):
        super().__init__(canvas, x, y, "./hare_and_hounds/game_logic/images/hare.png")  # Substitua "objeto2.png" pelo caminho da sua imagem de objeto

class ActorPlayer(PyNetgamesServerListener):
    def __init__(self):
        super().__init__()
        self.mainWindow = tk.Tk()
        self.rows = 3
        self.cols = 5
        self.mainWindow.geometry(f"{self.cols*150}x{self.rows*150 + 50}")  # Aumentei a altura para acomodar o botão
        self.mainWindow.title("Arrastar Imagens na Matriz")

        # Menu superior
        self.menu = tk.Menu(self.mainWindow)
        self.mainWindow.config(menu=self.menu)

        self.conexao_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Conexão", menu=self.conexao_menu)
        self.conexao_menu.add_command(label="Iniciar conexão", command=self.iniciar_conexao)

        self.canvas = tk.Canvas(self.mainWindow, width=self.cols*150, height=self.rows*150)
        self.canvas.pack()

        # Carregue a imagem de fundo
        self.background_image = Image.open("./hare_and_hounds/game_logic/images/tabuleiro.png")  # Substitua "background.jpg" pelo caminho da sua imagem
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_photo)

        # Tamanho das células da matriz
        cell_width = 150
        cell_height = 150

        # Crie os objetos a partir das classes Objeto1 e Objeto2
        objeto1_x = (self.cols//2 - 1) * cell_width + cell_width//4
        objeto1_y = (self.rows//2) * cell_height + cell_height//4
        self.objeto1 = Objeto1(self.canvas, objeto1_x, objeto1_y)

        objeto2_x = (self.cols//2) * cell_width + cell_width//4
        objeto2_y = (self.rows//2) * cell_height + cell_height//4
        self.objeto2 = Objeto2(self.canvas, objeto2_x, objeto2_y)

        # Crie mais objetos do tipo 1
        objeto3_x = (self.cols//2 + 1) * cell_width + cell_width//4
        objeto3_y = (self.rows//2) * cell_height + cell_height//4
        self.objeto3 = Objeto1(self.canvas, objeto3_x, objeto3_y)

        objeto4_x = (self.cols//2 + 2) * cell_width + cell_width//4
        objeto4_y = (self.rows//2) * cell_height + cell_height//4
        self.objeto4 = Objeto1(self.canvas, objeto4_x, objeto4_y)

        self.canvas.tag_bind("draggable", "<ButtonPress-1>", self.iniciar_arraste)
        self.canvas.tag_bind("draggable", "<B1-Motion>", self.arrastar)
        self.canvas.tag_bind("draggable", "<ButtonRelease-1>", self.soltar)

        self.matriz = [[None for _ in range(self.cols)] for _ in range(self.rows)]

        # Adicionar o botão "Reiniciar partida"
        self.botao_reiniciar = tk.Button(self.mainWindow, text="Reiniciar partida", command=self.reset)
        self.botao_reiniciar.pack(side=tk.BOTTOM, pady=10)  # Aumentei o espaço entre o botão e o canvas
        self.mainWindow.mainloop()

    def iniciar_conexao(self):
        self.add_listener()
        self.send_connect()

    def iniciar_arraste(self, event):
        item = self.canvas.find_withtag(tk.CURRENT)
        if item and len(item) > 0:
            item = item[0]
            self._drag_data = {'x': event.x, 'y': event.y, 'item': item}

    def arrastar(self, event):
        delta_x = event.x - self._drag_data['x']
        delta_y = event.y - self._drag_data['y']
        self.canvas.move(self._drag_data['item'], delta_x, delta_y)
        self._drag_data['x'] = event.x
        self._drag_data['y'] = event.y

    def soltar(self, event):
        x, y = event.x, event.y
        col = x // 150
        row = y // 150

        if col >= self.cols:
            col = self.cols - 1

        target_x = col * 150 + 37.5  # Centralize a imagem nas células da matriz
        target_y = row * 150 + 37.5  # Centralize a imagem nas células da matriz

        self.canvas.coords(self._drag_data['item'], target_x, target_y)
        self.matriz[row][col] = self._drag_data['item']

    def reset(self):
        # Limpar a matriz e reposicionar os objetos
        for row in range(self.rows):
            for col in range(self.cols):
                if self.matriz[row][col]:
                    self.canvas.delete(self.matriz[row][col])
                    self.matriz[row][col] = None

        # Posições iniciais das imagens no meio das posições da matriz
        cell_width = 150
        cell_height = 150

        objeto1_x = (self.cols//2 - 1) * cell_width + cell_width//4
        objeto1_y = (self.rows//2) * cell_height + cell_height//4
        self.canvas.coords(self.objeto1.objeto, objeto1_x, objeto1_y)
        self.matriz[self.rows//2][self.cols//2 - 1] = self.objeto1.objeto

        objeto2_x = (self.cols//2) * cell_width + cell_width//4
        objeto2_y = (self.rows//2) * cell_height + cell_height//4
        self.canvas.coords(self.objeto2.objeto, objeto2_x, objeto2_y)
        self.matriz[self.rows//2][self.cols//2] = self.objeto2.objeto

        # Reposicione os objetos adicionais do tipo 1
        objeto3_x = (self.cols//2 + 1) * cell_width + cell_width//4
        objeto3_y = (self.rows//2) * cell_height + cell_height//4
        self.canvas.coords(self.objeto3.objeto, objeto3_x, objeto3_y)
        self.matriz[self.rows//2][self.cols//2 + 1] = self.objeto3.objeto

        objeto4_x = (self.cols//2 + 2) * cell_width + cell_width//4
        objeto4_y = (self.rows//2) * cell_height + cell_height//4
        self.canvas.coords(self.objeto4.objeto, objeto4_x, objeto4_y)
        self.matriz[self.rows//2][self.cols//2 + 2] = self.objeto4.objeto


    def add_listener(self):
        self.server_proxy = PyNetgamesServerProxy()
        self.server_proxy.add_listener(self)

    def send_match(self):
        self.server_proxy.send_match(2)

    def send_connect(self):
        self.server_proxy.send_connect()
        print("****** ENVIANDO CONEXÃO ******")

    def receive_connection_success(self):
        print("****** CONECTADO ******")
        self.send_match()
    
    def receive_disconnect(self):
        return super().receive_disconnect()
    
    def receive_error(self, error: Exception):
        return super().receive_error(error)
    
    def receive_match(self, match: MatchStartedMessage):
        print("****** PARTIDA INICIADA ******")
        print("****** ORDEM: ", match.position)
        print("****** match_id: ", match.match_id)
    
    def receive_move(self, match: MoveMessage):
        return super().receive_move(match)
