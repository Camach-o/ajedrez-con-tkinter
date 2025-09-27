# Aplicación

TITLE = "Ajedrez"
menu_options = ["Partida", "Dificultad", "Reloj", "Emparejamiento", "Estilo", "Créditos"]
board = None
clock = None
panel = None
clock_frame = None

# Tablero



# Partida

ongoing_game = 0

# Colores de fondo

OSCURO_SUAVE = "#1f1f1f"
OSCURO_FUERTE = "#191918"

# Tabla de movimientos

# IMG_ATRAS = ImageTk.PhotoImage(Image.open("contenido_grafico/imagenes_panel/atras.png"))
# IMG_ADELANTE = ImageTk.PhotoImage(Image.open("contenido_grafico/imagenes_panel/adelante.png"))
# IMG_RESETEAR = ImageTk.PhotoImage(Image.open("contenido_grafico/imagenes_panel/retroceder.png"))

# Menús 

FUENTE_MENU = ("Arial", 14)
FUENTE_BOTONES_MENU = ("Calibri Bold", 14)
COLOR_BOTON_MENU = "#A6A6A6"

# Tema

white_theme = "#bb935b"
black_theme = "#592f0a"

# Clock

clock_status = 1       # 1.- Active | 0.- Disable
clock_type = 1         # 1.- Manual | 0.- Automatic
clock_time = 5         # 5 preset time
clock_bonus = 0        # 0 preset bonus
