import tkinter as tk
# from pathlib import Path
from tkinter import messagebox
import components.project_vars as pv
from webbrowser import open_new_tab
from PIL import Image, ImageTk
from components.pieces import IMG_WHITE_QUEEN, IMG_WHITE_ROOK, IMG_WHITE_BISHOP, IMG_WHITE_KNIGHT, IMG_BLACK_QUEEN, IMG_BLACK_ROOK, IMG_BLACK_BISHOP, IMG_BLACK_KNIGHT

# Custom Components
class MenuButton(tk.Button):
    def __init__(self, master, **kwargs):
        super().__init__(master, width=10, bg="#A6A6A6", **kwargs)
        self.configure(font=pv.FUENTE_BOTONES_MENU, activebackground="#A6A6A6")

# Menu options widgets
class PartideMenu(): # Falta por hacer
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
            radiobutton.configure(bg=pv.OSCURO_SUAVE, activebackground=pv.OSCURO_SUAVE)      
            radiobutton.configure(fg="white", font=("Calibri Bold", 14), activeforeground="white")
            radiobutton.configure(selectcolor=pv.OSCURO_SUAVE)
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
        self.fen_entry.configure(font=pv.FUENTE_BOTONES_MENU)

        self.startpos = tk.Button(self.fen_frame, width=13, text="Posición Inicial", bg="#A6A6A6")
        self.startpos.configure(font=pv.FUENTE_BOTONES_MENU, activebackground="#A6A6A6", command=set_fen)
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
            messagebox.showinfo("Información", "Configuración de tiempo no valida")
            return False
        
        if game_mode == "connected":
            messagebox.showinfo("Información", "Por los momentos las partidas vía LAN no están activas")
            return False

        pv.partida.start_partide(game_mode, color_selected, clock_status, time, bonus, fen)
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

class DifficultyMenu(): # Falta por hacer
    def __init__(self, frame):
        self.frame = frame
        self.difficulty_tittle = None
        self.radiobutton_options = {}
        self.selected_option = None

    def init_widgets(self):

        self.selected_option = tk.StringVar()
        self.selected_option.set(2)

        self.difficulty_tittle = tk.Label(self.frame, text="Elige una difícultad para Stockfish.")
        self.difficulty_tittle.configure(bg="#1f1f1f", font=("Calibri Bold", 18), fg="white")

        arg_radiobuttons = [{'var_name': "very_easy", 'text': "Muy Fácil"},
                            {'var_name': "easy", 'text': "Fácil"},
                            {'var_name': "intermediate", 'text': "Intermedio"},
                            {'var_name': "avanced", 'text': "Avanzado"},
                            {'var_name': "hard", 'text': "Difícil"},
                            {'var_name': "very_hard", 'text': "Muy Difícil"}]
        for n_value, args in enumerate(arg_radiobuttons):
            radiobutton = tk.Radiobutton(self.frame, text=args.get('text'), 
                                         variable=self.selected_option, value=n_value)
            radiobutton.configure(bg=pv.OSCURO_SUAVE, activebackground=pv.OSCURO_SUAVE)      
            radiobutton.configure(fg="white", font=("Calibri Bold", 14), activeforeground="white")
            radiobutton.configure(selectcolor=pv.OSCURO_SUAVE)
            self.radiobutton_options[args.get('var_name')] = radiobutton

    def save(self):
        pv.partida.set_stockfish_difficulty(self.selected_option.get())
        return True

    def show(self):
        self.radiobutton_options['very_easy'].grid(row=1, column=0)
        self.radiobutton_options['easy'].grid(row=1, column=1)
        self.radiobutton_options['intermediate'].grid(row=1, column=2)
        self.radiobutton_options['avanced'].grid(row=2, column=0)
        self.radiobutton_options['hard'].grid(row=2, column=1)
        self.radiobutton_options['very_hard'].grid(row=2, column=2)
        self.difficulty_tittle.grid(row=0, column=0, columnspan=3)

        rows, cols = 4, 3
        for r in range(rows):
            self.frame.grid_rowconfigure(r, weight=1)
        for c in range(cols):
            self.frame.grid_columnconfigure(c, weight=1)

    def hide(self):
        self.radiobutton_options['very_easy'].grid_forget()
        self.radiobutton_options['easy'].grid_forget()
        self.radiobutton_options['intermediate'].grid_forget()
        self.radiobutton_options['avanced'].grid_forget()
        self.radiobutton_options['hard'].grid_forget()
        self.radiobutton_options['very_hard'].grid_forget()
        self.difficulty_tittle.grid_forget()

        rows, cols = 4, 3
        for r in range(rows):
            self.frame.grid_rowconfigure(r, weight=0)
        for c in range(cols):
            self.frame.grid_columnconfigure(c, weight=0)

