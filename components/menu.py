import tkinter as tk
from webbrowser import open_new_tab
from PIL import Image, ImageTk
import stockfish
import components.alert as alert
import components.project_vars as pv
from components.pieces import IMG_WHITE_QUEEN, IMG_WHITE_ROOK, IMG_WHITE_BISHOP, IMG_WHITE_KNIGHT, IMG_BLACK_QUEEN, IMG_BLACK_ROOK, IMG_BLACK_BISHOP, IMG_BLACK_KNIGHT

FUENTE_BOTONES_MENU = ("Calibri Bold", 14)

# Menu options
class PartideMenu():
    def __init__(self, frame):
        self.frame = frame
        self.partideopts_frame = None
        self.clockopts_frame = None
        self.fen_frame = None

        self.game_mode = None
        self.color_selected = None
        self.clock_status = None

        self.labels = {}
        self.radiobuttons = {}

        self.time_entry = None
        self.bonus_entry = None

        self.fen_entry = None
        self.startpos = None

    def init_widgets(self):
        self.game_mode = tk.StringVar()
        self.game_mode.set(1)
        self.color_selected = tk.StringVar()
        self.color_selected.set(1)
        self.clock_status = tk.StringVar()
        self.clock_status.set(1)

        # Frames
        self.partideopts_frame = tk.Frame(self.frame, width=400, height=205, bg="#1f1f1f")
        self.clockopts_frame = tk.Frame(self.frame, width=400, height=175, bg="#1f1f1f")
        self.fen_frame = tk.Frame(self.frame, width=400, height=180, bg="#1f1f1f")

        # Label settings
        args_label = ([self.partideopts_frame, "Partida", 18],
                      [self.partideopts_frame, "Opciones de la partida", 15],
                      [self.clockopts_frame, "Opciones del reloj", 15],
                      [self.clockopts_frame, "Tiempo", 14],
                      [self.clockopts_frame, "Bonus", 14],
                      [self.fen_frame, "Configuración del FEN", 15])
        for args in args_label:
            label = tk.Label(args[0], text=args[1])
            label.configure(bg="#1f1f1f", font=("Calibri Bold", args[2]), fg="white")
            self.labels[args[1]] = label

        # Radiobutton settings
        args_radiobutton = ([self.partideopts_frame, "Jugar Solo", self.game_mode, 1],
                            [self.partideopts_frame, "Jugar contra Stockfish", self.game_mode, 2],
                            [self.partideopts_frame, "Jugar partida LAN (activar servidor)", self.game_mode, 3],
                            [self.partideopts_frame, "Jugar con Blancas", self.color_selected, 1],
                            [self.partideopts_frame, "Jugar con Negras", self.color_selected, 2],
                            [self.clockopts_frame, "Jugar con Reloj", self.clock_status, 1],
                            [self.clockopts_frame, "Jugar sin Reloj", self.clock_status, 2])
        for args in args_radiobutton:
            radiobutton = tk.Radiobutton(args[0], text=args[1], variable=args[2], value=args[3])
            radiobutton.configure(bg=pv.GRAY, activebackground=pv.GRAY)
            radiobutton.configure(fg="white", font=("Calibri Bold", 14), activeforeground="white")
            radiobutton.configure(selectcolor=pv.GRAY)
            self.radiobuttons[args[1]] = radiobutton

        # Time and Increment section
        def validate_entry(text):
            return text == "" or (text.isdigit() and len(text) <= 2)
        vcmd = (self.clockopts_frame.register(validate_entry), "%P")

        def create_time_entry(value_to_insert):
            entry = tk.Entry(self.clockopts_frame, width=20, cursor="arrow", relief="raised", bd=1)
            entry.configure(bg="#A6A6A6", validate="key", validatecommand=vcmd)
            entry.insert(0, value_to_insert)
            entry.pack_propagate(False)
            return entry

        self.time_entry = create_time_entry(pv.clock_default_minutes)
        self.bonus_entry = create_time_entry(pv.clock_default_bonus)

        # Fen section
        def set_fen():
            self.fen_entry.delete(0, tk.END)
            self.fen_entry.insert(0, pv.startposition)

        self.fen_entry = tk.Entry(self.fen_frame, width=36, bg="#A6A6A6")
        self.fen_entry.configure(font=FUENTE_BOTONES_MENU)

        self.startpos = tk.Button(self.fen_frame, width=13, text="Posición Inicial", bg="#A6A6A6")
        self.startpos.configure(font=FUENTE_BOTONES_MENU, activebackground="#A6A6A6", command=set_fen)
        set_fen()

    def save(self):
        if self.game_mode.get() == "1":
            game_mode = "only"
        if self.game_mode.get() == "2":
            game_mode = "stockfish"
        if self.game_mode.get() == "3":
            game_mode = "connected"

        if self.color_selected.get() == "1":
            color_selected = "white"
        if self.color_selected.get() == "2":
            color_selected = "black"

        if self.clock_status.get() == "1":
            clock_status = "active"
        if self.clock_status.get() == "2":
            clock_status = "desactive"

        time = int(self.time_entry.get())
        bonus = int(self.bonus_entry.get())
        fen = self.fen_entry.get()

        if not time in range(1, 61) or not bonus in range(0, 61):
            alert.show_info(tittle="Parámetro Invalido",
                            message="Configuración de tiempo no valida.")
            return False

        if not stockfish.Stockfish._is_fen_syntax_valid(fen=fen):
            alert.show_info(tittle="Parámetro Invalido",
                            message="El FEN elegido no es un FEN valido.")
            return False


        pv.partide.restart()
        if game_mode == "connected":
            pv.partide.start_connected_partide(type_connection="host",
                                               partide_settings=[game_mode,
                                                                 color_selected,
                                                                 clock_status, time,
                                                                 bonus,
                                                                 fen])
            return True

        pv.partide.start_partide(game_mode, color_selected, clock_status, time, bonus, fen)
        return True

    def show(self):
        self.partideopts_frame.grid(row=0, column=0)
        self.clockopts_frame.grid(row=1, column=0)
        self.fen_frame.grid(row=2, column=0)

        self.labels["Partida"].place(x=15, y=15)
        self.labels["Opciones de la partida"].place(x=15, y=55)
        self.labels["Opciones del reloj"].place(x=15, y=15)
        self.labels["Tiempo"].place(x=35, y=105)
        self.labels["Bonus"].place(x=35, y=145)
        self.labels["Configuración del FEN"].place(x=15, y=15)

        self.radiobuttons["Jugar Solo"].place(x=35, y=95)
        self.radiobuttons["Jugar contra Stockfish"].place(x=170, y=95)
        self.radiobuttons["Jugar partida LAN (activar servidor)"].place(x=35, y=130)
        self.radiobuttons["Jugar con Blancas"].place(x=35, y=170)
        self.radiobuttons["Jugar con Negras"].place(x=220, y=170)
        self.radiobuttons["Jugar con Reloj"].place(x=35, y=55)
        self.radiobuttons["Jugar sin Reloj"].place(x=220, y=55)

        self.time_entry.place(x=130, y=110)
        self.bonus_entry.place(x=130, y=150)
        self.fen_entry.place(x=15, y=60)
        self.startpos.place(x=15, y=105)

    def hide(self):
        self.partideopts_frame.grid_forget()
        self.clockopts_frame.grid_forget()
        self.fen_frame.grid_forget()

        self.labels["Partida"].place_forget()
        self.labels["Opciones de la partida"].place_forget()
        self.labels["Opciones del reloj"].place_forget()
        self.labels["Tiempo"].place_forget()
        self.labels["Bonus"].place_forget()
        self.labels["Configuración del FEN"].place_forget()

        self.radiobuttons["Jugar Solo"].place_forget()
        self.radiobuttons["Jugar contra Stockfish"].place_forget()
        self.radiobuttons["Jugar partida LAN (activar servidor)"].place_forget()
        self.radiobuttons["Jugar con Blancas"].place_forget()
        self.radiobuttons["Jugar con Negras"].place_forget()
        self.radiobuttons["Jugar con Reloj"].place_forget()
        self.radiobuttons["Jugar sin Reloj"].place_forget()

        self.time_entry.place_forget()
        self.bonus_entry.place_forget()
        self.fen_entry.place_forget()
        self.startpos.place_forget()

