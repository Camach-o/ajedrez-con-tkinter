from PIL import Image, ImageTk

# Image paths for white pieces
IMG_WHITE_KING = "assets/pieces/white_king.png"
IMG_WHITE_QUEEN = "assets/pieces/white_queen.png"
IMG_WHITE_ROOK = "assets/pieces/white_rook.png"
IMG_WHITE_BISHOP = "assets/pieces/white_bishop.png"
IMG_WHITE_KNIGHT = "assets/pieces/white_knight.png"
IMG_WHITE_PAWN = "assets/pieces/white_pawn.png"

# Image paths for black pieces
IMG_BLACK_KING = "assets/pieces/black_king.png"
IMG_BLACK_QUEEN = "assets/pieces/black_queen.png"
IMG_BLACK_ROOK = "assets/pieces/black_rook.png"
IMG_BLACK_BISHOP = "assets/pieces/black_bishop.png"
IMG_BLACK_KNIGHT = "assets/pieces/black_knight.png"
IMG_BLACK_PAWN = "assets/pieces/black_pawn.png"

class Piece:
    VALID_TYPES = ("R", "N", "B", "Q", "K", "P")
    def __init__(self, canvas, color, ptype, board_view, first_move=True):
        self.validate_atts(color, ptype, board_view, first_move)

        # Piece attributes
        self.ptype = ptype
        self.color = color
        self.board_view = board_view
        self.squares_limit = None
        self.movements = None
        self.first_move = first_move
        self.castling = False

        # Partide attributes
        self.pinned = False
        self.available_movements = None
        self.position = {"row": canvas.coordts[0], "column": canvas.coordts[1]}

        self.set_atributes_to_piece_type()

        # GUI attributes
        self.canvas = canvas
        self.image = ImageTk.PhotoImage(Image.open(self.img_path))
        self.id_piece = canvas.create_image(40, 40, image=self.image)

    def validate_atts(self, color, ptype, board_view, first_move):
        if not color in (1, 0):
            raise ValueError(f'{color} no es una opción valida')
        if not ptype in self.VALID_TYPES:
            raise ValueError(ptype, 'no es una opción valida')
        if not board_view in (1, 0):
            raise ValueError(f'{board_view} no es una opción valida')
        if not first_move in (1, 0):
            raise ValueError(f'{first_move} no es una opción valida')

    def set_atributes_to_piece_type(self):
        if self.ptype == "K":
            self.img_path = IMG_WHITE_KING if self.color else IMG_BLACK_KING
            self.movements = [(-1, -1), (-1, 1), (1, 1), (1, -1),
                              (-1, 0), (1, 0), (0, -1), (0, 1)]
            self.squares_limit = 1
            if self.first_move:
                self.movements.append((0, -2)) # left_castling
                self.movements.append((0, 2))  # right_castling

                if self.board_view == 1:
                    if self.color == 1 and self.position == {"row": 7, "column": 4}:
                        self.castling = True
                    elif self.color == 0 and self.position == {"row": 0, "column": 4}:
                        self.castling = True
                elif self.board_view == 0:
                    if self.color == 1 and self.position == {"row": 0, "column": 3}:
                        self.castling = True
                    elif self.color == 0 and self.position == {"row": 7, "column": 3}:
                        self.castling = True

        elif self.ptype == "Q":
            self.img_path = IMG_WHITE_QUEEN if self.color else IMG_BLACK_QUEEN
            self.movements = [(-1, -1), (-1, 1), (1, 1), (1, -1),
                              (-1, 0), (1, 0), (0, -1), (0, 1)]
            self.squares_limit = 7

        elif self.ptype == "R":
            self.img_path = IMG_WHITE_ROOK if self.color else IMG_BLACK_ROOK
            self.movements = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            self.squares_limit = 7
            if self.first_move:
                if self.board_view == 1:
                    if self.color == 1 and (self.position in ({"row": 7, "column": 0}, {"row": 7, "column": 7})):
                        self.castling = True
                    elif self.color == 0 and (self.position in ({"row": 0, "column": 0}, {"row": 0, "column": 7})):
                        self.castling = True
                elif self.board_view == 0:
                    if self.color == 1 and (self.position in ({"row": 0, "column": 0}, {"row": 0, "column": 7})):
                        self.castling = True
                    elif self.color == 0 and (self.position in ({"row": 7, "column": 0}, {"row": 7, "column": 7})):
                        self.castling = True

        elif self.ptype == "B":
            self.img_path = IMG_WHITE_BISHOP if self.color else IMG_BLACK_BISHOP
            self.movements = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
            self.squares_limit = 7

        elif self.ptype == "N":
            self.img_path = IMG_WHITE_KNIGHT if self.color else IMG_BLACK_KNIGHT
            self.movements = [(-1, -2), (-2, -1), (-2, 1), (-1, 2),
                              (1, 2), (2, 1), (2, -1), (1, -2)]
            self.squares_limit = 1

        elif self.ptype == "P":
            self.img_path = IMG_WHITE_PAWN if self.color else IMG_BLACK_PAWN
                       
            if self.board_view == self.color:
                self.movements = [(-1, 0), (-1, -1), (-1, 1)]
                if self.position["row"] == 6:
                    self.movements.append((-2, 0))
            else:
                self.movements = [(1, 0), (1, 1), (1, -1)]
                if self.position["row"] == 1:
                    self.movements.append((2, 0))

            self.squares_limit = 1

    def get_atributes(self):
        return {'tipo': self.ptype, 'color': self.color, "first_move": self.first_move, "view": self.board_view}
