import tkinter as tk
from uuid import UUID
from PIL import Image, ImageTk
from py_netgames_client.tkinter_client.PyNetgamesServerProxy import PyNetgamesServerProxy
from py_netgames_client.tkinter_client.PyNetgamesServerListener import PyNetgamesServerListener
from py_netgames_model.messaging.message import MatchStartedMessage, MoveMessage
from hare_and_hounds.game_logic.Entities.Pecas import Hare, Hound
from hare_and_hounds.game_logic.Entities.Matrix import Board
from hare_and_hounds.game_logic.MenuBar import Menubar


class ActorPlayer(PyNetgamesServerListener):
    _tk : tk.Tk
    _server_proxy: PyNetgamesServerProxy
    _ongoing_match : bool
    _match_id: UUID
    _board: Board
    _menu_bar : Menubar

    def __init__(self) -> None:
        super().__init__()
        self._tk = tk.Tk()
        self._tk.title("Hare and Hounds")
        self._server_proxy = PyNetgamesServerProxy()
        self._menu_bar = Menubar(self._server_proxy, self._tk)
        self._ongoing_match = False
        self.match_id = None
        self._board = None
        self.rows = 3
        self.cols = 5
        self.cell_width = 150
        self.cell_height = 150
        self.minha_vez = False
        # Aumentei a altura para acomodar o botão
        self._tk.geometry(f"{self.cols*150}x{self.rows*150 + 50}")

        # Menu superior
        self._tk.config(menu=self._menu_bar)

        # Adicionar o botão "Reiniciar partida"
        self.botao_reiniciar = tk.Button(
            self._tk, text="Reiniciar partida", command=self.reset)
        # Aumentei o espaço entre o botão e o canvas
        self.botao_reiniciar.pack(side=tk.BOTTOM, pady=10)

        # Cria o canvas que representa a janela onde as coisas serão desenhadas
        self.canvas = tk.Canvas(
            self._tk, width=self.cols*self.cell_width, height=self.rows*self.cell_height)
        self.canvas.pack()

        # Carregue a imagem de fundo
        self.background_image = Image.open(
            "./hare_and_hounds/game_logic/images/tabuleiro.png")
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.canvas.create_image(
            0, 0, anchor=tk.NW, image=self.background_photo)
        
        self.canvas.tag_bind(
            "draggable", "<ButtonPress-1>", self.iniciar_arraste)
        self.canvas.tag_bind("draggable", "<B1-Motion>", self.arrastar)
        self.canvas.tag_bind("draggable", "<ButtonRelease-1>", self.soltar)
        

    def preparacao_jogo(self):
        self.origem_x = None
        self.origem_y = None
        self._drag_data = {}

        self.matriz = [[None for _ in range(self.cols)]
                       for _ in range(self.rows)]

        self.total_jogadas = 0

        cao_1_x = 3 * self.cell_width + self.cell_width//4
        cao_1_y = 0 * self.cell_height + self.cell_height//4
        self.cao_1 = Hound(self.canvas, cao_1_x, cao_1_y)
        self.matriz[0][3] = self.cao_1.objeto

        cao_2_x = 4 * self.cell_width + self.cell_width//4
        cao_2_y = 1 * self.cell_height + self.cell_height//4
        self.cao_2 = Hound(self.canvas, cao_2_x, cao_2_y)
        self.matriz[1][4] = self.cao_2.objeto

        cao_3_x = 3 * self.cell_width + self.cell_width//4
        cao_3_y = 2 * self.cell_height + self.cell_height//4
        self.cao_3 = Hound(self.canvas, cao_3_x, cao_3_y)
        self.matriz[2][3] = self.cao_3.objeto

        lebre_x = 0 * self.cell_width + self.cell_width//4
        lebre_y = 1 * self.cell_height + self.cell_height//4
        self.lebre = Hare(self.canvas, lebre_x, lebre_y)
        self.matriz[1][0] = self.lebre.objeto

    def iniciar_arraste(self, event):
        item = self.canvas.find_withtag(tk.CURRENT)
        if item and len(item) > 0:
            item = item[0]
            self._drag_data = {'x': event.x, 'y': event.y, 'item': item}
            self.origem_x = event.x//150
            self.origem_y = event.y//150

    def arrastar(self, event):
        delta_x = event.x - self._drag_data['x']
        delta_y = event.y - self._drag_data['y']
        self.canvas.move(self._drag_data['item'], delta_x, delta_y)
        self._drag_data['x'] = event.x
        self._drag_data['y'] = event.y

    def soltar(self, event):
        print(self.minha_vez)
        if(self.minha_vez == True):
            x, y = event.x, event.y
            col = x // 150
            row = y // 150

            if col >= self.cols:
                col = self.cols - 1

            if(row == 0 and col == 0):
                target_x = self.origem_x * 150 + 37.5
                target_y = self.origem_y * 150 + 37.5
                self.canvas.coords(self._drag_data['item'], target_x, target_y)
                self.origem_x = None
                self.origem_y = None
                return
            
            if(row == 0 and col == 4):
                target_x = self.origem_x * 150 + 37.5
                target_y = self.origem_y * 150 + 37.5
                self.canvas.coords(self._drag_data['item'], target_x, target_y)
                self.origem_x = None
                self.origem_y = None
                return

            if(row == 2 and col == 0):
                target_x = self.origem_x * 150 + 37.5
                target_y = self.origem_y * 150 + 37.5
                self.canvas.coords(self._drag_data['item'], target_x, target_y)
                self.origem_x = None
                self.origem_y = None
                return
            
            if(row == 2 and col == 4):
                target_x = self.origem_x * 150 + 37.5
                target_y = self.origem_y * 150 + 37.5
                self.canvas.coords(self._drag_data['item'], target_x, target_y)
                self.origem_x = None
                self.origem_y = None
                return

            if self.matriz[row][col] is None:
                target_x = col * 150 + 37.5  # Centralize a imagem nas células da matriz
                target_y = row * 150 + 37.5  # Centralize a imagem nas células da matriz
                self.canvas.coords(self._drag_data['item'], target_x, target_y)
                self.matriz[row][col] = self._drag_data['item']
                print(self._drag_data)
                self.matriz[self.origem_y][self.origem_x] = None
                self.origem_x = None
                self.origem_y = None
                self.total_jogadas += 1
                self.send_move()

            else:
                # A posição na matriz está ocupada, retorne a peça à posição original
                # Centralize a imagem nas células da matriz
                target_x = self.origem_x * 150 + 37.5
                # Centralize a imagem nas células da matriz
                target_y = self.origem_y * 150 + 37.5
                self.canvas.coords(self._drag_data['item'], target_x, target_y)
                self.origem_x = None
                self.origem_y = None

        else:
            # A posição na matriz está ocupada, retorne a peça à posição original
            # Centralize a imagem nas células da matriz
            target_x = self.origem_x * 150 + 37.5
            # Centralize a imagem nas células da matriz
            target_y = self.origem_y * 150 + 37.5
            self.canvas.coords(self._drag_data['item'], target_x, target_y)
            self.origem_x = None
            self.origem_y = None

        # print("#####################################")
        # for i in range(len(self.matriz)):
        #     print(self.matriz[i])
        #     print()

    def atualizar_tela(self, matriz):
        self.matriz = matriz

        print(self.minha_vez)
        print("#############RECEBIDO#################")
        for i in range(len(self.matriz)):
            print(self.matriz[i])
            print()

        for x in range(self.rows):
            for y in range(self.cols):
                if (self.matriz[x][y] != None):
                    target_x = x * 150 + 37.5  # Centralize a imagem nas células da matriz
                    target_y = y * 150 + 37.5  # Centralize a imagem nas células da matriz
                    self.canvas.coords(5, target_x, target_y)


    def reset(self):
        self.origem_x = None
        self.origem_y = None
        self._drag_data = {}

        self.matriz = [[None for _ in range(self.cols)]
                       for _ in range(self.rows)]

        self.total_jogadas = 0
        
        cao_1_x = 3 * self.cell_width + self.cell_width//4
        cao_1_y = 0 * self.cell_height + self.cell_height//4
        self.canvas.coords(self.cao_1.objeto, cao_1_x, cao_1_y)
        self.matriz[0][3] = self.cao_1.objeto

        cao_2_x = 4 * self.cell_width + self.cell_width//4
        cao_2_y = 1 * self.cell_height + self.cell_height//4
        self.canvas.coords(self.cao_2.objeto, cao_2_x, cao_2_y)
        self.matriz[1][4] = self.cao_1.objeto

        cao_3_x = 3 * self.cell_width + self.cell_width//4
        cao_3_y = 2 * self.cell_height + self.cell_height//4
        self.canvas.coords(self.cao_3.objeto, cao_3_x, cao_3_y)
        self.matriz[2][3] = self.cao_1.objeto

        lebre_x = 0 * self.cell_width + self.cell_width//4
        lebre_y = 1 * self.cell_height + self.cell_height//4
        self.canvas.coords(self.lebre.objeto, lebre_x, lebre_y)
        self.matriz[1][0] = self.cao_1.objeto
        

    def run(self):
        self.preparacao_jogo()
        self._server_proxy.add_listener(self)
        self._tk.mainloop()

    def send_match(self):
        self.server_proxy.send_match(2)

    def receive_connection_success(self):
        self._menu_bar.connection_confirmed()
        print("****** CONECTADO ******")

    def receive_match(self, message: MatchStartedMessage):
        self._ongoing_match = True
        self._match_id = message.match_id
        self._board = Board(position=message.position)
        self.preparacao_jogo()
        print("****** PARTIDA INICIADA ******")
        print("****** ORDEM: ", message.position)
        print("****** match_id: ", message.match_id)

    def receive_move(self, match: MoveMessage):
        self.total_jogadas = match.payload["total_jogadas"]
        self.minha_vez = match.payload["minha_vez"]
        self.atualizar_tela(match.payload["matriz"])

    def receive_error(self, error: Exception):
        self._menu_bar.connection_error(error)
        self._ongoing_match = False
        self.preparacao_jogo()

    def receive_disconnect(self):
        self._menu_bar.disconnect()
        self._ongoing_match = False
        self.preparacao_jogo()

    def send_move(self):
        self.minha_vez == False
        self.server_proxy.send_move(
            self.match_id, {"matriz": self.matriz, "total_jogadas": self.total_jogadas, "minha_vez" : True})
        print(self.minha_vez == False)
        print("##############ENVIADO###############")
        for i in range(len(self.matriz)):
            print(self.matriz[i])
            print()

