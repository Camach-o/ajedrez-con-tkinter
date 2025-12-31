import threading
import stockfish
import queue
import random
# import time
# import secrets
from time import sleep
import components.project_vars as pv
from components import player
# import server
import threading
# import socket

""" DEFAULT 
    game_mode='only'
    color_selected='white'
    clock_status='desactive'
    fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
"""

class ChessPartide:
    VALID_GAME_MODE_TYPES = ('only', 'stockfish', 'connected')
    VALID_COLORS = ('white', 'black')
    VALID_STATUS_CLOCK = ('desactive', 'active')
    
    def __init__(self):

        self.game_mode = None
        self.color_selected = None
        self.clock_status = None
        self.fen = None

        self.main_player = None
        self.stockfish = None

        self.fen_historial = []
        self.movement_historial = []
        
        self.status = False

        self.player_moves = None
        self.stockfish_thread = None
        self.stockfish_active_move = set()
        self.player_turn = ['main_player', 'main_player']
        self.color_turn = [1, 0]

        pv.clock.suscribe_a_watcher(self.pause_clock)

        # self.my_socket = None
        # self.server_socket =  None
        # self.connected_players = []
        # self.private_code_to_connect = ""
        # self.connected_partide_settings = {}

        # self.connection_type = 'host' # | 'guest'

    def _validate_atributes(self): 
        """
        """
        if not self.game_mode in self.VALID_GAME_MODE_TYPES:
            raise ValueError(f'{self.game_mode} no es una opción valida')
        if not self.color_selected in self.VALID_COLORS:
            raise ValueError(f'{self.color_selected} no es una opción valida')
        if not self.clock_status in self.VALID_STATUS_CLOCK:
            raise ValueError(f'{self.clock_status} no es una opción valida')
        if not stockfish.Stockfish._is_fen_syntax_valid(fen=self.fen):
            raise ValueError(f'{self.fen} no es un fen valido')

    def _init_main_player(self):
        if not self.main_player:
            self.main_player = player.ChessPlayer(board=pv.board)
            self.main_player.suscribe_a_watcher(self.get_new_movement)

            pv.panel.previous_fen_bttn.configure(command=self.main_player.previous_fen)
            pv.panel.first_fen_bttn.configure(command=self.main_player.first_fen)
            pv.panel.last_fen_bttn.configure(command=self.main_player.last_fen)
            pv.panel.next_fen_bttn.configure(command=self.main_player.next_fen)

    def _init_stockfish(self):
        self.player_moves = queue.Queue()
        if not self.stockfish:
            self.stockfish = stockfish.Stockfish(path="stockfish_module/stockfish/stockfish-windows-x86-64.exe")
            self.stockfish_thread = threading.Thread(target=self.activate_stockfish, daemon=True)
            self.stockfish_thread.start()

    def _init_connection(self):
        if self.connection_type == 'host':
            pass
            # self.private_code_to_connect = '555' #secrets.token_hex(5)
            # print(self.private_code_to_connect)
            # self.active_server()
            # self.connect_to_server()

    def set_stockfish_difficulty(self, difficulty: int = 1) -> None:

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

        while True:
            # movement = 1
            movimiento = self.player_moves.get()
            if movimiento == 'first_move':
                last_move = self.stockfish.get_best_move()
                self.stockfish.make_moves_from_current_position([last_move])
                self.get_new_movement(last_move)
                self.player_moves.task_done()
                continue

            if movimiento:
                self.stockfish.make_moves_from_current_position([movimiento])
                last_move = self.stockfish.get_best_move()
                sleep(random.randint(1, 3))
                self.stockfish.make_moves_from_current_position([last_move])
                self.get_new_movement(last_move)
                self.player_moves.task_done()

    def start_partide(self, game_mode, color_selected, clock_status, time, bonus, fen):
        """ Esta función será para activar los mecanismos que empiezan la partida
        
        """

        # terminar última partida
        if self.status:
            self.restart()

        opponent = False

        self.game_mode = game_mode
        self.color_selected = color_selected
        self.clock_status = clock_status
        self.fen = fen
        self._validate_atributes()

        pv.clock.status = self.clock_status
        pv.clock.update_clock_timers(time, bonus)

        if self.main_player == None:
            self._init_main_player()
            opponent = False

        if self.game_mode == 'stockfish':
            if self.stockfish == None:
                self._init_stockfish()
            self.stockfish.set_fen_position(fen) 
            opponent = "black" if color_selected == "white" else "white"
            self.player_turn[1] = 'stockfish'

        elif self.game_mode == 'connected':
            if self.connection_type == 'host':
                self.connected_partide_settings = (game_mode, color_selected, clock_status, time, bonus, fen)
                self._init_connection()
            opponent = "black" if color_selected == "white" else "white"
            self.player_turn[1] = 'connected_player'

        # Activar al jugador principal
        self.main_player.active(self.fen, self.color_selected, opponent=opponent)
        self.color_turn = self.main_player.turn

        # Defino el turno y hago que comience quien le corresponda
        turn = "white" if self.color_turn[0] == 1 else "black" # Esto lo puedo cambiar
        if color_selected != turn:
            self.player_turn.reverse()
            pv.clock.start_with_top_timer()
            if game_mode == "stockfish":
                self.player_moves.put('first_move')
        # Indico que hay una partida en curso
        self.status = True

    # Clock settings
    def finish_partide_for_time(self):
        pass

    def pause_clock(self):
        pv.clock.kill_timers()
        if self.game_mode == 'connected':
            # Le decimos al servidor que pause la partida
            pass

    def restart(self):
        pv.panel.restart_movements_viewer()
        pv.clock.restart()
        self.main_player.restart()

        self.status = False
        self.game_mode = None
        self.color_selected = None
        self.clock_status = None
        self.fen = None

        self.fen_historial = []
        self.movement_historial = []
        
        self.stockfish_thread = None

        self.player_turn = ['main_player', 'main_player']
        self.color_turn = [1, 0]

        # Reseteamos a stockfish
        # self.stockfish

    def stop(self):
        pass
        # self.main_player.is_game_over()
        # self.stockfish.stop()

    def get_new_movement(self, movement):
        self.movement_historial.append(movement)
        self.main_player.last_fen()
        self.pass_turn(movement)

    def pass_turn(self, movement):
        if self.clock_status == 'active':
            pv.clock.switch_active_timer()

            # if self.game_mode =='connected':
                # self.connected_player
                # Le decimos al servidor que le diga cambie el reloj activo

        if self.player_turn[0] == 'main_player':
            # pass
            if self.game_mode == 'stockfish':
                self.player_moves.put(movement)
            #elif

        if self.player_turn[0] == 'stockfish':
            self.main_player.recive_movement(movement=movement)

        # elif self.player_turn[0] == 'connected_player':
        #     self.main_player.recive_movement(movement=movement)

        self.player_turn.reverse()


