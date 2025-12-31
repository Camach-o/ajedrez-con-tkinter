from tkinter import Canvas
from PIL import Image, ImageTk
from components.pieces import Piece

BOARD_LIMIT = 8

class ChessSquare(Canvas):
    def __init__(self, container, coord, **kwargs):
        super().__init__(container, width=80, height=80, highlightthickness=0, **kwargs)
        self.piece = None
        self.color = None
        self.coordts = coord
        self.highlight = False
        self.active_selection = 0

        # Highlights
        self.path_capture_img = "assets/highlights/capture.png"
        self.capture_img = ImageTk.PhotoImage(Image.open(self.path_capture_img))
        self.highlight_capture = self.create_image(40, 40, image=self.capture_img, state="hidden")

        self.path_free_img = "assets/highlights/free_square.png"
        self.free_img = ImageTk.PhotoImage(Image.open(self.path_free_img))
        self.highlight_free_square = self.create_image(40, 40, image=self.free_img, state="hidden")

        self.path_selected_img = "assets/highlights/selected_square.png"
        self.selected_img = ImageTk.PhotoImage(Image.open(self.path_selected_img))
        self.highlight_selected_square = self.create_image(40, 40, image=self.selected_img, state="hidden")

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
        self.piece = Piece(self, color=att['color'], ptype=att['tipo'], board_view=att['view'], first_move=att['first_move'])

class ChessBoard:
    def __init__(self, container):
        self.board_container = container

        self.board = [[0 for _ in range(0, BOARD_LIMIT)] for _ in range(0, BOARD_LIMIT)]
        self.theme = {"white": "#bb935b", "black": "#592f0a"}
        self.row_numbers = ["8", "7", "6", "5", "4", "3", "2", "1"]
        self.row_labels = []
        self.column_letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
        self.column_labels = []
        self.view = [1, 0]

    def _create_board_squares(self):
        """ Create and set the squares on the board."""
        for row in range(0, BOARD_LIMIT):
            for column in range(0, BOARD_LIMIT):
                square_widget = ChessSquare(self.board_container, coord=(row, column))
                square_widget.pack_propagate(False)
                square_widget.grid(row=row, column=column)
                self.board[row][column] = square_widget

    def set_squares_callback(self, callback):
        """ Bind a function whith the squares."""
        for row in self.board:
            for square in row:
                square.bind('<Button-1>', callback)

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

    def put_piece(self, square, ptype, color, board_view):
        """ Create and put a piece in the board.
        
            Args:
                square (Square): Square where the piece will be placed.
                ptype (string): A letter that indicate the ptype of the piece.
                color (number): The color of the piece, 1 for white and 0 for black.
                board_view (number): Board's view, 1 for white and 0 for black.
        """
        square.piece = Piece(square,
                             color=color,
                             ptype=ptype,
                             board_view=board_view)

    def turn_the_board(self):
        """ Turn the board upside down."""

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
        self.view.reverse()

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

    def turn_off_highlights(self):
        """ Move across the board to turn off the active highlights."""

        for row in self.board:
            for square in row:
                if square.highlight:
                    square.turn_off_highlight()

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

    def get_position_of_square(self, square):
        """ Return the coordinate of the square."""
        row_indx, column_indx = square.coordts
        return f"{self.column_letters[column_indx]}{self.row_numbers[row_indx]}"

    def get_square_of_position(self, position):
        """ Return the letter row and the number column of the square."""
        column_letter, row_number = position
        column = self.column_letters.index(column_letter)
        row = self.row_numbers.index(row_number)
        return self.board[row][column]
