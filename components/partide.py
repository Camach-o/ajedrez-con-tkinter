import queue
import random
import threading
from time import sleep
import stockfish
from components import player
from components import server
import components.alert as alert
import components.project_vars as pv

class ChessPartide:
    VALID_GAME_MODE_TYPES = ('only', 'stockfish', 'connected')
    VALID_COLORS = ('white', 'black')
    VALID_STATUS_CLOCK = ('desactive', 'active')

    def __init__(self):

        # Ongoing game attributes
        self.game_mode = None
        self.color_selected = None
        self.clock_status = None
        self.fen = None
        self.time = None
        self.bonus = None
        self.player_moves = None
        self.player_turn = ['main_player', 'main_player']
        self.connected_partide_settings = None

        # Players
        self.main_player = None
        self.stockfish = None
        self.connection_server = None
        self.my_socket = None

        pv.clock.suscribe_observer(self.pause_connected_clock)
        self._init_main_player()

    def start_partide(self, game_mode, color_selected, clock_status, time, bonus, fen):
        """ Active the process to starts a partide."""

        # Check the values and save them
        self._validate_attributes(game_mode, color_selected, clock_status, fen)
        pv.clock.status = clock_status
        pv.clock.set_time(time, bonus)
        self.game_mode = game_mode
        self.color_selected = color_selected
        self.clock_status = clock_status
        self.time = time
        self.bonus = bonus
        self.fen = fen

        opponent_color = False
        if game_mode != 'only':
            opponent_color = "black" if color_selected == "white" else "white"

        if self.game_mode == 'stockfish':
            if self.stockfish is None:
                self._init_stockfish()
            self.stockfish.set_fen_position(fen)
            self.player_turn[1] = 'stockfish'

        elif self.game_mode == 'connected':
            self.player_turn[1] = 'connected_player'

        # Active the main player
        self.main_player.active(self.fen, self.color_selected, opponent_color=opponent_color)

        # Define the color that starts the partide
        turn = "white" if self.main_player.turn[0] == 1 else "black"
        if color_selected != turn:
            self.player_turn.reverse()
            pv.clock.starts_with_top_timer()
            if game_mode == "stockfish":
                self.player_moves.put('first_move')

        # Indicate that there is a ongoing game
        pv.ongoing_game = True

    def start_connected_partide(self, type_connection, partide_settings=None):
        """ Starts the process to connect whith other player."""
        if not self.connection_server:
            self.connection_server = server.Server()

        if type_connection == "host":
            pv.dont_touch = True
            self.connection_server.active_server()
            self.my_socket = self.connection_server.connect_to_server(type_connection="host")

        if type_connection == "guest":
            self.my_socket = self.connection_server.search_and_connect()
            if not self.my_socket:
                alert.show_info("Error de conexión", "No se ha logrado encontrar una partida en la red.")
                return
            pv.is_there_a_connected_player = True

        receive_data_thread = threading.Thread(target=self.connection_server.receive_data,
                                             args=(self.my_socket, self.receive_instructions),
                                             daemon=True)
        receive_data_thread.start()

        if type_connection == "host":
            self.connected_partide_settings = partide_settings
            game_mode, color_selected, clock_status, time, bonus, fen = partide_settings
            self.start_partide(game_mode, color_selected, clock_status, time, bonus, fen)

        if type_connection == "guest":
            self.my_socket.sendall("give_me_settings<>None".encode())

        pv.there_is_an_active_server = True

    def restart(self):
        """ Restart the current partide."""
        # Players
        if pv.there_is_an_active_server:
            self.connection_server.finish_connection()
            self.my_socket = None
        pv.is_there_a_connected_player = False
        pv.dont_touch = False

        # Restarts window components
        pv.panel.restart_movements_viewer()
        pv.clock.restart()
        self.main_player.restart()
        pv.ongoing_game = False

        # Ongoing game attributes
        self.game_mode = None
        self.color_selected = None
        self.clock_status = None
        self.fen = None
        self.time = None
        self.bonus = None
        self.player_turn = ['main_player', 'main_player']

    def get_new_movement(self, movement):
        """ Receive the new movement when a player moves."""
        self.main_player.last_fen()
        self.pass_turn(movement)

    def pass_turn(self, movement):
        """ Change the turn of the partide and passed the movement
            to the player that gets the turn.
        """
        if self.clock_status == 'active' and pv.ongoing_game:
            pv.clock.switch_active_timer()

        if self.player_turn[0] == 'main_player':
            if self.game_mode == 'stockfish':
                if pv.ongoing_game:
                    self.player_moves.put(movement)
            elif self.game_mode == 'connected':
                self.send_data(f"movement<>{movement}")

        elif self.player_turn[0] in ('stockfish', 'connected_player'):
            self.main_player.receive_movement(movement=movement)

        self.player_turn.reverse()

    def _init_main_player(self):
        if not self.main_player:
            self.main_player = player.ChessPlayer(board=pv.board)
            self.main_player.suscribe_observer(self.get_new_movement)

            # Here I can aplicate the single responsibility principle
            pv.panel.previous_fen_bttn.configure(command=self.main_player.previous_fen)
            pv.panel.first_fen_bttn.configure(command=self.main_player.first_fen)
            pv.panel.last_fen_bttn.configure(command=self.main_player.last_fen)
            pv.panel.next_fen_bttn.configure(command=self.main_player.next_fen)

    def _init_stockfish(self):
        self.player_moves = queue.Queue()
        if not self.stockfish:
            self.stockfish = stockfish.Stockfish(path="stockfish_module/stockfish/stockfish-windows-x86-64.exe")
            active_stockfish_thread = threading.Thread(target=self.activate_stockfish, daemon=True)
            active_stockfish_thread.start()

    def set_stockfish_difficulty(self, difficulty):
        if not self.stockfish:
            return
        if self.player_turn[0] == "stockfish":
            return

        elo = 0
        if difficulty == 0:
            elo = 800
        elif difficulty == 1:
            elo = 1100
        elif difficulty == 2:
            elo = 1400
        elif difficulty == 3:
            elo = 1700
        elif difficulty == 4:
            elo = 2000
        elif difficulty == 5:
            elo = 2300

        self.stockfish.set_elo_rating(elo)

    def activate_stockfish(self):
        """ This function is called in a Thread. Here is active Stockfish to process moves."""
        while True:
            movimiento = self.player_moves.get()
            if movimiento:
                sleep(random.randint(1, 3))
                if movimiento != 'first_move':
                    self.stockfish.make_moves_from_current_position([movimiento])
                last_move = self.stockfish.get_best_move()
                self.stockfish.make_moves_from_current_position([last_move])
                self.get_new_movement(last_move)
                self.player_moves.task_done()

    def finish_connected_partide(self):
        """ Tells to the connected player that the main player was disconnected."""
        self.send_data("finish_partide<>None")
        self.connection_server.finish_connection()

    def receive_instructions(self, data):
        """ Receive instructions when there are a connected partide."""
        instruction = data.split("<>")
        instruction_type, content = instruction
        print("Datos recibidos del servidor: ",instruction)
        if instruction_type == 'movement':
            self.get_new_movement(content)
        elif instruction_type == 'message':
            self.get_new_message(content)
        elif instruction_type == 'pause_clock':
            pv.clock.pause(content)
        elif instruction_type == 'finish_partide':
            self.connection_server.finish_connection()
        elif instruction_type == 'give_me_settings':
            game_mode, color_selected, clock_status, time, bonus, fen = self.connected_partide_settings
            color_selected = "black" if color_selected == "white" else "white"
            content = [game_mode, color_selected, clock_status, str(time), str(bonus), fen]
            content = ",".join(content)
            self.send_data(f"receive_settings<>{content}")
        elif instruction_type == 'receive_settings':
            game_mode, color_selected, clock_status, time, bonus, fen = content.split(",")
            self.start_partide(game_mode, color_selected, clock_status, int(time), int(bonus), fen)

    def send_data(self, data):
        """ Sends to a connected player information of the partide."""
        if not pv.there_is_an_active_server:
            return
        if self.my_socket:
            self.my_socket.sendall(f"{data}".encode())

    def pause_connected_clock(self):
        """ Tells to the connected player that the clock is paused."""
        if self.game_mode == 'connected':
            self.send_data("pause_clock<>connected_player")

    def get_new_message(self, message):
        """ When a connected player send us a message, this function calls to the
            chat to receive it.
        """
        pv.panel.receive_message(message, message_by="connected_player")

    def _validate_attributes(self, game_mode, color_selected, clock_status, fen):
        """ Check is the partide attributes are right."""
        if not game_mode in self.VALID_GAME_MODE_TYPES:
            raise ValueError(f'{game_mode} no es una opción valida')
        if not color_selected in self.VALID_COLORS:
            raise ValueError(f'{color_selected} no es una opción valida')
        if not clock_status in self.VALID_STATUS_CLOCK:
            raise ValueError(f'{clock_status} no es una opción valida')
        if not stockfish.Stockfish._is_fen_syntax_valid(fen=fen):
            raise ValueError(f'{fen} no es un fen valido')
