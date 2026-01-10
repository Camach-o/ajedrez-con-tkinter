# App
APP_TITTLE = 'Ajedrez'
# App colors
GRAY = "#1f1f1f"
DARK_GRAY = "#191918"
DEFAULT_BOARD_WHITE_THEME = "#bb935b"
DEFAULT_BOARD_BLACK_THEME = "#592f0a"

menu_options = ["Partida", "Dificultad", "Emparejamiento", "Estilo", "Créditos"]
height_windows = None
width_windows = None

# App Objects
window = None
clock = None
board = None
panel = None
menu = None
partide = None
player = None

startposition = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

# Partide vars
ongoing_game = False
dont_touch = False
is_there_a_connected_player = False
there_is_an_active_server = False
connection_wait_thread = 0

# Clock vars
clock_status = 1                   # 1.- Active | 0.- Disable
clock_default_minutes = 5          # 5 default time
clock_default_bonus = 0            # 0 default bonus