class MatchMenu(): # Falta por hacer
    def __init__(self, frame):
        self.frame = frame
        self.connected_tittle = None
        self.no_connected_tittle = None
        pass

    def init_widgets(self):
        # Connected player
        self.connected_tittle = tk.Label(self.frame, text="Desconectarse de la Partida.")
        self.connected_tittle.configure(bg="#1f1f1f", font=("Calibri Bold", 20), fg="white")
        self.disconnet_button = tk.Button(self.frame, text="DESCONECTARME", command=self.disconnect)
        self.disconnet_button.configure(font=pv.FUENTE_BOTONES_MENU, activebackground="#A6A6A6", width=18, bg="#A6A6A6")

        # No connected player
        self.no_connected_tittle = tk.Label(self.frame, text="Ingresa un código de invitación\npara poder conectarte a una partida.")
        self.no_connected_tittle.configure(bg="#1f1f1f", font=("Calibri Bold", 18), fg="white")
        self.no_connected_entry = tk.Entry(self.frame, width=30)
        self.no_connected_entry.configure(font=pv.FUENTE_BOTONES_MENU, bg="#A6A6A6")
        # Invitado

        pass

    def save(self): # Connect
        if pv.connection_wait_thread and pv.connection_wait_thread.is_alive():
            return
        code = self.no_connected_entry.get()
        pv.partida.serch_and_connect()

        # pv.partida.start_partide(game_mode='connected', color_selected, clock_status, time, bonus, fen)
        return True

    def disconnect(self):
        pass

    def show(self, mostrar_segun="no_connected_player"):
        if mostrar_segun == "connected_player":
            self.connected_tittle.grid(row=0, column=0)
            self.disconnet_button.grid(row=1, column=0, sticky="n")
        elif mostrar_segun == "no_connected_player":
            self.no_connected_tittle.grid(row=0, column=0)
            self.no_connected_entry.grid(row=1, column=0, sticky="n")

        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

    def hide(self):
        self.connected_tittle.grid_forget()
        self.disconnet_button.grid_forget()
        self.no_connected_tittle.grid_forget()
        self.no_connected_entry.grid_forget()

        self.frame.grid_rowconfigure(0, weight=0)
        self.frame.grid_rowconfigure(1, weight=0)
        self.frame.grid_columnconfigure(0, weight=0)

class StyleMenu(): # No parece ser necesario hacer algo más
    def __init__(self, frame):
        self.frame = frame
        self.labels = {}
        self.entrys = {}

    def init_widgets(self):
        for args in (["Casillas Blancas", "white", pv.white_theme], ["Casillas Negras", "black", pv.black_theme]):
            label = tk.Label(self.frame, text=args[0], fg="white")
            label.configure(font=("Calibri Bold", 18), bg=pv.OSCURO_SUAVE)
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
            if self.entrys["white"].get() == self.entrys["black"].get():
                raise Exception
            color = [self.entrys["white"].get(), self.entrys["black"].get()]
            for loop, square in enumerate(self.square_list):
                square.configure(bg=color[0])
                if loop == 1:
                    continue
                else: 
                    color.reverse()
        except:
            messagebox.showerror("HUBO UN ERROR", "La configuración seleccionada no puede ser aplicada.")
            return False
        else:
            return True

    def save(self):
        if self._update_color():
            pv.white_theme = self.entrys["white"].get().upper()
            pv.black_theme = self.entrys["black"].get().upper()
            pv.board.set_theme(pv.white_theme, pv.black_theme)
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
        self.entrys["white"].insert(0, pv.white_theme)
        self.entrys["black"].delete(0, tk.END)
        self.entrys["black"].insert(0, pv.black_theme)
        self.frame.focus_set()
        self.labels["white"].place_forget()
        self.entrys["white"].place_forget()
        self.labels["black"].place_forget()
        self.entrys["black"].place_forget()
        self.color_view.place_forget()
        self.check_color.place_forget()