class DifficultyMenu():
    def __init__(self, frame):
        self.frame = frame
        self.menu_tittle = None
        self.difficulty_options = {}
        self.selected_difficulty = None

    def init_widgets(self):
        self.menu_tittle = tk.Label(self.frame,
                                    text="Elige un ELO para cambiar la difícultad para Stockfish.")
        self.menu_tittle.configure(bg="#1f1f1f", font=("Calibri Bold", 18), fg="white")

        self.selected_difficulty = tk.StringVar()
        self.selected_difficulty.set(2)

        radiobutton_args = [{'var_name':"very_easy", 'text':"Muy Fácil (800)"},
                            {'var_name':"easy", 'text':"Fácil (1100)"},
                            {'var_name':"intermediate", 'text':"Intermedio (1400)"},
                            {'var_name':"avanced", 'text':"Avanzado (1700)"},
                            {'var_name':"hard", 'text':"Difícil (2000)"},
                            {'var_name':"very_hard", 'text':"Muy Difícil (2300)"}]
        for n_value, args in enumerate(radiobutton_args):
            radiobutton = tk.Radiobutton(self.frame, selectcolor=pv.GRAY,
                                        foreground="white", activeforeground="white",
                                        variable=self.selected_difficulty, value=n_value,
                                        bg=pv.GRAY, activebackground=pv.GRAY,
                                        text=args.get('text'), font=("Calibri Bold", 14))
            self.difficulty_options[args.get('var_name')] = radiobutton

    def save(self):
        pv.partide.set_stockfish_difficulty(int(self.selected_difficulty.get()))
        return True

    def show(self):
        self.menu_tittle.grid(row=0, column=0, columnspan=3)
        self.difficulty_options['very_easy'].grid(row=1, column=0)
        self.difficulty_options['easy'].grid(row=1, column=1)
        self.difficulty_options['intermediate'].grid(row=1, column=2)
        self.difficulty_options['avanced'].grid(row=2, column=0)
        self.difficulty_options['hard'].grid(row=2, column=1)
        self.difficulty_options['very_hard'].grid(row=2, column=2)

        rows, cols = 4, 3
        for r in range(rows):
            self.frame.grid_rowconfigure(r, weight=1)
        for c in range(cols):
            self.frame.grid_columnconfigure(c, weight=1)

    def hide(self):
        self.menu_tittle.grid_forget()
        self.difficulty_options['very_easy'].grid_forget()
        self.difficulty_options['easy'].grid_forget()
        self.difficulty_options['intermediate'].grid_forget()
        self.difficulty_options['avanced'].grid_forget()
        self.difficulty_options['hard'].grid_forget()
        self.difficulty_options['very_hard'].grid_forget()

        rows, cols = 4, 3
        for r in range(rows):
            self.frame.grid_rowconfigure(r, weight=0)
        for c in range(cols):
            self.frame.grid_columnconfigure(c, weight=0)

