import time
import socket
import threading
import components.alert as alert
import components.project_vars as pv

PUERTO_UDP = 5005
PUERTO_TCP = 8000
IP_SERVER = '0.0.0.0'

class Server():
    def __init__(self):
        self.connected_players = []
        self.server_socket = None
        self.my_socket = None
        self.broadcaster = None

    def announce_server(self):
        """ Active and announce UDP server."""
        self.broadcaster = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.broadcaster.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        print(f"[*] Anunciando servidor en puerto UDP {PUERTO_UDP}...")

        while self.broadcaster:
            mensaje = f"SERVER_ALIVE:{PUERTO_TCP}".encode()
            self.broadcaster.sendto(mensaje, ('255.255.255.255', PUERTO_UDP))
            time.sleep(2)

    def receive_data(self, player_socket, task):
        """ Receive the data from the server to give it to the player."""
        while True:
            try:
                data = player_socket.recv(1024).decode()
                if not data:
                    break
                task(data)
            except socket.timeout:
                print("RData. Se agotó el tiempo de espera.")
                continue
            except Exception as e:
                print(f"RData. Ha ocurrido un error en la recepción de los datos: {e}")
                break
        self.finish_connection()

    def player_thread(self, player_socket, players):
        """ Stay tuned for """
        while True:
            try:
                data = player_socket.recv(1024).decode()
                if not data:
                    break
                for player in players:
                    if player is not player_socket:
                        player.sendall(f"{data}".encode())
            except socket.timeout:
                print("PThread. Se agotó el tiempo de espera.")
                continue
            except Exception as e:
                print(f"PThread. Ha ocurrido un error en la recepción de los datos: {e}")
                break
        player_socket.close()
        players.remove(player_socket)
        self.finish_connection()

    def wait_for_players(self, server_socket):
        """ Wait for the players connection."""
        players_count = 0
        while players_count < 2:
            try:
                player_socket, address = server_socket.accept()
                players_count += 1
                self.connected_players.append(player_socket)
                print("¡Conexión exitosa!")
            except socket.timeout:
                print("WFPlayers. Se agotó el tiempo de espera.")
                continue
            except Exception as e:
                print(f"Ha ocurrido un error en la espera del jugador: {e}")
                return
            print(f'[+] Se ha conectado un jugador: {address}')
            interaction_thread = threading.Thread(target=self.player_thread,
                                                  args=(player_socket,
                                                  self.connected_players),
                                                  daemon=True)
            interaction_thread.start()
        pv.is_there_a_connected_player = True
        pv.dont_touch = False

    def active_server(self):
        """ Active the UDP and TCP connections."""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((IP_SERVER, PUERTO_TCP))
        server_socket.settimeout(5)
        server_socket.listen()
        self.server_socket = server_socket
        print('\n[+] El servidor está en escucha de conexiones entrantes...')

        announce_server_thread = threading.Thread(target=self.announce_server, daemon=True)
        announce_server_thread.start()

        wait_for_players_thread = threading.Thread(target=self.wait_for_players, args=(server_socket,), daemon=True)
        wait_for_players_thread.start()

    def search_and_connect(self):
        """ Search an UDP server to next connect with de TCP server."""
        try:
            finder = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            finder.settimeout(5)
            finder.bind(('', PUERTO_UDP))
            print("[?] Buscando servidor en la red local...")

            data, addr = finder.recvfrom(1024)
            server_ip = addr[0]
            tcp_port = int(data.decode().split(":")[1])
            print(f"[!] Servidor encontrado en {server_ip}:{tcp_port}")
            finder.close()
        except socket.timeout:
            print("SAConnect. Se agotó el tiempo de espera.")
            return None

        return self.connect_to_server(type_connection="guest",
                                      server_ip=server_ip, tcp_port=tcp_port)

    def awaiting_approval(self, sockect_ap, server_ip, tcp_port):
        """ Wait for the connection to the server to be approved."""
        try:
            sockect_ap.connect((server_ip, tcp_port))
        except socket.timeout:
            print("AAprroval. Se agotó el tiempo de espera.")
            sockect_ap.close()
        except Exception as e:
            print(f"AApproval. Falló la conexión con el servidor: {e}")
            sockect_ap.close()

    def connect_to_server(self, type_connection, server_ip=None, tcp_port=None):
        """ To connect with the server."""
        if type_connection == "host":
            server_ip='127.0.0.1'
            tcp_port=8000

        connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection_socket.settimeout(15)

        connection_wait_thread = threading.Thread(target=self.awaiting_approval,
                                                  args=(connection_socket, server_ip, tcp_port),
                                                  daemon=True)
        connection_wait_thread.start()
        self.my_socket = connection_socket
        return connection_socket

    def finish_connection(self):
        """ Close the server."""
        if not pv.there_is_an_active_server:
            return
        pv.there_is_an_active_server = False
        if self.connected_players:
            for player_socket in self.connected_players:
                if player_socket:
                    player_socket.close()

        if self.server_socket:
            self.server_socket.close()

        if self.broadcaster:
            self.broadcaster.close()

        if self.my_socket:
            self.my_socket.close()

        self.connected_players = []
        self.server_socket = None
        self.my_socket = None
        self.broadcaster = None
        pv.clock.kill_timers()
        pv.is_there_a_connected_player = False
        pv.ongoing_game = False
        pv.dont_touch = True

        alert.show_info(tittle="Partida finalizada.", message="La conexión LAN se ha cerrado.")
