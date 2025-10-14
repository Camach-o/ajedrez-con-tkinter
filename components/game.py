from tkinter import *
if __name__ != "__main__":
    from components.pieces import *
    import components.project_vars as project_vars
    import components.board as board
    
else:
    from pieces import *
    import project_vars as project_vars
    import board as board
from PIL import Image, ImageTk

BOARD_LIMIT = 8

class ChessGame():
    def __init__(self, root):
        # ChessGame
        self.board_view = [1, 0]                    # 1 Para Blancas | 0 Para Negras
        self.ob_board = board.Board(root, self)
        self.board = self.ob_board.board
        self.fen_historial = []
        self.last_move = ""
        self.halfmove = 0
        self.fullmove = 0
        self.en_passant = {'pawn': None, 'square': None}
        self.castling = None
        self.turn = [1, 0]                          # Switch para cambiar de turno
        self.team_winner = None
        self.game_over = False

        self.fifty_movements_count = 0

        self.selected_square = None                 # Almacena la casilla que ha sido clickeada
        self.selected_piece = None                  # Almacena la piece que ha sido clickeada

        # Clock
        self.time = None
        self.bonus = None

        # Panel
        self.movement_index = None

    def is_game_over(self):
        """ This function check the king status to certified that is in check mate or no.""" # Mejorar

        king_position = self.get_king_square(self.turn[0])
        king_status = self.is_square_attacked(king_position, 1)

        def is_triple_repetition(): # Falta limitar lectura del fen (posición del tablero y enroques solamente)
            if not self.fen_historial:
                return
            
            fen_list = list(self.fen_historial)
            actual_fen = fen_list.pop()

            repetitions = 0
            for fen in fen_list[::-1]:
                if fen == actual_fen:
                    repetitions += 1
                if repetitions == 2:
                    return True
            return False

        # 50 movimiemtos
        def fifty_movements():
            
            # Si el movimiento anterior no fue captura de pieza y no fue movimiento de péon
                # sumar 1 al contador de los 50 movimientos

            if self.halfmove == 100:
                print("tablas por 50 movimientos")
            # si se han alcanzado 50 movimientos
                # retornar tablas por 50 movimientos

        def is_there_enough_material():
            white_material = []
            black_material = []

            for row in self.board:
                for square in row:
                    if square.piece and square.piece.type != "K":
                        if square.piece.color == 1:
                            white_material.append(square.piece)
                        black_material.append(square.piece)
            if len(white_material) < 2 and len(black_material) < 2:
                for material in (white_material, black_material):
                    if material:
                        if material[0].type in ("Q", "R", "P"):
                            return True
                return False
            return True

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
            check_squares = self.is_square_attacked(king_position, 2)
            if check_squares:
                for square in check_squares:
                    if square.highlight:
                        self.turn_off_highlights()
                        return True
            self.turn_off_highlights()
            return False

        if is_triple_repetition():
            return {"status": "stalemate", "reason": "triple repetition"}
        
        if fifty_movements():
            return {"status": "stalemate", "reason": "fifty movements"}
        
        if not is_there_enough_material():
            return {"status": "stalemate", "reason": "there is not enough material"}

        if king_status == 0: # Normal
            if not can_king_move() and not can_one_piece_move():
                return {"status": "stalemate", "reason": "there is not movements1"}
            return {"status": "continue", "reason": "is not checkmate"}

        if king_status == 1: # Check
            if not can_king_move():
                if not can_one_piece_defend():
                    return {"status": "checkmate", "reason": "checkmate"}
            return {"status": "check", "reason": "one piece is attacking"}

        if king_status == 2: # DoubleCheck
            if not can_king_move():
                return {"status": "checkmate", "reason": "checkmate for double check"}
            return {"status": "check", "reason": "check for double check"}

    def get_king_square(self, color): # No hacer cambios
        for row in self.board:
            for square in row:
                if square.piece and square.piece.type == "K":
                    if square.piece.color == color:
                        return square

    def get_square_position(self, row, column): # No hacer cambios
        return f"{self.ob_board.column_letters[column]}{self.ob_board.row_numbers[row]}"

    def get_movement(self, old_coordts, new_coordts, piece_moved, piece_captured): # No hacer cambios
        """ Returns a string indicating the last movement.

            Args:
                old_coordts (tuple): row and column indx of the old square
                new_coordts (tuple): row and column indx of the new square
                piece_moved (str): the letter of the piece to moved
                piece_captured (str): the letter of the piece captured
        """

        oldrow, oldcolumn = old_coordts
        newrow, newcolumn = new_coordts
        new_position = self.get_square_position(newrow, newcolumn)
        status_game = self.is_game_over()
        piece_indicator = piece_moved
        castling = ""
        capture = ""
        check = ""

        def is_move_castling(row, column):
            new_coord = tuple([a + b for a, b in zip((row, column), (0, -2))])
            if new_coord == (newrow, newcolumn):
                if self.board_view[0] == 1:
                    return "O-O-O"
                return "O-O"

            new_coord = tuple([a + b for a, b in zip(old_coordts, (0, 2))])
            if new_coord == (newrow, newcolumn):
                if self.board_view[0] == 1:
                    return "O-O"
                return "O-O-O"
            return False

        if not piece_moved in ("RNBQK"):
            piece_indicator = ""

        if piece_captured:
            if not piece_indicator:
                piece_indicator = self.ob_board.column_letters[oldcolumn]
            capture = "x"
        
        if status_game.get("status") == "check":
            check = "+"
        elif status_game.get("status") == "checkmate":
            check = "#"
        
        if piece_moved == "K":
            castling = is_move_castling(oldrow, oldcolumn)

        if castling:
            self.last_move = f"{castling}"
            return self.last_move
            
        self.last_move = f"{piece_indicator}{capture}{new_position}{check}"
        return self.last_move
    
    def get_fen(self):
        fen = []
        # Orde Pieces
        tablero = self.board
        if self.board_view[0] == 0:
            tablero = list(reversed(tablero))
        for row in tablero:
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
            if not row == tablero[-1]:
                fen.append("/")

        # Turn
        if self.turn[0]:
            fen.append(f" w ")
        else:
            fen.append(f" b ")
        # Castling
        white_castling = self.can_king_castling(1)
        black_castling = self.can_king_castling(0)
        if white_castling:
            fen.append(f"{white_castling}")
        if black_castling:
            fen.append(f"{black_castling.lower()}")
        if not white_castling and not black_castling:
            fen.append(f"-")
        # En Passant
        if self.en_passant["square"]:
            row, column = self.en_passant["square"].coordts
            fen.append(f" {self.get_square_position(row, column)}")
        else:
            fen.append(f" -")

        fen.append(f" {self.halfmove} {self.fullmove}")
        print("".join(fen))

        return "".join(fen)

    def can_king_castling(self, king_color):
        king_square = self.get_king_square(king_color)
        king = king_square.piece

        if self.board_view[0] == 1:
            left_castling = "Q"
            right_castling = "K"
        else:
            left_castling = "K"
            right_castling = "Q"

        if not king.castling:
            return False
        
        rook_to_castling = []
        for row in self.board:
            for square in row:
                if square.piece and square.piece.type == "R":
                    if square.piece.color == self.turn[0]:
                        if square.piece.castling:
                            rook_to_castling.append(square)
        if not rook_to_castling:
            return False

        king_row, king_column = king_square.coordts
        left_rook = self.board[king_row][0]
        right_rook = self.board[king_row][-1]

        def is_there_a_rook(square):
            if square.piece and square.piece.type == "R":
                return square.piece
            return False
        
        left_rook = is_there_a_rook(self.board[king_row][0])
        right_rook = is_there_a_rook(self.board[king_row][-1])

        valid_castling = ""
        if left_rook:
            if left_rook.castling:
                valid_castling += left_castling
        if right_rook:
            if right_rook.castling:
                valid_castling += right_castling

        if self.board_view[0] == 1:
            return valid_castling[::-1]
        else:
            return valid_castling

    def is_square_attacked(self, square, give_me): # No hacer cambios
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
                                    if give_me == 2:
                                        return square_storage
                                else:
                                    break
        if give_me == 1:
            return pieces_that_attack_the_square
    
    def pin_pieces(self): # Tal vez agregar un docstring
        for row in self.board:
            for square in row:
                if square.piece:
                    if square.piece.pinned:
                        square.piece.pinned = False
                        square.piece.available_movements = None

        king_position = self.get_king_square(self.turn[0])
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
                            if not self.board[y][x].piece.type in ("QRB"):
                                break
                            if direction in [(-1, -1), (-1, 1), (1, 1), (1, -1)]:
                                if self.board[y][x].piece.type in ("QB"):
                                    that_piece = self.board[y][x]
                                break
                            elif direction in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                                if self.board[y][x].piece.type in ("QR"):
                                    that_piece = self.board[y][x]
                                break
                    squares_between_king_and_rival_piece.append(self.board[y][x])                    
            if that_piece:
                squares_between_king_and_rival_piece.append(that_piece)
                if piece_to_pin:
                    piece_to_pin.pinned = True
                    piece_to_pin.available_movements = squares_between_king_and_rival_piece

    def move_piece(self, old_square, new_square): # Solo hace falta ponerle lo del peón al paso
        """ Move a piece.
        
            Args:
                old_square (object): square where the piece is.
                new_square (object): square where the piece will be placed.
        """

        piece = old_square.piece

        # For en-passant
        if piece.type == "P":
            if new_square == self.en_passant['square']:
                self.en_passant['pawn'].quit_piece()
        if self.en_passant:
            self.en_passant = {'pawn': None, 'square': None}

        # For castling
        def is_move_castling(row, column):
            # Left_castling
            new_coord = tuple([a + b for a, b in zip((row, column), (0, -2))])
            if new_coord == new_square.coordts:
                self.move_piece(self.board[row][0], self.board[row][column-1])
                if self.turn[0] == 1:
                    self.fullmove -= 1

            # Right_castling
            new_coord = tuple([a + b for a, b in zip(old_square.coordts, (0, 2))])
            if new_coord == new_square.coordts:
                self.move_piece(self.board[row][-1], self.board[row][column+1])
                if self.turn[0] == 1:
                    self.fullmove -= 1

        if piece.type == "K":
            row, column = old_square.coordts
            is_move_castling(row, column)

        # For double step
        if piece.type == "P":
            if (2, 0) == tuple([i - j for i, j in zip(old_square.coordts, new_square.coordts)]):
                row, column = tuple([i + j for i, j in zip(old_square.coordts, (-1, 0))])
                r, c = new_square.coordts
                if self.board[r][c-1].piece or self.board[r][c+1].piece:
                    self.en_passant = {'pawn': new_square, 'square': self.board[row][column]}
            elif (-2, 0) == tuple([i - j for i, j in zip(old_square.coordts, new_square.coordts)]):
                row, column = tuple([i + j for i, j in zip(old_square.coordts, (1, 0))])
                r, c = new_square.coordts
                if self.board[r][c-1].piece or self.board[r][c+1].piece:
                    self.en_passant = {'pawn': new_square, 'square': self.board[row][column]}

        # Quit first_move atribute in the piece
        if piece.type in ("P", "K", "R"):
            piece.first_move = False

        att = piece.get_atributes()
        new_square.put_piece(att)
        old_square.quit_piece()


        # def fifty_movements():
        #     print(self.last_move)
        #     if not "x" in self.last_move:
        #         self.halfmove += 1
        #         return
            
        #     piezas_mayores = "RNBKQ"
        #     for pieza in piezas_mayores:
        #         if pieza in self.last_move:
        #             break
        #     else:
        #         self.halfmove += 1
        #         return
            
        #     self.halfmove = 0

        # fifty_movements()
        # if self.turn[0] == 1:
        #     self.fullmove += 1

    def pass_turn(self): # No hacer cambios
        self.turn.reverse()

    def click_event(self, event): # Debería checar si hacer cambios
        """ Determines what action to take when a square is selected."""

        square = event.widget
        def actions():
            piece_captured = ""
            if square.piece:
                piece_captured = square.piece.type

            piece_moved = ""
            if self.selected_square.piece:
                piece_moved = self.selected_square.piece.type

            old_coordts = self.selected_square.coordts
            new_coordts = square.coordts

            self.move_piece(self.selected_square, square)
            self.pass_turn()
            self.fen_historial.append(self.get_fen())
            self.pin_pieces()
            self.is_game_over()
            self.get_movement(old_coordts=old_coordts,
                              new_coordts=new_coordts,
                              piece_moved=piece_moved,
                              piece_captured=piece_captured)

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
                        actions()
                    self.turn_off_highlights()         
            else: # Movement
                if square.highlight and self.selected_square:
                    actions()
                self.turn_off_highlights()
        else: # Deselect all squares 
            self.turn_off_highlights()
    
    def turn_on_highlights(self, square): # No hacer cambios
        """ Activate the marker on the selected square and on the squares that
          are available for moving the piece if there is one on the square.

            Args:
                square (Square): It is the square by which the function is called.
        """

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

    def turn_off_highlights(self): # No hacer cambios
        """ Move across the board to turn off the active highlights."""

        for row in self.board:
            for square in row:
                if square.highlight:
                    square.turn_off_highlight()
        if self.selected_square:                    
            self.selected_square.active_selection = False
            self.selected_square = 0

    def validate_highlight(self, square_for_validation, selected_square): # No hacer cambios
        """ Check that the conditions for activating the highlight of the square are met.
        
            Args:
                square_for_validation (Square): Square in which the highlight will be activated.
                selected_square (Square): Selected square for which the function is called.
        """

        king_status = self.is_square_attacked(self.get_king_square(self.turn[0]), 1)
        check_squares = self.is_square_attacked(self.get_king_square(self.turn[0]), 2)

        def is_this_the_movement(movement):
            """ Returns true when the movement being queried is the one currently being performed."""
            new_coordts = square_for_validation.coordts
            old_coordts = tuple(selected_square.coordts)
            if new_coordts == tuple([i + j for i, j in zip(old_coordts, movement)]):
                return True
            return False

        def validate_castling(side):
            if square_for_validation.piece:
                return False
            elif not (selected_square.piece.castling and not self.is_square_attacked(selected_square, 1)):
                return False
            
            def is_there_a_rook(square):
                if square.piece and square.piece.type == "R":
                    return square.piece
                return False
                
            def can_rook_castling(rook, next_king):
                if rook.castling:
                    row, column = [i + j for i, j in zip(selected_square.coordts, next_king)]
                    if not self.board[row][column].piece:
                        if not self.is_square_attacked(self.board[row][column], 1):
                            if not self.is_square_attacked(square_for_validation, 1):
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
            if is_this_the_movement((0, 2)):
                return validate_castling((0, 2))
            if square_for_validation.piece and square_for_validation.piece.color == self.turn[0]:
                return False
            return not self.is_square_attacked(square_for_validation, 1)
    
        elif selected_square.piece.type == "P":
            piece_coordts = tuple(selected_square.piece.position.values())
            if selected_square.piece.color == self.board_view[0]:
                if is_this_the_movement((-1, -1)) or is_this_the_movement((-1, 1)):
                    if not square_for_validation.piece:
                        if not square_for_validation == self.en_passant['square']:
                            return False             
                elif is_this_the_movement((-2, 0)):
                    row, column = tuple([i + j for i, j in zip(piece_coordts, (-1, 0))])
                    if self.board[row][column].piece:
                        return False
                    row, column = tuple([i + j for i, j in zip(piece_coordts, (-2, 0))])
                    if self.board[row][column].piece:
                        return False
                elif is_this_the_movement((-1, 0)):
                    row, column = tuple([i + j for i, j in zip(piece_coordts, (-1, 0))])
                    if self.board[row][column].piece:
                        return False
                    
            else:
                if is_this_the_movement((1, 1)) or is_this_the_movement((1, -1)):
                    if not square_for_validation.piece:
                        if not square_for_validation == self.en_passant['square']:
                            return False
                elif is_this_the_movement((2, 0)):
                    row, column = tuple([i + j for i, j in zip(piece_coordts, (1, 0))])
                    if self.board[row][column].piece:
                        return False
                    row, column = tuple([i + j for i, j in zip(piece_coordts, (2, 0))])
                    if self.board[row][column].piece:
                        return False
                elif is_this_the_movement((1, 0)):
                    row, column = tuple([i + j for i, j in zip(piece_coordts, (1, 0))])
                    if self.board[row][column].piece:
                        return False

        if king_status == 2:
            return False
        elif king_status == 1:
            if not selected_square.piece.pinned and square_for_validation in check_squares:
                return True
            return False
        elif king_status == 0:
            if selected_square.piece.pinned:
                if square_for_validation in selected_square.piece.available_movements:
                    return True
                return False
            else:
                if square_for_validation.piece:
                    if square_for_validation.piece.color != self.turn[0] and square_for_validation.piece.type != "K":
                        return True
                    return False                  
                return True

    def start(self): # No hacer cambios
        self.ob_board.put_board()
        self.ob_board.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR", self.board_view[0])

if __name__ == "__main__":
    root = Tk()
    juego = ChessGame(root)
    juego.start()
    root.mainloop()