class MatchMenu(): # Falta por hacer
    def __init__(self, frame, top_level_menu):
        self.frame = frame
        self.connected_tittle = None
        self.no_connected_tittle = None
        self.top_level_menu = top_level_menu

    def init_widgets(self):
        # Connected player
        self.connected_tittle = tk.Label(self.frame, text="Desconectarse de la Partida.")
        self.connected_tittle.configure(bg=pv.GRAY, font=("Calibri Bold", 20), fg="white")
        self.disconnet_button = tk.Button(self.frame, command=self.disconnect)
        self.disconnet_button.configure(text="DESCONECTARME", font=FUENTE_BOTONES_MENU,
                                        activebackground="#A6A6A6", width=18, bg="#A6A6A6")

        # No connected player
        self.no_connected_tittle = tk.Label(self.frame, text="No estás conectado con ninguna partida LAN.\n" \
                                            "¡ADVERTENCIA!\n" \
                                            "Buscar una partida LAN detendrá la partida actual.")
        self.no_connected_tittle.configure(bg=pv.GRAY, font=("Calibri Bold", 18), fg="white")
        self.no_connected_button = tk.Button(self.frame, command=self.save)
        self.no_connected_button.configure(text="BUSCAR Y CONECTARME", font=FUENTE_BOTONES_MENU,
                                           activebackground="#A6A6A6", width=22, bg="#A6A6A6")

    def save(self):
        if pv.connection_wait_thread and pv.connection_wait_thread.is_alive():
            return
        pv.partide.restart()
        pv.partide.start_connected_partide(type_connection="guest")
        return True

    def disconnect(self):
        if pv.partide:
            self.top_level_menu.close_menu()
            pv.partide.finish_connected_partide()

    def show(self, type_menu="no_connected_player"):
        if type_menu == "connected_player":
            self.connected_tittle.grid(row=0, column=0)
            self.disconnet_button.grid(row=1, column=0, sticky="n")
        elif type_menu == "no_connected_player":
            self.no_connected_tittle.grid(row=0, column=0)
            self.no_connected_button.grid(row=1, column=0, sticky="n")

        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

    def hide(self):
        self.connected_tittle.grid_forget()
        self.disconnet_button.grid_forget()
        self.no_connected_tittle.grid_forget()
        self.no_connected_button.grid_forget()

        self.frame.grid_rowconfigure(0, weight=0)
        self.frame.grid_rowconfigure(1, weight=0)
        self.frame.grid_columnconfigure(0, weight=0)

