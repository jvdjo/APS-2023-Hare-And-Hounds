import tkinter as tk
from uuid import UUID
from PIL import Image, ImageTk
from py_netgames_client.tkinter_client.PyNetgamesServerProxy import PyNetgamesServerProxy
from py_netgames_client.tkinter_client.PyNetgamesServerListener import PyNetgamesServerListener
from py_netgames_model.messaging.message import MatchStartedMessage, MoveMessage
from hare_and_hounds.game_logic.Entities.Pecas import Hare, Hound
from hare_and_hounds.game_logic.Entities.Board import Board
from hare_and_hounds.game_logic.MenuBar import Menubar
from typing import Optional
from hare_and_hounds.game_logic.Entities.Pecas import Animal


class ActorPlayer(PyNetgamesServerListener):
    _tk: tk.Tk
    _server_proxy: PyNetgamesServerProxy
    _ongoing_match: bool
    _match_id: UUID
    _board: Optional[Board]
    _menu_bar: Menubar

    def __init__(self) -> None:
        super().__init__()
        self._tk = tk.Tk()
        self._tk.title("Hare and Hounds")
        self._server_proxy = PyNetgamesServerProxy()
        self._menu_bar = Menubar(self._server_proxy, self._tk)
        self._ongoing_match = False
        self.match_id = None
        self.rows = 3
        self.cols = 5
        self.cell_width = 150
        self.cell_height = 150
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
        self._board = Board()

    def preparacao_jogo(self):
        self.origem_x = None
        self.origem_y = None
        self._drag_data = {}

        self._board._board = [[None for _ in range(self.cols)]
                              for _ in range(self.rows)]
        
        self._board._board[0][0] = 99
        self._board._board[0][4] = 99
        self._board._board[2][0] = 99
        self._board._board[2][4] = 99

        self._board._total_jogadas = 0

        cao_1_x = 3 * self.cell_width + self.cell_width//4
        cao_1_y = 0 * self.cell_height + self.cell_height//4
        self.cao_1 = Hound(self.canvas, cao_1_x, cao_1_y, Animal.Hound)
        self._board._board[0][3] = self.cao_1.objeto

        cao_2_x = 4 * self.cell_width + self.cell_width//4
        cao_2_y = 1 * self.cell_height + self.cell_height//4
        self.cao_2 = Hound(self.canvas, cao_2_x, cao_2_y, Animal.Hound)
        self._board._board[1][4] = self.cao_2.objeto

        cao_3_x = 3 * self.cell_width + self.cell_width//4
        cao_3_y = 2 * self.cell_height + self.cell_height//4
        self.cao_3 = Hound(self.canvas, cao_3_x, cao_3_y, Animal.Hound)
        self._board._board[2][3] = self.cao_3.objeto

        lebre_x = 0 * self.cell_width + self.cell_width//4
        lebre_y = 1 * self.cell_height + self.cell_height//4
        self.lebre = Hare(self.canvas, lebre_x, lebre_y, Animal.Hare)
        self._board._board[1][0] = self.lebre.objeto

    def iniciar_arraste(self, event):
        item = self.canvas.find_withtag(tk.CURRENT)
        if item and len(item) > 0:
            item = item[0]
            if (item == 5 and self._board._animal == Animal.Hare) or (item != 5 and self._board._animal == Animal.Hound):
                self._drag_data = {'x': event.x, 'y': event.y, 'item': item}
                self.origem_x = event.x//150
                self.origem_y = event.y//150

    def arrastar(self, event):
        if (self.origem_x != None and self.origem_y != None):
            delta_x = event.x - self._drag_data['x']
            delta_y = event.y - self._drag_data['y']
            self.canvas.move(self._drag_data['item'], delta_x, delta_y)
            self._drag_data['x'] = event.x
            self._drag_data['y'] = event.y

    def soltar(self, event):
        if (self.origem_x != None and self.origem_y != None):
            if (self._board._is_turn == True):
                x, y = event.x, event.y
                col = x // 150
                row = y // 150
                origem = (self.origem_x, self.origem_y)
                destino = (col, row)

                if col >= self.cols:
                    col = self.cols - 1

                if (row == 0 and col == 0):
                    target_x = self.origem_x * 150 + 37.5
                    target_y = self.origem_y * 150 + 37.5
                    self.canvas.coords(
                        self._drag_data['item'], target_x, target_y)
                    self.origem_x = None
                    self.origem_y = None
                    return

                if (row == 0 and col == 4):
                    target_x = self.origem_x * 150 + 37.5
                    target_y = self.origem_y * 150 + 37.5
                    self.canvas.coords(
                        self._drag_data['item'], target_x, target_y)
                    self.origem_x = None
                    self.origem_y = None
                    return

                if (row == 2 and col == 0):
                    target_x = self.origem_x * 150 + 37.5
                    target_y = self.origem_y * 150 + 37.5
                    self.canvas.coords(
                        self._drag_data['item'], target_x, target_y)
                    self.origem_x = None
                    self.origem_y = None
                    return

                if (row == 2 and col == 4):
                    target_x = self.origem_x * 150 + 37.5
                    target_y = self.origem_y * 150 + 37.5
                    self.canvas.coords(
                        self._drag_data['item'], target_x, target_y)
                    self.origem_x = None
                    self.origem_y = None
                    return

                if self._board._board[row][col] is None and self.validar_movimentacao(origem, destino):
                    target_x = col * 150 + 37.5  # Centralize a imagem nas células da matriz
                    target_y = row * 150 + 37.5  # Centralize a imagem nas células da matriz
                    self.canvas.coords(
                        self._drag_data['item'], target_x, target_y)
                    self._board._board[row][col] = self._drag_data['item']
                    self._board._board[self.origem_y][self.origem_x] = None
                    self.origem_x = None
                    self.origem_y = None
                    self._board._total_jogadas += 1
                    self._board._is_turn = False
                    ganhador = self.verificar_vitoria()
                    if(ganhador != 0):
                        print("O jogador" + " " + str(self._board._animal) + " " + "ganhou")
                        self.reset()
                        return
                    self.send_move()

                else:
                    # A posição na matriz está ocupada, retorne a peça à posição original
                    # Centralize a imagem nas células da matriz
                    target_x = self.origem_x * 150 + 37.5
                    # Centralize a imagem nas células da matriz
                    target_y = self.origem_y * 150 + 37.5
                    self.canvas.coords(
                        self._drag_data['item'], target_x, target_y)
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

    def validar_movimentacao(self, origem, destino):
        # Calcula as diferenças nas coordenadas
        diferenca_x = abs(destino[0] - origem[0])
        diferenca_y = abs(destino[1] - origem[1])
        # Permite movimentos em qualquer direção nas outras situações
        if ((origem[0] == 1 or origem[0] == 3) and destino[0] == 2):
            if (origem[1] == 1 and (destino[1] == 0 or destino[1] == 2)):
                return False
        if (origem[0] == 2 and (destino[0] == 1 or destino[0] == 3)):
            if ((origem[1] == 0 or origem[1] == 2) and destino[1] == 1):
                return False
        if (self._board._animal == Animal.Hound):
            return destino[0] - origem[0] <= 0 and diferenca_y <= 1
        return diferenca_x <= 1 and diferenca_y <= 1

    def verificar_vitoria(self):
        if (self._board._total_jogadas == 50):
            return Animal.Hare
        if (self._board._board[1][4] == 5):
            return Animal.Hare

        #busca posição da lebre
        for linha in range(self.rows):
            for coluna in range(self.cols):
                if self._board._board[linha][coluna] == 5:
                    lebre_x = linha
                    lebre_y = coluna

        # Verifica as posições ao redor
        for i in range(max(0, lebre_x - 1), min(lebre_x + 2, self.rows)):
            for j in range(max(0, lebre_y - 1), min(lebre_y + 2, self.cols)):
                if self._board._board[i][j] == None:
                    return 0
        return Animal.Hound

    def atualizar_tela(self):
        for x in range(self.rows):
            for y in range(self.cols):
                if (self._board._board[x][y] != None):
                    # Centralize a imagem nas células da matriz
                    target_x = x * self.cell_width + self.cell_width//4
                    # Centralize a imagem nas células da matriz
                    target_y = y * self.cell_height + self.cell_height//4
                    self.canvas.coords(
                        self._board._board[x][y], target_y, target_x)

    def reset(self):
        self.origem_x = None
        self.origem_y = None
        self._drag_data = {}

        self._board._board = [[None for _ in range(self.cols)]
                              for _ in range(self.rows)]
        
        self._board._board[0][0] = 99
        self._board._board[0][4] = 99
        self._board._board[2][0] = 99
        self._board._board[2][4] = 99

        self._board._total_jogadas = 0

        cao_1_x = 3 * self.cell_width + self.cell_width//4
        cao_1_y = 0 * self.cell_height + self.cell_height//4
        self.canvas.coords(self.cao_1.objeto, cao_1_x, cao_1_y)
        self._board._board[0][3] = self.cao_1.objeto

        cao_2_x = 4 * self.cell_width + self.cell_width//4
        cao_2_y = 1 * self.cell_height + self.cell_height//4
        self.canvas.coords(self.cao_2.objeto, cao_2_x, cao_2_y)
        self._board._board[1][4] = self.cao_2.objeto

        cao_3_x = 3 * self.cell_width + self.cell_width//4
        cao_3_y = 2 * self.cell_height + self.cell_height//4
        self.canvas.coords(self.cao_3.objeto, cao_3_x, cao_3_y)
        self._board._board[2][3] = self.cao_3.objeto

        lebre_x = 0 * self.cell_width + self.cell_width//4
        lebre_y = 1 * self.cell_height + self.cell_height//4
        self.canvas.coords(self.lebre.objeto, lebre_x, lebre_y)
        self._board._board[1][0] = self.lebre.objeto

        if(self._board._animal == Animal.Hare):
            self._board._is_turn = False
        self._server_proxy.send_move(self._match_id, self._board.to_dict())

    def run(self):
        self._server_proxy.add_listener(self)
        self._tk.mainloop()

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

    def receive_move(self, message: MoveMessage):
        board = Board.from_dict(message.payload)
        self._board._total_jogadas = board._total_jogadas
        self._board._is_turn = board._is_turn
        self._board._total_jogadas = board._total_jogadas
        self._board._board = board._board
        self._board.flip()
        print(self._board)
        self.atualizar_tela()
        self.botao_reiniciar.config(state=tk.ACTIVE)

    def receive_error(self, error: Exception):
        print("ACONTECEU UM ERRO")
        self._menu_bar.connection_error(error)
        self._ongoing_match = False
        self.preparacao_jogo()

    def receive_disconnect(self):
        self._menu_bar.disconnect()
        self._ongoing_match = False
        self.preparacao_jogo()

    def send_move(self):
        print("##############ENVIADO###############")
        self._server_proxy.send_move(
            self._match_id, self._board.to_dict())
        self.botao_reiniciar.config(state=tk.DISABLED)