class CreditsMenu(): # No parece que haga falta hacer algo, tal vez docstrigns
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
        self.thanks.configure(font=("Calibri Bold", 14), bg=pv.OSCURO_SUAVE)

        self.github_link = tk.Button(self.frame, text=self.link, fg="white", bd=0)
        self.github_link.configure(font=("Calibri Bold", 14), bg=pv.OSCURO_SUAVE)
        self.github_link.configure(activeforeground="white", activebackground=pv.OSCURO_SUAVE)
        self.github_link.configure(command=lambda: self.open_github_link())

    def open_github_link(self):
        open_new_tab("https://github.com/Camach-o")

    def show(self):
        self.thanks.place(x=45, y=30)
        self.github_link.place(x=175, y=185)

    def hide(self):
        self.thanks.place_forget()
        self.github_link.place_forget()

class PromotionMenu():
    def __init__(self, frame, top_level_menu):
        self.frame = frame
        self.top_level_menu = top_level_menu
        self.options = []
        self.white_images = None
        self.black_images = None
        self.active = False
        self.piece_to_promote_info = {}

    def init_widgets(self): # No veo por qué cambiar (Tal vez colocar letras en mayusculas)
        piece_types = ('q', 'r', 'b', 'n')

        for ptype in piece_types:
            piece_option = tk.Label(self.frame, text=ptype, width=80, height=80)
            piece_option.configure(bg=pv.white_theme, fg="white", bd=3, relief="solid")
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

    def define_promotion(self, event): # No parece necesario cambiar
        promotion = event.widget.configure().get("text")[-1]
        self.top_level_menu.close_promotion_menu()
        pv.partida.main_player.promotion_selected.set(promotion.upper())

class Menu():
    def __init__(self, root):
        self.root = root
        self.menu_frame = None
        self.selected_menu = None

        self.top_frame = None
        self.bottom_frame = None
        self.button_close = None
        self.button_save = None

        self.init_menu()

    def init_menu(self):
        # width=600, height=250 Reference of size
        self.menu_frame = tk.Frame(self.root, bd="2", bg=pv.OSCURO_SUAVE, relief="solid")
        self.top_frame = tk.Frame(self.menu_frame, bg=pv.OSCURO_SUAVE)
        self.top_frame.grid(row=0, column=0)
        self.bottom_frame = tk.Frame(self.menu_frame, bg=pv.OSCURO_SUAVE)
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
        # self.match_menu = MatchMenu(self.top_frame)
        # self.match_menu.init_widgets()
        self.promotion_menu = PromotionMenu(self.top_frame, self)
        self.promotion_menu.init_widgets()

    def _place_menu(self): 
        """ Returns the coordinates where the menu will be placed."""

        self.menu_frame.update()
        height_menu = self.menu_frame.winfo_height()
        width_menu = self.menu_frame.winfo_width()
        y = (pv.height_windows / 2) - (height_menu / 2)
        x = (pv.width_windows / 2) - (width_menu / 2)
        self.menu_frame.place(y=y, x=x)

    def _show_buttons(self, txt_save_button="Guardar", only_close=False):
        self.button_save.pack(side="left", padx=(0, 80), pady=(0, 5))
        self.button_close.pack(side="right", padx=(80, 0), pady=(0, 5))
        self.button_save.configure(text=txt_save_button)

        if only_close:
            self.button_save.pack_forget()
            self.button_close.pack_forget()
            self.button_close.pack(pady=(0, 5))

    def show_promotion_menu(self, color="white"):
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
        
        - option (event): Widget that called the function.
        """

        if self.promotion_menu.active:
            return
        if self.selected_menu:
            self.close_menu()
        
        self.menu_frame.place(y=50, x=200)
        option_called = option.widget.configure().get("text")[-1]
        if pv.ongoing_game:
            if option_called == "Dificultad" or option_called == "Emparejamiento":
                messagebox.showwarning("FINALIZA LA PARTIDA", 
                                       "Mientras haya una partida en juego no se pueden realizar nuevos ajustes.")
                return

        if option_called in pv.menu_options:
            if option_called == "Partida":
                self.selected_menu = self.partide_menu
                self._show_buttons(txt_save_button="Iniciar")
            elif option_called == "Dificultad":
                self.selected_menu = self.difficulty_menu
                self.top_frame.configure(width=600, height=250)
                self.top_frame.grid_propagate(False)
                self._show_buttons(txt_save_button="Guardar")
            # elif option_called == "Emparejamiento":
            #     messagebox.showinfo("Información", "Por los momentos las partidas vía LAN no están activas")
            #     self.close_menu()
            #     return False
                # self.selected_menu = self.match_menu
                # self.top_frame.configure(width=600, height=200)
                # self.top_frame.grid_propagate(False)
                # self._show_buttons(txt_save_button="Conectarme")
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