class StyleMenu():
    def __init__(self, frame):
        self.frame = frame
        self.labels = {}
        self.entrys = {}

        self.check_color = None
        self.color_view = None
        self.square_list = None

    def init_widgets(self):
        for args in (["Casillas Blancas", "white", pv.DEFAULT_BOARD_WHITE_THEME], ["Casillas Negras", "black", pv.DEFAULT_BOARD_BLACK_THEME]):
            label = tk.Label(self.frame, text=args[0], fg="white")
            label.configure(font=("Calibri Bold", 18), bg=pv.GRAY)
            entry = tk.Entry(self.frame, width=12, bg="#A6A6A6")
            entry.configure(font=("Calibri Bold", 12), fg=args[1], relief="raised", bd=2)
            entry.insert(0, args[2].upper())

            self.labels[args[1]] = label
            self.entrys[args[1]] = entry

        # Color display
        self.check_color = tk.Button(self.frame, width=10, text="<PROBAR>", font=("Calibri Bold", 10))
        self.check_color.configure(bg="#A6A6A6", command=self._update_color)
        self.square_list = []

        # Color Viewer
        self.color_view = tk.Frame(self.frame, bd=3, relief="solid")
        for row in range(2):
            for column in range(2):
                square = tk.Frame(self.color_view, width=70, height=70)
                square.grid(column=column, row=row)
                self.square_list.append(square)
        self._update_color()

    def _update_color(self):
        try:
            if not self.entrys["white"].get() or not self.entrys["black"].get():
                raise Exception
            if self.entrys["white"].get() == self.entrys["black"].get():
                raise Exception
            color = [self.entrys["white"].get(), self.entrys["black"].get()]
            for loop, square in enumerate(self.square_list):
                square.configure(bg=color[0])
                if loop == 1:
                    continue
                color.reverse()
        except:
            alert.show_info(tittle="HUBO UN ERROR", message="La configuración seleccionada no puede ser aplicada.")
            return False
        return True

    def save(self):
        if self._update_color():
            pv.DEFAULT_BOARD_WHITE_THEME = self.entrys["white"].get().upper()
            pv.DEFAULT_BOARD_BLACK_THEME = self.entrys["black"].get().upper()
            pv.board.set_theme(pv.DEFAULT_BOARD_WHITE_THEME, pv.DEFAULT_BOARD_BLACK_THEME)
            return True
        return False

    def show(self):
        self.labels["white"].place(x=50, rely=0.22)
        self.entrys["white"].place(relx=0.42, rely=0.25)
        self.labels["black"].place(x=50, rely=0.52)
        self.entrys["black"].place(relx=0.42, rely=0.54)
        self.color_view.place(relx=0.80, rely=0.42, anchor="center")
        self.check_color.place(relx=0.44, rely=0.78)

    def hide(self):
        self.entrys["white"].delete(0, tk.END)
        self.entrys["white"].insert(0, pv.DEFAULT_BOARD_WHITE_THEME)
        self.entrys["black"].delete(0, tk.END)
        self.entrys["black"].insert(0, pv.DEFAULT_BOARD_BLACK_THEME)
        self.frame.focus_set()
        self.labels["white"].place_forget()
        self.entrys["white"].place_forget()
        self.labels["black"].place_forget()
        self.entrys["black"].place_forget()
        self.color_view.place_forget()
        self.check_color.place_forget()