# Connection functions
# ####################################################################

    # def get_new_message(self, message):
    #     print(message)

#     def send_message(self, message):
#         if not self.my_socket:
#             return
#         message = ['message', message]
#         message = " ".join(message)
#         self.my_socket.sendall(message.encode())

#     def player_thread(self, player_socket):

#         # print('se activó un jugador')
#         while True:
#             try:
#                 data = player_socket.recv(1024).decode()
#                 if not data:
#                     continue
#                 print(data, type(data))
#                 for player in self.connected_players:
#                     if player != player_socket:
#                         interaction = data.split()
#                         interaction_type, content = interaction
#                         if interaction_type == 'movement':
#                             self.get_new_movement(content)
#                         elif interaction_type == 'message':
#                             self.get_new_message(content)
#                         elif interaction_type == 'give_me_settings':
#                             command = ['reciv_settings', 'configuración']
#                             command = " ".join(command)
#                             self.my_socket.sendall(command.encode())
#                             print('ya se envió los settings')
#                         elif interaction_type == 'reciv_settings':
#                             print(content)
#             except socket.timeout:
#                 print("Error: Se agotó el tiempo de espera.")
#                 continue
#             except Exception as e:
#                 print(f"Ocurrió un error inesperado en la recepción de la interacción: {e}")
#                 break
#         player_socket.close()
#         self.connected_players.remove(player_socket)
#         # self.finish_connected_partide()

