from tkinter import *
from PIL import Image, ImageTk

IMG_REY_BLANCO = "contenido_grafico/images_pieces/rey-blanco.png"
IMG_DAMA_BLANCA = "contenido_grafico/images_pieces/reina-blanca.png"
IMG_TORRE_BLANCA = "contenido_grafico/images_pieces/torre-blanca.png"
IMG_ALFIL_BLANCO = "contenido_grafico/images_pieces/alfil-blanco.png"
IMG_CABALLO_BLANCO = "contenido_grafico/images_pieces/caballo-blanco.png"
IMG_PEON_BLANCO = "contenido_grafico/images_pieces/peon-blanco.png"

IMG_REY_NEGRO = "contenido_grafico/images_pieces/rey-negro.png"
IMG_DAMA_NEGRA = "contenido_grafico/images_pieces/reina-negra.png"
IMG_TORRE_NEGRA = "contenido_grafico/images_pieces/torre-negra.png"
IMG_ALFIL_NEGRO = "contenido_grafico/images_pieces/alfil-negro.png"
IMG_CABALLO_NEGRO = "contenido_grafico/images_pieces/caballo-negro.png"
IMG_PEON_NEGRO = "contenido_grafico/images_pieces/peon-negro.png"

class Piece:
    VALID_TYPES = ("R", "N", "B", "Q", "K", "P")
    """ Letter represetnation.
        R = Rey     / King
        D = Dama    / Quing
        T = Torre   / Rook
        A = Afil    / Bishop
        C = Caballo / Knight
        P = Peón    / Pawn
        I hate that the horse is called kNight in chess nomenclature,
        for that I used Spanish letters to reference the pieces.
    """
    def __init__(self, canvas, color, type, board_view, first_move=True):
        if type not in Piece.VALID_TYPES:
            raise ValueError(f'"{type}" no es un indicador de piece valido.')
        # if color != 1 or color != 0:
        #     raise ValueError(f'"{color}" no es un color valido.')
        # elif board_view != 1 or board_view != 0:
        #     raise ValueError(f'"{board_view}" la vista del tablero no es valida.')
        
        # Piece atributes
        self.type = type
        self.color = color
        self.board_view = board_view
        self.squares_limit = None
        self.movements = None
        self.first_move = first_move
        self.castling = False

        # Atributos de partida
        self.pinned = False
        self.available_movements = None
        self.position = {"row": canvas.coordts[0], "column": canvas.coordts[1]}

        self.set_atributes_to_piece_type()

        # Atributos de interfaz
        self.canvas = canvas
        self.imagen = ImageTk.PhotoImage(Image.open(self.img_path))
        self.id_piece = canvas.create_image(40, 40, image=self.imagen)

    def set_atributes_to_piece_type(self):
        if self.type == "K":
            self.img_path = IMG_REY_BLANCO if self.color else IMG_REY_NEGRO
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
   
        elif self.type == "Q":
            self.img_path = IMG_DAMA_BLANCA if self.color else IMG_DAMA_NEGRA
            self.movements = [(-1, -1), (-1, 1), (1, 1), (1, -1), 
                              (-1, 0), (1, 0), (0, -1), (0, 1)]
            self.squares_limit = 7

        elif self.type == "R":
            self.img_path = IMG_TORRE_BLANCA if self.color else IMG_TORRE_NEGRA
            self.movements = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            self.squares_limit = 7
            if self.first_move:
                if self.board_view == 1:
                    if self.color == 1 and (self.position == {"row": 7, "column": 0} or self.position == {"row": 7, "column": 7}):
                        self.castling = True
                    elif self.color == 0 and (self.position == {"row": 0, "column": 0} or self.position == {"row": 0, "column": 7}):
                        self.castling = True
                elif self.board_view == 0:
                    if self.color == 1 and (self.position == {"row": 0, "column": 0} or self.position == {"row": 0, "column": 7}):
                        self.castling = True
                    elif self.color == 0 and (self.position == {"row": 7, "column": 0} or self.position == {"row": 7, "column": 7}):
                        self.castling = True

        elif self.type == "B":
            self.img_path = IMG_ALFIL_BLANCO if self.color else IMG_ALFIL_NEGRO
            self.movements = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
            self.squares_limit = 7

        elif self.type == "N":
            self.img_path = IMG_CABALLO_BLANCO if self.color else IMG_CABALLO_NEGRO
            self.movements = [(-1, -2), (-2, -1), (-2, 1), (-1, 2), 
                              (1, 2), (2, 1), (2, -1), (1, -2)]
            self.squares_limit = 1

        elif self.type == "P": 
            self.img_path = IMG_PEON_BLANCO if self.color else IMG_PEON_NEGRO
                       
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
        return {'tipo': self.type, 'color': self.color, "first_move": self.first_move, "view": self.board_view} 