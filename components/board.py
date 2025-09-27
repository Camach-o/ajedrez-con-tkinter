from tkinter import *
if __name__ != "__main__":
    from components.pieces import *
    import components.project_vars as project_vars
    
else:
    from pieces import *
    import project_vars as project_vars
from PIL import Image, ImageTk

BOARD_LIMIT = 8
TEMA_PREDETERMINADO_TABLERO = ("#bb935b", "#592f0a") # Blanco | Negro

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
    def __init__(self, container):
        # Ventana
        self.board_container = container

        # Tablero
        self.board = [[0 for _ in range(0, BOARD_LIMIT)] for _ in range(0, BOARD_LIMIT)]
        self.theme = {"white": "#bb935b", "black": "#592f0a"}
        self.board_view = [1, 0]                    # 1 Para Blancas | 0 Para Negras
        self.selected_square = None                 # Almacena la casilla que ha sido clickeada
        self.selected_piece = None                  # Almacena la piece que ha sido clickeada
        self.turn = [1, 0]                          # Switch para cambiar de turno
        self.check = 0                              # Valor de indicación para determinar si hay jaque
        self.check_squares = []                     # Casillas donde hay jaque
        self.king = None                            # Almacena al rey
        self.last_play = None

        self.row_numbers = ["8", "7", "6", "5", "4", "3", "2", "1"]
        self.row_labels = []
        self.column_letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
        self.column_labels = []
        self.en_passant = {'pawn': None, 'square': None}

        # Movimientos
        self.pgn = []
        self.ultimo_movimiento = None

    #################### Creación GUI del tablero ###########################

    def _create_board_squares(self): # No modificar
        """ Create and set the squares on the board."""

        for row in range(0, BOARD_LIMIT):
            for column in range(0, BOARD_LIMIT):
                square_widget = Square(self.board_container, coord=(row, column))
                square_widget.bind('<Button-1>', self.click_event)
                square_widget.pack_propagate(False)
                square_widget.grid(row=row, column=column)
                self.board[row][column] = square_widget

    def _create_position_labels(self): # No modificar
        """ Create and put the position labels."""

        for row, n in enumerate(self.row_numbers):
            square = self.board[row][0]
            num = square.create_text(12, 14, text=n, font=("Arial Black", 16))
            self.row_labels.append(num)

        for column, n in enumerate(self.column_letters):
            square = self.board[7][column]
            let = square.create_text(70, 68, text=n, font=("Arial Black", 16))
            self.column_labels.append(let)

    def _create_pieces(self): # No parece ser necesario modificar
        """ Create the pieces and place them in their starting positions on the board."""

        for piece_group in ({"row": 0, "color": 0 if self.board_view[0] else 1}, 
                            {"row": 7, "color": 1 if self.board_view[0] else 0}):
            for column, type in enumerate(("R", "N", "B", "Q", "K", "B", "N", "R") if self.board_view[0] else ("R", "N", "B", "K", "Q", "B", "N", "R")):
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
        piece = Piece(self.board[7][4], color=1, type="R", board_view=self.board_view[0])
        self.board[7][4].piece = piece

        piece = Piece(self.board[0][0], color=0, type="R", board_view=self.board_view[0])
        self.board[0][0].piece = piece

        piece = Piece(self.board[3][4], color=1, type="C", board_view=self.board_view[0])
        self.board[3][4].piece = piece

        piece = Piece(self.board[0][4], color=0, type="D", board_view=self.board_view[0])
        self.board[0][4].piece = piece

        piece = Piece(self.board[4][4], color=1, type="P", board_view=self.board_view[0])
        self.board[4][4].piece = piece

        piece = Piece(self.board[6][0], color=1, type="P", board_view=self.board_view[0])
        self.board[6][0].piece = piece

    def set_theme(self, white, black): # No modificar
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

    def turn_the_board(self): # No modificar
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
        self._create_pieces()

    def clear_board(self): # Ver si puedo eliminar las pieces
        """ Remove pieces and reset board values."""
        
        for row in self.board:
            for square in row:
                if square.piece:
                    square.delete(square.piece.id_piece)
                    square.piece = None
        self.turn_off_highlights()

    #################### Creación GUI del tablero #####################
   

    #################### Estado de la partida ########################

    def _is_game_over(self):
        """ This function check the king status to certified that is in check mate or no.""" # Mejorar

        # Rey y rey
        # Material insuficiente
        # 50 movimiemtos
        # Triple repetición


        king_position = self._get_king_position()
        king_status = self._is_square_attacked(king_position, 1)

        def is_there_one_active_highlight():
            for row in self.board:
                for square in row:
                    if square.highlight:
                        if square.piece:
                            if square.piece.color == self.turn[0]:
                                continue
                        self.turn_off_highlights()
                        return True
            return False

        def can_king_move():
            self.turn_off_highlights()
            self.turn_on_highlights(king_position)
            return is_there_one_active_highlight()

        def can_one_piece_move():
            self.turn_off_highlights()
            for row in self.board:
                for square in row:
                    if square.piece:
                        if square.piece.color == self.turn[0]:
                            self.turn_on_highlights(square)
            return is_there_one_active_highlight()

        def can_one_piece_defend():
            self.turn_off_highlights()
            for row in self.board:
                for square in row:
                    if square.piece:
                        if square.piece.color == self.turn[0]:
                            self.turn_on_highlights(square)
            check_squares = self._is_square_attacked(self._get_king_position(), 2)
            if check_squares:
                for square in check_squares:
                    if square.highlight:
                        self.turn_off_highlights()
                        return True
            self.turn_off_highlights()
            return False

        if king_status == 0: # Normal
            # Si el rey puede mover o alguna pieza puede mover
            if can_king_move() or can_one_piece_move():
                # No es tablas
                print("continuar partida")
            else: # Si el rey no puede mover y ninguna pieza puede mover
                # Es tablas
                print("no continuar partida tabla")

        elif king_status == 1: # Check
            if can_king_move():
                # No es jaque mate
                print("continuar partida 1")
            else: # Si no se puede mover  
                # Si una pieza puede defender
                if can_one_piece_defend():
                    print("continuar partida 2")
                else:
                    print("no continuar partida jaque")

        elif king_status == 2: # DoubleCheck
                pass
            # Revisamos si el rey se puede mover
                # Si se puede mover
                if can_king_move():
                    # No es jaque mate
                    print("continuar partida")
                else: # Si no se puede mover
                    # Es jaque mate
                    print("no continuar partida doble")

    def _get_king_position(self): # No modificar
        for row in self.board:
            for square in row:
                if square.piece and square.piece.type == "R":
                    if square.piece.color == self.turn[0]:
                        return square

    def _pin_pieces(self):
        for row in self.board:
            for square in row:
                if square.piece:
                    if square.piece.pinned:
                        square.piece.pinned = False
                        square.piece.available_movements = None

        king_position = self._get_king_position()
        directions = [(-1, -1), (-1, 1), (1, 1), (1, -1), (-1, 0), (1, 0), (0, -1), (0, 1)]
        for direction in directions:
            piece_to_pin = None
            that_piece = None
            squares_between_king_and_rival_piece = []
            y, x = king_position.coordts[0], king_position.coordts[1]
            for _ in range(0, 7):
                y, x = y + direction[0], x + direction[1]
                if y in range(0, BOARD_LIMIT) and x in range(0, BOARD_LIMIT):
                    if self.board[y][x].piece:
                        if self.board[y][x].piece.color == self.turn[0]:
                            if piece_to_pin:
                                break
                            piece_to_pin = self.board[y][x].piece
                        else:
                            if not self.board[y][x].piece.type in ("Q", "R", "B"):
                                break
                            if direction in [(-1, -1), (-1, 1), (1, 1), (1, -1)]:
                                if self.board[y][x].piece.type in ("Q", "B"):
                                    that_piece = self.board[y][x]
                                break
                            elif direction in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                                if self.board[y][x].piece.type in ("Q", "R"):
                                    that_piece = self.board[y][x]
                                break
                    squares_between_king_and_rival_piece.append(self.board[y][x])                    
            if that_piece:
                squares_between_king_and_rival_piece.append(that_piece)
                if piece_to_pin:
                    piece_to_pin.pinned = True
                    piece_to_pin.available_movements = squares_between_king_and_rival_piece

    def get_fen(self):
        # row_fen = None
        # row_free_squares = 0

        fen = []
        for row in self.board:
            for square in row:
                if square.piece:
                    valor = square.piece.type.upper() if square.piece.color else square.piece.type.lower()
                    fen.append(valor)
                else:
                    try:
                        valor = int(fen[-1])
                    except:
                        valor = None
                    if valor:
                        valor += 1
                        fen[-1] = str(valor)
                    else:
                        fen.append("1")
            fen.append("/")

        if self.turn[0]:
            fen.append(f" w")
        else:
            fen.append(f" b")
        fen.append(f" KQkq")
        if self.en_passant["square"]:
            row, column = self.en_passant["square"].coordts
            fen.append(f" {self.get_movement(row, column)}")
        else:
            fen.append(f" -")

        print("".join(fen))



                

    #################### Estado de la partida ########################


    #################### Sistema de movimiento #############

    def click_event(self, event): # Puede resumirse el código
        """ Determina qué acción toma el evento desencadenado por la casilla seleccionada."""

        square = event.widget
        if square != self.selected_square:
            if square.piece:
                if square.piece.color == self.turn[0]:
                    if self.selected_square:
                        self.turn_off_highlights()
                    self.selected_square = square
                    self.selected_square.active_selection = True
                    self.turn_on_highlights(self.selected_square)   
                else: # Capture
                    if square.highlight and self.selected_square:
                        self.move_piece(self.selected_square, square)
                        self.pass_turn()
                        self._pin_pieces()
                        self._is_game_over()
                    self.turn_off_highlights()         
            else: # Movement
                if square.highlight and self.selected_square:
                    self.move_piece(self.selected_square, square)
                    self.pass_turn()
                    self._pin_pieces()
                    self._is_game_over()
                self.turn_off_highlights()
        else: # Deselect all squares 
            self.turn_off_highlights()
    
    def turn_on_highlights(self, square): # Metodo (No parece necesitar cambios) 
        """ Activa el highlight de la casilla seleccionada y de las casillas hábiles para mover o capturar."""
        
        square.turn_on_highlight()
        for direction in square.piece.movements:
            y, x = square.coordts[0], square.coordts[1]
            for _ in range(0, square.piece.squares_limit):
                y, x = y + direction[0], x + direction[1]
                if y in range(0, BOARD_LIMIT) and x in range(0, BOARD_LIMIT):
                    if self.validate_highlight(self.board[y][x], square):
                        self.board[y][x].turn_on_highlight()
                    if self.board[y][x].piece:
                        break

    def turn_off_highlights(self): # Metodo (No parece necesitar cambios)
        """ Recorre el tablero para turn_off los highlights de casilla activos."""

        for fila in self.board:
            for casilla in fila:
                if casilla.highlight:
                    casilla.turn_off_highlight()
        if self.selected_square:                    
            self.selected_square.active_selection = False
            self.selected_square = 0

    def validate_highlight(self, square_for_validation, selected_square): # Funcion 
        """ Check that the conditions for activating the highlight of the square are met.
        
            Args:
                square_for_validation (object): Square in which the highlight will be activated.
                selected_square (object): Selected square for which the function is called.
        """

        def is_this_the_movement(movement):
            """ Returns true when the movement being queried is the one currently being performed."""
            new_corrdts = square_for_validation.coordts
            old_coordts = tuple(selected_square.coordts)
            if new_corrdts == tuple([i + j for i, j in zip(old_coordts, movement)]):
                return True
            return False

        def validate_castling(side):
            if square_for_validation.piece:
                return False
            if not (selected_square.piece.castling and not self._is_square_attacked(selected_square, 1)):
                return False
            
            def is_there_a_rook(square):
                if square.piece and square.piece.type == "R":
                    return square.piece
                return False
                
            def can_rook_castling(rook, next_king):
                if rook.castling:
                    row, column = [a + b for a, b in zip(selected_square.coordts, next_king)]
                    if not self.board[row][column].piece:
                        if not self._is_square_attacked(self.board[row][column], 1):
                            if not self._is_square_attacked(square_for_validation, 1):
                                return True
                return False

            king_row = selected_square.coordts[0]
            left_rook = is_there_a_rook(self.board[king_row][0])
            right_rook = is_there_a_rook(self.board[king_row][-1])
            if left_rook or right_rook:
                if left_rook and side == (0, -2):
                    return can_rook_castling(left_rook, (0, -1))
                elif right_rook and side == (0, 2):
                    return can_rook_castling(right_rook, (0, 1))
            return False

        if selected_square.piece.type == "K":
            if is_this_the_movement((0, -2)):
                return validate_castling((0, -2)) 
            elif is_this_the_movement((0, 2)):
                return validate_castling((0, 2))
            elif square_for_validation.piece and square_for_validation.piece.color == self.turn[0]:
                return False
            else:
                return not self._is_square_attacked(square_for_validation, 1)
    
        if selected_square.piece.type == "P":
            piece_coordts = tuple(selected_square.piece.position.values())
            if selected_square.piece.color == self.board_view[0]:
                if is_this_the_movement((-1, -1)) or is_this_the_movement((-1, 1)):
                    if not square_for_validation.piece:
                        if not square_for_validation == self.en_passant['square']:
                            return False             
                elif is_this_the_movement((-2, 0)) or is_this_the_movement((-1, 0)):
                    row, column = tuple([i + j for i, j in zip(piece_coordts, (-1, 0))])
                    if self.board[row][column].piece:
                        return False
            else:
                if is_this_the_movement((1, 1)) or is_this_the_movement((1, -1)):
                    if not square_for_validation.piece:
                        if not square_for_validation == self.en_passant['square']:
                            return False
                elif is_this_the_movement((2, 0)) or is_this_the_movement((1, 0)):
                    row, column = tuple([i + j for i, j in zip(piece_coordts, (1, 0))])
                    if self.board[row][column].piece:
                        return False

        king_status = self._is_square_attacked(self._get_king_position(), 1)
        check_squares = self._is_square_attacked(self._get_king_position(), 2)
        if king_status:
            if king_status == 1:
                return True if not selected_square.piece.pinned and square_for_validation in check_squares else False               
            elif king_status == 2:
                return False
        else:
            if selected_square.piece.pinned:
                return True if square_for_validation in selected_square.piece.available_movements else False
            else:
                if square_for_validation.piece:
                    return True if square_for_validation.piece.color != self.turn[0] and square_for_validation.piece.type != "K" else False                  
                else:
                    return True

    def _is_square_attacked(self, square, give_me): # Funcion
        """ Check if the square is under attack.

            Arg:
                square (object Square): It is the square through which the function is called.
                give_me (int): A number indicating the value to be returned.
                1 to pieces_that_attack_the_square | 2 check_squares
            
            Return:
                pieces_that_attack_the_square: A number that represent the square status
                0 to normal | 1 to is attacked for one piece | 2 is attacked for two piece
                check_squares (list): List with the squares between the king and the rival piece.

            Also the function save the squares between the square and the rival piece that attacked it.
        """

        pieces_that_attack_the_square = 0
        check_squares = None

        moves_and_move_limit_for_piece = {
            "K": ([(-1, -1), (-1, 1), (1, 1), (1, -1), (-1, 0), (1, 0), (0, -1), (0, 1)], 1),
            "Q": ([(-1, -1), (-1, 1), (1, 1), (1, -1), (-1, 0), (1, 0), (0, -1), (0, 1)], 7),
            "R": ([(-1, 0), (1, 0), (0, -1), (0, 1)], 7),
            "B": ([(-1, -1), (-1, 1), (1, 1), (1, -1)], 7),
            "N": ([(-1, -2), (-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2)], 1),
            "P": ([(-1, -1), (-1, 1)] if self.turn[0] else [(1, -1), (1, 1)], 1) 
                  if self.board_view[0] else 
                  ([(1, -1), (1, 1)] if self.turn[0] else [(-1, -1), (-1, 1)], 1)}

        for rival_piece, values in moves_and_move_limit_for_piece.items():
            directions, number_of_movements = values
            for direction in directions:
                square_storage = []
                y, x = square.coordts[0], square.coordts[1]
                for _ in range(0, number_of_movements):
                    y, x = y + direction[0], x + direction[1]
                    if y in range(0, BOARD_LIMIT) and x in range(0, BOARD_LIMIT):
                        square_storage.append(self.board[y][x])
                        if self.board[y][x].piece:
                            if self.board[y][x].piece.type == "K" and self.board[y][x].piece.color == self.turn[0]:
                                continue
                            elif self.board[y][x].piece.color == self.turn[0]:
                                break
                            elif self.board[y][x].piece.color != self.turn[0]:
                                if self.board[y][x].piece.type == rival_piece:
                                    pieces_that_attack_the_square += 1
                                    check_squares = square_storage
                                else:
                                    break
        
        if give_me == 1:
            return pieces_that_attack_the_square
        elif give_me == 2:
            if pieces_that_attack_the_square == 1:
                return check_squares
            else:
                return False
    
    def get_movement(self, row, colum):
        return f"{self.column_letters[colum]}{self.row_numbers[row]}"

    def move_piece(self, old_square, new_square): # Solo hace falta ponerle lo del peón al paso
        """ Move a piece.
        
            Args:
                old_square (object): square where the piece is.
                new_square (object): square where the piece will be placed.
        """

        piece = old_square.piece

        if piece.type == "P":
            if new_square == self.en_passant['square']:
                self.en_passant['pawn'].quit_piece()

        if self.en_passant:
            self.en_passant = {'pawn': None, 'square': None}

        def is_move_castling():
            row, column = old_square.coordts

            # Left_castling
            new_coord = tuple([a + b for a, b in zip((row, column), (0, -2))])
            if new_coord == new_square.coordts:
                self.move_piece(self.board[row][0], self.board[row][column-1])

            # Right_castling
            new_coord = tuple([a + b for a, b in zip(old_square.coordts, (0, 2))])
            if new_coord == new_square.coordts:
                self.move_piece(self.board[row][-1], self.board[row][column+1])

        if piece.type == "K":
            is_move_castling()

        if piece.type == "P":
            if (2, 0) == tuple([i - j for i, j in zip(old_square.coordts, new_square.coordts)]):
                row, colum = tuple([i + j for i, j in zip(old_square.coordts, (-1, 0))])
                self.en_passant = {'pawn': new_square, 'square': self.board[row][colum]}
            elif (-2, 0) == tuple([i - j for i, j in zip(old_square.coordts, new_square.coordts)]):
                row, colum = tuple([i + j for i, j in zip(old_square.coordts, (1, 0))])
                self.en_passant = {'pawn': new_square, 'square': self.board[row][colum]}


        if piece.type in ("P", "K", "R"):
            piece.first_move = False

        att = piece.get_atributes()
        new_square.put_piece(att)
        old_square.quit_piece()


        self.get_fen()

    def pass_turn(self): # Revisar
        self.turn.reverse()

    #################### Sistema de movimiento ########################







    #################### Función para inicializar el tablero ########################

    def start_board(self):
        """Llama a las funciones que crean la interfaz gráfica y objetos del tablero"""
        self._create_board_squares()
        self._create_position_labels()
        self._create_pieces()
        # self.pieces_pruebas()
        self.set_theme(self.theme.get("white"), self.theme.get("black"))


if __name__ == "__main__":
    root = Tk()
    board = Board(root)
    board.start_board()
    root.bind("<Key>", lambda _:board.turn_the_board())
    root.mainloop()