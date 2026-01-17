from tkinter import StringVar
from itertools import islice
import components.alert as alert
import components.project_vars as pv

BOARD_LIMIT = 8

"""
    El jugador (player) es una entidad que se encarga de realizar las tareas
    para llevar a cabo la partida; como mover las piezas (ver movimientos disponibles -
    clavar las piezas, validar el estado de la partida, etc), presionar el reloj,
    anotar los movimientos. Es un objeto totalmente integrado con el proyecto.
"""

class ChessPlayer():
    def __init__(self, board):
        # Chess Player Utilities
        self.ob_board = board
        self.board = self.ob_board.board

        # Chess player attributes to see
        self.board_view = [1, 0]                    # 1 Para Blancas | 0 Para Negras
        self.turn = [1, 0]                          # Switch para cambiar de turno
        self.last_move = ""
        self.pieces_to_move = None
        self.selected_square = None                 # Almacena la casilla que ha sido clickeada
        self.game_over = False

        self.fen_historial = []
        self.fen_index = 0
        self.castling = None
        self.en_passant = {'pawn': None, 'square': None}
        self.is_last_move_en_passant = False
        self.active_promotion = False
        self.promotion_selected = ""
        self.halfmove = 0
        self.fullmove = 1

        self.opponent_color = 0

        # Player attributes
        self._listeners = []

    def is_game_over(self):
        """ This function check the king status to certified that is in check mate or no.""" # Mejorar

        king_position = self.get_king_square(self.turn[0])
        king_status = self.is_square_attacked(king_position, 1)

        def is_triple_repetition():
            if not self.fen_historial:
                return
            
            fen_list = list(self.fen_historial)
            actual_fen = fen_list.pop()
            actual_fen = list([v for v in islice(actual_fen.split(), 3)])

            repetitions = 0
            for fen in fen_list[::-1]:
                fen_to_compare = list([v for v in islice(fen.split(), 3)])
                if fen_to_compare == actual_fen:
                    repetitions += 1
                if repetitions == 2:
                    return True
            return False

        # 50 movimiemtos
        def fifty_movements():
            if self.halfmove == 100:
                return True

        def is_there_enough_material():
            white_material = []
            black_material = []

            for row in self.board:
                for square in row:
                    if square.piece and square.piece.ptype != "K":
                        if square.piece.color == 1:
                            white_material.append(square.piece)
                        black_material.append(square.piece)
            if len(white_material) < 2 and len(black_material) < 2:
                for material in (white_material, black_material):
                    if material:
                        if material[0].ptype in ("Q", "R", "P"):
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
                if square.piece and square.piece.ptype == "K":
                    if square.piece.color == color:
                        return square

    def get_square_position(self, row, column): # No hacer cambios
        return f"{self.ob_board.column_letters[column]}{self.ob_board.row_numbers[row]}"

    def get_nomenclature_of_movement(self, old_coordts, new_coordts, piece_moved, piece_captured): # No hacer cambios
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
        ambiguity_indicator = ""
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

        def check_ambiguity(piece_moved, new_row, new_col):
            moves_and_move_limit_for_piece = {
                "Q": ([(-1, -1), (-1, 1), (1, 1), (1, -1), (-1, 0), (1, 0), (0, -1), (0, 1)], 7),
                "R": ([(-1, 0), (1, 0), (0, -1), (0, 1)], 7),
                "B": ([(-1, -1), (-1, 1), (1, 1), (1, -1)], 7),
                "N": ([(-1, -2), (-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2)], 1),}

            info_piece_to_check = {f"{piece_moved}": moves_and_move_limit_for_piece.get(piece_moved)}
            
            square_storage = []
            for rival_piece, values in info_piece_to_check.items():
                directions, number_of_movements = values
                for direction in directions:
                    y, x = new_row, new_col
                    for _ in range(0, number_of_movements):
                        y, x = y + direction[0], x + direction[1]
                        if y in range(0, BOARD_LIMIT) and x in range(0, BOARD_LIMIT):
                            if self.board[y][x].piece:
                                if self.board[y][x].piece.color == self.turn[0]:
                                    break
                                elif self.board[y][x].piece.color != self.turn[0]:
                                    if self.board[y][x].piece.ptype == rival_piece:
                                        square_storage.append(self.board[y][x])
                                    else:
                                        break
            return square_storage

        if piece_moved in ("RNBQ"):
            ambiguity = check_ambiguity(piece_moved=piece_moved, new_row=newrow, new_col=newcolumn)
            if ambiguity:
                ambiguity_indicator = self.get_square_position(row=oldrow, column=oldcolumn)

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
            
        if self.is_last_move_en_passant:
            ambiguity_indicator = self.ob_board.column_letters[oldcolumn]
            capture = "x"
            self.is_last_move_en_passant = False
        self.last_move = f"{piece_indicator}{ambiguity_indicator}{capture}{new_position}{self.promotion_selected}{check}"
        # self.promotion_selected = ""
        return self.last_move
    
    def get_fen(self): # Tal vez agregar un docstring
        """ Obtener el fen de la posición actual del tablero"""

        fen = []
        
        # Orde Pieces
        tablero = self.board
        if self.board_view[0] == 0:
            tablero = list(reversed(tablero))

            for row, contenido in enumerate(tablero):
                tablero[row] = list(reversed(contenido))
            
        for row in tablero:
            for square in row:
                if square.piece:
                    valor = square.piece.ptype.upper() if square.piece.color else square.piece.ptype.lower()
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

        return "".join(fen)

    def can_king_castling(self, king_color): # Tal vez agregar un docstring
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
                if square.piece and square.piece.ptype == "R":
                    if square.piece.color == self.turn[0]:
                        if square.piece.castling:
                            rook_to_castling.append(square)
        if not rook_to_castling:
            return False

        king_row, king_column = king_square.coordts
        left_rook = self.board[king_row][0]
        right_rook = self.board[king_row][-1]

        def is_there_a_rook(square):
            if square.piece and square.piece.ptype == "R":
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
                            if self.board[y][x].piece.ptype == "K" and self.board[y][x].piece.color == self.turn[0]:
                                continue
                            elif self.board[y][x].piece.color == self.turn[0]:
                                break
                            elif self.board[y][x].piece.color != self.turn[0]:
                                if self.board[y][x].piece.ptype == rival_piece:
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
                            if not self.board[y][x].piece.ptype in ("QRB"):
                                break
                            if direction in [(-1, -1), (-1, 1), (1, 1), (1, -1)]:
                                if self.board[y][x].piece.ptype in ("QB"):
                                    that_piece = self.board[y][x]
                                break
                            elif direction in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                                if self.board[y][x].piece.ptype in ("QR"):
                                    that_piece = self.board[y][x]
                                break
                    squares_between_king_and_rival_piece.append(self.board[y][x])                    
            if that_piece:
                squares_between_king_and_rival_piece.append(that_piece)
                if piece_to_pin:
                    piece_to_pin.pinned = True
                    piece_to_pin.available_movements = squares_between_king_and_rival_piece

    def move_piece(self, old_square, new_square): # Solo hace falta los 50 movimientos
        """ Move a piece.
        
            Args:
                old_square (object): square where the piece is.
                new_square (object): square where the piece will be placed.
        """

        piece = old_square.piece

        # To do it en-passant and reset en-passant info
        if piece.ptype == "P":
            if new_square == self.en_passant['square']:
                self.en_passant['pawn'].quit_piece()
                self.is_last_move_en_passant = True
        if self.en_passant:
            self.en_passant = {'pawn': None, 'square': None}

        # If the move is a castling
        def is_move_castling(row, column):
            # Left_castling
            new_coord = tuple([a + b for a, b in zip((row, column), (0, -2))])
            if new_coord == new_square.coordts:
                self.move_piece(self.board[row][0], self.board[row][column-1])

            # Right_castling
            new_coord = tuple([a + b for a, b in zip(old_square.coordts, (0, 2))])
            if new_coord == new_square.coordts:
                self.move_piece(self.board[row][-1], self.board[row][column+1])

        if piece.ptype == "K":
            row, column = old_square.coordts
            is_move_castling(row, column)

        # To get en-passant info if a pawn move 2 squares
        if piece.ptype == "P":
            movement_coords = tuple([i - j for i, j in zip(old_square.coordts, new_square.coordts)])
            new_row, new_column = new_square.coordts
            left_column = new_column - 1 
            rigth_column = new_column + 1
            there_is_a_pawn = False

            for column in (left_column, rigth_column):
                if column == left_column:
                    if left_column < 0:
                        continue
                if column == rigth_column:
                    if rigth_column > 7:
                        continue
                if self.board[new_row][column].piece:
                    if self.board[new_row][column].piece.ptype == "P":
                        if self.board[new_row][column].piece.color != self.turn[0]:
                            there_is_a_pawn = True

            if movement_coords == (2, 0):
                if there_is_a_pawn:
                    self.en_passant = {'pawn': new_square, 
                                        'square': self.board[new_row+1][new_column]}
            elif movement_coords == (-2, 0):
                if there_is_a_pawn:
                    self.en_passant = {'pawn': new_square, 
                                        'square': self.board[new_row-1][new_column]}

        # Quit first_move attribute in the piece
        if piece.ptype in ("P", "K", "R") and piece.first_move:
            piece.first_move = False
        # Promotion
        if piece.ptype == "P":
            if new_square in self.board[0] or new_square in self.board[7]:
                opponent_color = "white" if (self.turn[0] == 1) else "black"
                if self.opponent_color != opponent_color:
                    self.promotion_selected = StringVar(value="waitting")
                    pv.menu.show_promotion_menu(color="white" if (self.turn[0] == 1) else "black")
                    pv.window.wait_variable(self.promotion_selected)
                    att = piece.get_attributes()
                    att['tipo'] = self.promotion_selected.get()
                    new_square.put_piece(att)
                    old_square.quit_piece()
                    self.promotion_selected = self.promotion_selected.get().lower()
                    return
                else:
                    promotion = self.promotion_selected.upper()
                    att = piece.get_attributes()
                    att['tipo'] = promotion
                    new_square.put_piece(att)
                    old_square.quit_piece()
                    return

        att = piece.get_attributes()
        new_square.put_piece(att)
        old_square.quit_piece()

    def receive_movement(self, movement):
        if len(movement) == 5:
            self.promotion_selected = movement[-1]
            self.active_promotion = True
            movement = movement[:-1]

        old_position, new_position = movement[:2], movement[2:]
        old_square = self.ob_board.get_square_of_position(old_position)
        new_square = self.ob_board.get_square_of_position(new_position)

        self.start_process_to_move(old_square, new_square)

    def pass_turn(self): # No hacer cambios
        self.turn.reverse()

    def start_process_to_move(self, selected_square, square_touched): # Poner lo de promoción
        """ It's to do all process after start a move"""

        piece_captured, piece_moved = "", ""

        if selected_square.piece:
            piece_moved = selected_square.piece.ptype
        if square_touched.piece:
            piece_captured = square_touched.piece.ptype

        old_coordts = selected_square.coordts
        new_coordts = square_touched.coordts

        # mover pieza desde la casilla vieja 'selected_square' a la casilla nueva 'square_touched'
        self.move_piece(selected_square, square_touched)

        # pasar el turno al otro
        self.pass_turn()

        # quien recibe el turno valida si se han clavado alguna pieza
        self.pin_pieces()

        # se optiene la nomenclatura del movimiento
        nomencalture_movement = self.get_nomenclature_of_movement(old_coordts=old_coordts,
                                                                new_coordts=new_coordts,
                                                                piece_moved=piece_moved,
                                                                piece_captured=piece_captured)
                    
        # Enviamos el movimiento al panel
        pieces = "blacks" if self.turn[0] else "whites"
        pv.panel.insert_movement(pieces, nomencalture_movement)

        # Modificamos el contador de halfmove
        def update_halfmove():
            if not "x" in self.last_move:
                piezas_mayores = "RNBKQO"
                for pieza in piezas_mayores:
                    if pieza in self.last_move:
                        self.halfmove += 1
                        return
            self.halfmove = 0
        update_halfmove()

        # Modificamos el contador de fullmove
        if self.turn[0] == 1:
            self.fullmove += 1
    
        # Hacer el registro del fen
        self.fen_historial.append(self.get_fen())
        self.fen_index += 1

        self.active_promotion = False
        
        partide_status = self.is_game_over().get("status")
        if partide_status in ("checkmate", "stalemate"):
            if partide_status == "checkmate":
                if self.pieces_to_move == "all":
                    if self.turn[0] == 1:
                        alert.show_info(tittle="Partida finalizada.", message="¡Han ganado las Negras!")
                    elif self.turn[0] == 0:
                        alert.show_info(tittle="Partida finalizada.", message="¡Han ganado las Blancas!")
                elif self.pieces_to_move == 1:
                    if self.turn[0] == 1:
                        alert.show_info(tittle="Partida finalizada.", message="has perdido...")
                    elif self.turn[0] == 0:
                        alert.show_info(tittle="Partida finalizada.", message="¡HAS GANADO!")
                elif self.pieces_to_move == 0:
                    if self.turn[0] == 1:
                        alert.show_info(tittle="Partida finalizada.", message="¡HAS GANADO!")
                    elif self.turn[0] == 0:
                        alert.show_info(tittle="Partida finalizada.", message="has perdido...")
            elif partide_status == "stalemate":
                alert.show_info(tittle="Partida finalizada.", message="¡TABLAS!")
            pv.ongoing_game = False
            pv.clock.kill_timers()
            self.game_over = True

    def set_pieces_to_control(self, pieces_to_control):
        if pieces_to_control == 'all':
            self.pieces_to_move == 'all'
        elif pieces_to_control == 'white':
            self.pieces_to_move = 1
        elif pieces_to_control == 'black':
            self.pieces_to_move = 0
        else:
            txt = f'The value "{pieces_to_control}" is not valid.'
            raise ValueError(txt)
        
    def suscribe_observer(self, callback):
        if callback not in self._listeners:
            self._listeners.append(callback)

    def show_move(self, move):
        for callback in self._listeners:
            callback(move)

    def click_event(self, event): # Debería checar si hacer cambios
        """ Determines what action to take when a square is selected."""

        if self.active_promotion:
            return # The player can't touch when the promotion menu is active

        if self.fen_index != (len(self.fen_historial)-1):
            return # When the player is in other fen

        if self.game_over:
            return # When game is over

        if self.pieces_to_move != 'all':
            if not self.pieces_to_move == self.turn[0]:
                return # When isn't the player turn

        if pv.there_is_an_active_server and not pv.is_there_a_connected_player:
            return # When there is a connected game but isn't a connected player

        if pv.dont_touch:
            return # Is necesary that the player don't touch

        square_touched = event.widget
        if square_touched != self.selected_square:
            if square_touched.piece:
                if square_touched.piece.color == self.turn[0]:
                    if self.selected_square:
                        self.turn_off_highlights()
                    self.selected_square = square_touched
                    self.selected_square.active_selection = True
                    self.turn_on_highlights(self.selected_square)   
                else: # Capture
                    if square_touched.highlight and self.selected_square:
                        old = self.ob_board.get_position_of_square(self.selected_square) # Tal vez puede ponerse arriba en una sola línea
                        new = self.ob_board.get_position_of_square(square_touched)
                        self.promotion_selected = ""
                        self.start_process_to_move(self.selected_square, square_touched)
                        last_move = f"{old}{new}{self.promotion_selected}"
                        self.show_move(last_move)
                    self.turn_off_highlights()         
            else: # Movement
                if square_touched.highlight and self.selected_square:
                    old = self.ob_board.get_position_of_square(self.selected_square) # Tal vez puede ponerse arriba en una sola línea
                    new = self.ob_board.get_position_of_square(square_touched)
                    self.promotion_selected = ""
                    self.start_process_to_move(self.selected_square, square_touched)
                    last_move = f"{old}{new}{self.promotion_selected}"
                    self.show_move(last_move)
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

        self.ob_board.turn_off_highlights()
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
                if square.piece and square.piece.ptype == "R":
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

        if selected_square.piece.ptype == "K":
            if is_this_the_movement((0, -2)):
                return validate_castling((0, -2)) 
            if is_this_the_movement((0, 2)):
                return validate_castling((0, 2))
            if square_for_validation.piece and square_for_validation.piece.color == self.turn[0]:
                return False
            return not self.is_square_attacked(square_for_validation, 1)
    
        elif selected_square.piece.ptype == "P":
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
                    if square_for_validation.piece.color != self.turn[0] and square_for_validation.piece.ptype != "K":
                        return True
                    return False                  
                return True

    def set_fen_position(self, fen, board_view): # Revisar
        self.ob_board.clear_board()

        colocation, turn, castlings, en_passant, halfmove, fullmove = tuple(fen.split())

        # Definir vista del tablero
        if self.board_view[0] == 0:
            colocation = colocation[::-1]

        # Insertar piezas en el tablero
        row, column = 0, 0
        for value in colocation:
            if value.upper() in "RNBQKP":
                color = 1 if value.isupper() else 0
                self.ob_board.put_piece(self.board[row][column], 
                                        ptype=value.upper(), 
                                        color=color,
                                        board_view=board_view)
                column += 1
            elif value == "/":
                row += 1
                column = 0
            elif value in "123456789":
                v = int(value)
                column += v

        # Definimos el turno
        if turn == "w":
            self.turn = [1, 0]

        if turn == "b":
            self.turn = [0, 1]
        
        # Determinar si el rey puede enrocar
        if castlings != "-": # Puede mejorarse
            if not "K" in castlings:
                if self.board_view[0] == 1:
                    if self.board[7][7].piece: 
                        self.board[7][7].piece.castling = False
                if self.board_view[0] == 0:
                    if self.board[0][0].piece:
                        self.board[0][0].piece.castling = False
            if not "Q" in castlings:
                if self.board_view[0] == 1:
                    if self.board[7][0].piece:
                        self.board[7][0].piece.castling = False
                if self.board_view[0] == 0:
                    if self.board[0][7].piece:
                        self.board[0][7].piece.castling = False
            if not "k" in castlings:
                if self.board_view[0] == 1:
                    if self.board[0][7].piece:
                        self.board[0][7].piece.castling = False
                if self.board_view[0] == 0:
                    if self.board[7][0].piece:
                        self.board[7][0].piece.castling = False
            if not "q" in castlings:
                if self.board_view[0] == 1:
                    if self.board[0][0].piece:
                        self.board[0][0].piece.castling = False
                if self.board_view[0] == 0:
                    if self.board[7][7].piece: 
                        self.board[7][7].piece.castling = False

        # Para insertar el peón al paso del fen elegido (si tiene)
        if en_passant != "-":
            square = self.ob_board.get_square_of_position(en_passant)
            y, x = square.coordts
            if "3" in en_passant:
                if self.board_view[0] == 1:
                    pawn = self.board[y-1][x]
                if self.board_view[0] == 0:
                    pawn = self.board[y+1][x]
            if "6" in en_passant:
                if self.board_view[0] == 1:
                    pawn = self.board[y+1][x]
                if self.board_view[0] == 0:
                    pawn = self.board[y-1][x]
            self.en_passant = {'pawn': pawn, 'square': square}

        self.halfmove = int(halfmove)
        self.fullmove = int(fullmove)

    def active(self, fen, color_selected, opponent_color): # No hacer cambios
        if color_selected == "white":
            self.board_view = [1, 0]
        if color_selected == "black":
            self.board_view = [0, 1]

        if self.ob_board.view != self.board_view:
            self.ob_board.turn_the_board()

        self.opponent_color = opponent_color
        if opponent_color:
            self.pieces_to_move = color_selected
        else:
            self.pieces_to_move = "all"
        self.set_pieces_to_control(self.pieces_to_move)
            
        self.set_fen_position(fen, self.board_view[0])
        self.fen_historial.append(fen) # Mirar de ojo el tema con este fen
        self.ob_board.set_squares_callback(self.click_event)

    def restart(self):
        self.board_view = [1, 0]
        self.turn = [1, 0]
        self.last_move = ""
        self.pieces_to_move = None
        self.selected_square = None
        self.game_over = False

        self.fen_historial = []
        self.fen_index = 0
        self.castling = None
        self.en_passant = {'pawn': None, 'square': None}
        self.is_last_move_en_passant = False
        self.active_promotion = False
        self.promotion_selected = ""
        self.halfmove = 0
        self.fullmove = 1
        self.opponent_color = 0

    # Las funciones para mover el fen son similares, tal vez podría reducir código
    def first_fen(self):
        if not self.fen_historial:
            return
        self.fen_index = 0
        self.set_fen_position(self.fen_historial[self.fen_index], self.board_view[0])

    def last_fen(self):
        if not self.fen_historial:
            return
        self.fen_index = (len(self.fen_historial)-1)
        self.set_fen_position(self.fen_historial[self.fen_index], self.board_view[0])

    def previous_fen(self):
        if not self.fen_historial:
            return
        if self.fen_index == 0:
            return
        self.fen_index -= 1
        self.set_fen_position(self.fen_historial[self.fen_index], self.board_view[0])

    def next_fen(self):
        if not self.fen_historial:
            return
        if self.fen_index == (len(self.fen_historial)-1):
            return
        self.fen_index += 1 
        self.set_fen_position(self.fen_historial[self.fen_index], self.board_view[0])