class CreditsMenu():
    def __init__(self, frame):
        self.frame = frame
        self.thanks = None
        self.github_link = None
        self.link = "https://github.com/Camach-o"
        self.text = "Hola, un placer, soy Camacho. \n\n" \
        "De ante mano gracias por haber descargado este juego,\n" \
        "para mí es grato poder compartirlo, se trata de mi\n" \
        "primer gran proyecto, espero pases un buen rato usandolo.\n" \
        "Si deseas ver otro de mis proyectos dale un vistazo a mi GitHub:\n\n"

    def init_widgets(self):
        self.thanks = tk.Label(self.frame, text=self.text, justify='center', fg="white")
        self.thanks.configure(font=("Calibri Bold", 14), bg=pv.GRAY)

        self.github_link = tk.Button(self.frame, text=self.link, fg="white", bd=0)
        self.github_link.configure(font=("Calibri Bold", 14), bg=pv.GRAY)
        self.github_link.configure(activeforeground="white", activebackground=pv.GRAY)
        self.github_link.configure(command=self.open_github_link)

    def open_github_link(self):
        open_new_tab("https://github.com/Camach-o")

    def show(self):
        self.thanks.place(x=45, y=30)
        self.github_link.place(x=175, y=185)

    def hide(self):
        self.thanks.place_forget()
        self.github_link.place_forget()

# No menu option
class PromotionMenu():
    def __init__(self, frame, top_level_menu):
        self.frame = frame
        self.top_level_menu = top_level_menu
        self.options = []
        self.white_images = None
        self.black_images = None
        self.active = False
        self.piece_to_promote_info = {}

    def init_widgets(self):
        piece_types = ('Q', 'R', 'B', 'N')

        for ptype in piece_types:
            piece_option = tk.Label(self.frame, text=ptype, width=80, height=80, bd=3)
            piece_option.configure(bg=pv.DEFAULT_BOARD_WHITE_THEME, fg="white", relief="solid")
            piece_option.bind("<Button-1>", self.define_promotion)
            self.options.append(piece_option)

        self.white_images = [
            IMG_WHITE_QUEEN,
            IMG_WHITE_ROOK,
            IMG_WHITE_BISHOP,
            IMG_WHITE_KNIGHT]

        self.black_images = [
            IMG_BLACK_QUEEN,
            IMG_BLACK_ROOK,
            IMG_BLACK_BISHOP,
            IMG_BLACK_KNIGHT]

        for path in (self.white_images, self.black_images):
            for i, img in enumerate(path):
                path[i] = ImageTk.PhotoImage(Image.open(img))

    def show(self, color="white"):
        for i, img in enumerate(self.white_images if color == "white" else self.black_images):
            self.options[i].configure(image=img)
            self.options[i].grid(row=0, column=i, padx=15)

        self.frame.grid_rowconfigure(0, weight=1)
        for c in range(4):
            self.frame.grid_columnconfigure(c, weight=1)
        self.active = True

    def hide(self):
        for label in self.options:
            label.grid_forget()
        self.frame.place_forget()
        self.active = False

        self.frame.grid_rowconfigure(0, weight=0)
        for c in range(4):
            self.frame.grid_columnconfigure(c, weight=0)

    def define_promotion(self, event):
        promotion = event.widget.configure().get("text")[-1]
        self.top_level_menu.close_promotion_menu()
        pv.partide.main_player.promotion_selected.set(promotion)

# Custom Component
class MenuButton(tk.Button):
    def __init__(self, master, **kwargs):
        super().__init__(master, width=10, bg="#A6A6A6", **kwargs)
        self.configure(font=FUENTE_BOTONES_MENU, activebackground="#A6A6A6")

