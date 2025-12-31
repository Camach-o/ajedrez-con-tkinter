# Aplicación
TITLE = "Ajedrez"
menu_options = ["Partida", "Dificultad", "Estilo", "Créditos"] # , "Emparejamiento"

OSCURO_SUAVE = "#1f1f1f"
OSCURO_FUERTE = "#191918"
TEMA_PREDETERMINADO_TABLERO = ("#bb935b", "#592f0a") # Blanco | Negro

FUENTE_MENU = ("Arial", 14)
FUENTE_BOTONES_MENU = ("Calibri Bold", 14)
COLOR_BOTON_MENU = "#A6A6A6"

height_windows = None
width_windows = None

# Objetos
board = None
clock = None
panel = None
clock_frame = None
game = None
menubar = None
partida = None
player = None
window = None




# Partida
promotion_menu_status = False

startposition = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

ongoing_game = 0

connection_wait_thread = 0

# Colores de fondo
# Menús


# Tema

white_theme = "#bb935b"
black_theme = "#592f0a"

# Clock

clock_status = 1       # 1.- Active | 0.- Disable
clock_default_minutes = 5         # 5 preset time
clock_default_bonus = 0        # 0 preset bonus
