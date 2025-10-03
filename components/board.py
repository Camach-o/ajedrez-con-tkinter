from tkinter import *
# if __name__ != "__main__":
#     from components.pieces import *
#     import components.project_vars as project_vars
#     import components.game as game
    
# else:
from pieces import *
import project_vars as project_vars
import game
from PIL import Image, ImageTk

BOARD_LIMIT = 8

class Square(Canvas):
    def __init__(self, container, coord, **kwargs):
        super().__init__(container, width=80, height=80, highlightthickness=0, **kwargs)
        self.piece = None
        self.color = None
        self.coordts = coord
        self.highlight = False
        self.active_selection = 0

        # Highlights 
        self.path_capture_img = "contenido_grafico/images_highlight/capture.png"
        self.capture_img = ImageTk.PhotoImage(Image.open(self.path_capture_img))
        self.highlight_capture = self.create_image(40, 40, image=self.capture_img, state="hidden")          
        
        self.path_free_img = "contenido_grafico/images_highlight/free_square.png"
        self.free_img = ImageTk.PhotoImage(Image.open(self.path_free_img))
        self.highlight_free_square = self.create_image(40, 40, image=self.free_img, state="hidden")

        self.path_selected_img = "contenido_grafico/images_highlight/selected_square.png"
        self.selected_img = ImageTk.PhotoImage(Image.open(self.path_selected_img))
        self.highlight_selected_square = self.create_image(40, 40, image=self.selected_img, state="hidden")

        # self.bind('<Button-1>', project_vars.game.click_event)

    def turn_on_highlight(self):
        """ Select and active the highlight corresponding to the square status."""
        if self.active_selection:
            self.itemconfigure(self.highlight_selected_square, state="normal")
        elif self.piece:
            self.itemconfigure(self.highlight_capture, state="normal")
        else:
            self.itemconfigure(self.highlight_free_square, state="normal")
        self.highlight = True

    def turn_off_highlight(self):
        """ Disable the square highlighting."""
        self.itemconfigure(self.highlight_selected_square, state="hidden")
        self.itemconfigure(self.highlight_capture, state="hidden")
        self.itemconfigure(self.highlight_free_square, state="hidden")
        self.highlight = False
        self.active_selection = 0

    def quit_piece(self):
        self.delete(self.piece.id_piece)
        self.piece = False

    def put_piece(self, att):
        if self.piece:
            self.quit_piece()
        self.piece = Piece(self, color=att['color'], type=att['tipo'], board_view=att['view'], first_move=att['first_move'])
        
class Board:
    def __init__(self, container, game):
        self.board_container = container
        self.game = game

        self.board = [[0 for _ in range(0, BOARD_LIMIT)] for _ in range(0, BOARD_LIMIT)]
        self.theme = {"white": "#bb935b", "black": "#592f0a"}
        self.board_view = [1, 0]
        self.row_numbers = ["8", "7", "6", "5", "4", "3", "2", "1"]
        self.row_labels = []
        self.column_letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
        self.column_labels = []

    def _create_board_squares(self):
        """ Create and set the squares on the board."""

        for row in range(0, BOARD_LIMIT):
            for column in range(0, BOARD_LIMIT):
                square_widget = Square(self.board_container, coord=(row, column))
                square_widget.bind('<Button-1>', self.game.click_event)
                square_widget.pack_propagate(False)
                square_widget.grid(row=row, column=column)
                self.board[row][column] = square_widget

    def _create_position_labels(self):
        """ Create and put the position labels."""

        for row, n in enumerate(self.row_numbers):
            square = self.board[row][0]
            num = square.create_text(12, 14, text=n, font=("Arial Black", 16))
            self.row_labels.append(num)

        for column, n in enumerate(self.column_letters):
            square = self.board[7][column]
            let = square.create_text(70, 68, text=n, font=("Arial Black", 16))
            self.column_labels.append(let)

    def set_initial_position(self):
        """ Create the pieces and place them in their inital positions on the board."""

        if self.board_view[0] == 1:
            aliniation = ("R", "N", "B", "Q", "K", "B", "N", "R")
        else:
            aliniation = ("R", "N", "B", "K", "Q", "B", "N", "R")

        for piece_group in ({"row": 0, "color": 0 if self.board_view[0] else 1}, 
                            {"row": 7, "color": 1 if self.board_view[0] else 0}):
            for column, type in enumerate(aliniation):
                square = self.board[piece_group['row']][column]
                piece = Piece(square, color=piece_group['color'], type=type,
                              board_view=self.board_view[0])
                self.board[piece_group['row']][column].piece = piece

        # Pawns
        for square in self.board[1]:
            piece = Piece(square, color=0 if self.board_view[0] else 1, type="P", 
                          board_view=self.board_view[0])
            square.piece = piece

        for square in self.board[6]:
            piece = Piece(square, color=1 if self.board_view[0] else 0, type="P",
                          board_view=self.board_view[0])
            square.piece = piece

    def pieces_pruebas(self): # Eliminar luego de terminar
        """ Inserta en el tablero pieces para probar los mecanismos del juego."""
        piece = Piece(self.board[7][4], color=1, type="K", board_view=self.board_view[0])
        self.board[7][4].piece = piece

        piece = Piece(self.board[0][0], color=0, type="K", board_view=self.board_view[0])
        self.board[0][0].piece = piece

        piece = Piece(self.board[3][4], color=1, type="N", board_view=self.board_view[0])
        self.board[3][4].piece = piece

        piece = Piece(self.board[0][4], color=0, type="Q", board_view=self.board_view[0])
        self.board[0][4].piece = piece

        piece = Piece(self.board[4][4], color=1, type="P", board_view=self.board_view[0])
        self.board[4][4].piece = piece

        piece = Piece(self.board[6][0], color=1, type="P", board_view=self.board_view[0])
        self.board[6][0].piece = piece

    def set_theme(self, white, black):
        """ Set the theme on the squares and position labels on the board.
        
            Args:
                white (str): Hexadecimal value for the color white.
                black (str): Hexadecimal value for the color black.
        """

        theme = [white, black]
        for row in self.board:
            for square in row:
                square.configure(background=theme[0])
                square.color=theme[0]
                theme.reverse()
            theme.reverse()

        for row, label_id in enumerate(self.row_labels):
            square = self.board[row][0]
            square.itemconfigure(label_id, 
                                 fill=theme[0] if theme[0] != square.color else theme[1])
        for columna, label_id in enumerate(self.column_labels):
            square = self.board[7][columna]
            square.itemconfigure(label_id, 
                                 fill=theme[0] if theme[0] != square.color else theme[1])

    def turn_the_board(self):
        """ Turn the board upside down."""

        self.board_view.reverse()
        for i, row in enumerate(self.board):
            row[0].delete(self.row_labels[i])
        for i, column in enumerate(self.board[7]):
            column.delete(self.column_labels[i])

        self.row_labels = []
        self.column_labels = []
        self.row_numbers.reverse()
        self.column_letters.reverse()
        self._create_position_labels()
        self.set_theme(self.theme.get("white"), self.theme.get("black"))
        self.clear_board()
        self.set_initial_position()

    def clear_board(self):
        """ Remove pieces and reset board values."""
        
        for row in self.board:
            for square in row:
                if square.piece:
                    square.delete(square.piece.id_piece)
                    square.piece = None
        self.turn_off_highlights()

    def put_board(self):
        """ Calls the functions that create the graphical interface of the board."""
        self._create_board_squares()
        self._create_position_labels()
        self.set_theme(self.theme.get("white"), self.theme.get("black"))