class Menu():
    def __init__(self, root):
        self.root = root
        self.menu_frame = None
        self.selected_menu = None

        self.top_frame = None
        self.bottom_frame = None
        self.button_close = None
        self.button_save = None

        self._init_menu()

    def _init_menu(self):
        self.menu_frame = tk.Frame(self.root, bd="2", bg=pv.GRAY, relief="solid")
        self.top_frame = tk.Frame(self.menu_frame, bg=pv.GRAY)
        self.bottom_frame = tk.Frame(self.menu_frame, bg=pv.GRAY)
        self.top_frame.grid(row=0, column=0)
        self.bottom_frame.grid(row=1, column=0)

        self.button_save = MenuButton(self.bottom_frame, text="Guardar", command=self.save_configuration)
        self.button_close = MenuButton(self.bottom_frame, text="Cerrar", command=self.close_menu)

        self.partide_menu = PartideMenu(self.top_frame)
        self.partide_menu.init_widgets()
        self.style_menu = StyleMenu(self.top_frame)
        self.style_menu.init_widgets()
        self.credits_menu = CreditsMenu(self.top_frame)
        self.credits_menu.init_widgets()
        self.difficulty_menu = DifficultyMenu(self.top_frame)
        self.difficulty_menu.init_widgets()
        self.match_menu = MatchMenu(self.top_frame, self)
        self.match_menu.init_widgets()
        self.promotion_menu = PromotionMenu(self.top_frame, self)
        self.promotion_menu.init_widgets()

    def _place_menu(self):
        """ Calculate the coordinates where the menu will be placed and place it."""
        self.menu_frame.update()
        height_menu = self.menu_frame.winfo_height()
        width_menu = self.menu_frame.winfo_width()
        y = (pv.height_windows / 2) - (height_menu / 2)
        x = (pv.width_windows / 2) - (width_menu / 2)
        self.menu_frame.place(y=y, x=x)

    def _show_buttons(self, txt_save_button="Guardar", only_close=False):
        """ Packs the buttons of the main menu.

            Args:
                - txt_save_button (str): text to set in the save button (it can change).
                - only_close (bool): determine if the cancel button is display or are display both.
        """
        self.button_save.pack(side="left", padx=(0, 80), pady=(0, 5))
        self.button_close.pack(side="right", padx=(80, 0), pady=(0, 5))
        self.button_save.configure(text=txt_save_button)

        if only_close:
            self.button_save.pack_forget()
            self.button_close.pack_forget()
            self.button_close.pack(pady=(0, 5))

    def show_promotion_menu(self, color="white"):
        """ Display the promotion menu.
        
            Args:
                - color (str): is the color of the player who is promoted.
        """
        self.menu_frame.place(y=50, x=200)
        if self.selected_menu:
            self.close_menu()

        self.bottom_frame.grid_forget()
        self.button_close.pack_forget()

        self.top_frame.configure(width=460, height=115)
        self.top_frame.grid_propagate(False)

        self.selected_menu = self.promotion_menu
        self.selected_menu.show(color=color)

        self._place_menu()

        self.promotion_menu.active = True

    def close_promotion_menu(self):
        self.bottom_frame.grid(row=1, column=0)
        self.close_menu()

    def show_menu(self, option): 
        """ Displays the menu and widgets for the selected option.

            Arg:
                - option (event): widget that called the function.
        """
        if self.promotion_menu.active:
            return

        if self.selected_menu:
            self.close_menu()

        self.menu_frame.place(y=50, x=200)
        option_called = option.widget.configure().get("text")[-1]

        if option_called in pv.menu_options:
            if option_called == "Partida":
                self.selected_menu = self.partide_menu
                self._show_buttons(txt_save_button="Iniciar")
            elif option_called == "Dificultad":
                self.selected_menu = self.difficulty_menu
                self.top_frame.configure(width=600, height=250)
                self.top_frame.grid_propagate(False)
                self._show_buttons(txt_save_button="Guardar")
            elif option_called == "Emparejamiento":
                self.selected_menu = self.match_menu
                self.top_frame.configure(width=600, height=200)
                self.top_frame.grid_propagate(False)
                self._show_buttons(only_close=True)
                if pv.there_is_an_active_server:
                    self.selected_menu.show(type_menu="connected_player")
                else:
                    self.selected_menu.show(type_menu="no_connected_player")
                self._place_menu()
                return
            elif option_called == "Estilo":
                self.selected_menu = self.style_menu
                self.top_frame.configure(width=600, height=250)
                self._show_buttons(txt_save_button="Guardar")
            elif option_called == "Créditos":
                self.selected_menu = self.credits_menu
                self.top_frame.configure(width=600, height=250)
                self._show_buttons(only_close=True)

        self.selected_menu.show()
        self._place_menu()

    def save_configuration(self):
        """ Save the new settings for the selected option and update the game."""
        if self.selected_menu:
            if self.selected_menu.save():
                self.close_menu()

    def close_menu(self):
        self.selected_menu.hide()
        self.selected_menu = None
        self.top_frame.grid_propagate(True)
        self.button_save.pack_forget()
        self.button_close.pack_forget()
        self.menu_frame.place_forget()