#     def active_server(self): # Ya se crea el server y la escucha de conexiones

#         PUERTO_UDP = 5005
#         PUERTO_TCP = 8000
#         IP_SERVER = '0.0.0.0'

#         def anunciar_servidor():
#             """Hilo que grita la presencia del servidor por UDP."""
#             broadcaster = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#             broadcaster.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
#             print(f"[*] Anunciando servidor en puerto UDP {PUERTO_UDP}...")
            
#             while True:
#                 # El mensaje incluye el puerto TCP donde el servidor está escuchando
#                 mensaje = f"SERVER_ALIVE:{PUERTO_TCP}".encode()
#                 broadcaster.sendto(mensaje, ('255.255.255.255', PUERTO_UDP))
#                 time.sleep(2)

#         # Activamos la escucha del socket en segundo plano
#         def wait_for_players():
#             # Que se mantenga en bucle esperando
#             while len(self.connected_players) < 2:
#                 try:
#                     player_socket, address = self.server_socket.accept()
#                     if address[0] == '127.0.0.1':
#                         print('asi se pone')
#                         self.my_socket = player_socket
#                     self.connected_players.append(player_socket)
#                     print("¡Conexión exitosa!")
#                 except socket.timeout:
#                     print("Error: Se agotó el tiempo de espera.")
#                     continue
#                 except Exception as e:
#                     print(f"Ocurrió un error inesperado en la espera del jugador: {e}")
#                     continue

#                 print(f'[+] Se ha conectado un jugador: {address}')
                
#                 # Iniciamos el hilo de interacciones
#                 thread = threading.Thread(target=self.player_thread, args=(player_socket, ), daemon=True)
#                 thread.start()

#         # Creamos el socket de la partida
#         self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#         self.server_socket.bind((IP_SERVER, PUERTO_TCP))
#         self.server_socket.listen()
#         print('\n[+] El servidor está en escucha de conexiones entrantes...')
#         self.server_socket.settimeout(5)

#         # Activamos la escucha del socket en segundo plano
#         thread = threading.Thread(target=anunciar_servidor, daemon=True)
#         thread.start()

#         # Activamos la escucha del socket en segundo plano
#         thread = threading.Thread(target=wait_for_players, daemon=True)
#         thread.start()

#     def connect_to_server(self, ip_servidor='127.0.0.1', puerto_tcp=8000): # Me parece que esta función esta bien, solo hace falta recibir los datos de partida

        

#         # Espero que el servidor me acepte
#         def awaiting_approval():
#             try:
#                 s.connect((ip_servidor, puerto_tcp))
#                 if not self.server_socket:
#                     command = ['give_me_settings', 'hola']
#                     command = " ".join(command)
#                     s.sendall(command.encode())
#             except socket.timeout:
#                 print("Se agotó el tiempo de espera en la conexión con el servidor.")
#                 s.close()
#                 return
#             except Exception as e:
#                 print(f"Fallo inesperado en la conexión con el servidor: {e}")
#                 s.close()
#                 return

#         # Creo mi socket
#         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         s.settimeout(15)
#         if not self.server_socket:
#             self.my_socket = s
#         # Pido que se haga la conexión con el servidor
#         pv.connection_wait_thread = threading.Thread(target=awaiting_approval, daemon=True)
#         pv.connection_wait_thread.start()

#     def search_and_connect(self):
#         PUERTO_UDP = 5005
#         PUERTO_TCP = 8000
#         ip_servidor = '127.0.0.1'

#         # PASO 1: Descubrimiento UDP
#         buscador = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         buscador.bind(('', PUERTO_UDP))
#         print("[?] Buscando servidor en la red local...")

#         # Recibimos el anuncio del servidor
#         data, addr = buscador.recvfrom(1024)
#         ip_servidor = addr[0]
#         puerto_tcp = int(data.decode().split(":")[1])
#         print(f"[!] Servidor encontrado en {ip_servidor}:{puerto_tcp}")
#         buscador.close()

#         self.connect_to_server(ip_servidor, puerto_tcp)

#     def finish_connected_partide(self):
#         self.server_socket.close()

# #############################################################################
