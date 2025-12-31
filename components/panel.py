import tkinter as tk
import re
from tkinter import ttk
from itertools import count
from PIL import Image, ImageTk
import components.project_vars as pv

class Panel:
    def __init__(self, windows):
        self.windows = windows
        self.img_back = ImageTk.PhotoImage(Image.open("assets/panel/back.png"))
        self.img_next = ImageTk.PhotoImage(Image.open("assets/panel/next.png"))
        self.img_first_fen = ImageTk.PhotoImage(Image.open("assets/panel/first_fen.png"))
        self.img_last_fen = ImageTk.PhotoImage(Image.open("assets/panel/last_fen.png"))
        self.row_index = count(1)

        self.movements_labels_container = []

        # Controller
        self.previous_fen_bttn = None
        self.first_fen_bttn = None
        self.last_fen_bttn = None
        self.next_fen_bttn = None


        # Chat
        self.chat_entry = None
        self.chat_text = None
        self.chat_frame = None

    # Movements viewer
    def create_movements_viewer_widgets(self):
        self.frame_movements_viewer = tk.Frame(self.windows, width=286, height=370)
        self.frame_movements_viewer.configure(bg=pv.OSCURO_SUAVE, relief="solid", bd=1)
        self.frame_movements_viewer.grid_propagate(False)
        self.frame_movements_viewer.grid(row=0, column=0)

        self.frame_movements_viewer.columnconfigure(0, weight=0)
        self.frame_movements_viewer.columnconfigure(1, weight=1)
        self.frame_movements_viewer.columnconfigure(2, weight=1)
        self.frame_movements_viewer.rowconfigure(2, weight=1)

        title_movements_viewer = tk.Label(self.frame_movements_viewer)
        title_movements_viewer.configure(bg=pv.OSCURO_SUAVE, fg="white")
        title_movements_viewer.configure(text="TABLA DE MOVIMIENTOS", font=("Calibri Bold", 14))
        title_movements_viewer.grid(row=0, column=0, columnspan=3, sticky="ew")

        title_n_movement = tk.Label(self.frame_movements_viewer, width=5)
        title_n_movement.configure(bg=pv.OSCURO_SUAVE, anchor="w")
        title_n_movement.configure(text=" N°", fg="white", font=("Calibri Bold", 12))
        title_n_movement.grid(row=1, column=0)

        title_white_movements = tk.Label(self.frame_movements_viewer)
        title_white_movements.configure(bg=pv.OSCURO_SUAVE, anchor="w")
        title_white_movements.configure(text="BLANCAS", fg="white", font=("Calibri Bold", 12))
        title_white_movements.grid(row=1, column=1, sticky="ew", padx=(10, 0))

        title_black_movements = tk.Label(self.frame_movements_viewer)
        title_black_movements.configure(bg=pv.OSCURO_SUAVE, anchor="w")
        title_black_movements.configure(text="NEGRAS", fg="white", font=("Calibri Bold", 12))
        title_black_movements.grid(row=1, column=2, sticky="ew", padx=(10, 0))

        self.movements_viewer_canvas = tk.Canvas(self.frame_movements_viewer, height=200)
        self.movements_viewer_canvas.configure(bg=pv.OSCURO_SUAVE, highlightthickness=0)
        self.movements_viewer_canvas.grid(row=2, column=0, columnspan=3, sticky="nsew", pady=(5, 5))

        self.movements_viewer_framescroll = tk.Frame(self.movements_viewer_canvas, bg=pv.OSCURO_SUAVE)
        self.movements_viewer_framescroll.columnconfigure(0, weight=0)
        self.movements_viewer_framescroll.columnconfigure(1, weight=1)
        self.movements_viewer_framescroll.columnconfigure(2, weight=1)
        framescroll_id = self.movements_viewer_canvas.create_window((0, 0), window=self.movements_viewer_framescroll, anchor="nw")

        def update_movements_viewer(_):
            self.movements_viewer_canvas.configure(scrollregion=self.movements_viewer_canvas.bbox("all"))

        def scroll_event(event):
            if self.movements_viewer_canvas.bbox(framescroll_id)[3] >= self.movements_viewer_canvas.bbox(framescroll_id)[2]:
                self.movements_viewer_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        self.movements_viewer_framescroll.bind("<Configure>", update_movements_viewer)
        self.movements_viewer_canvas.bind_all("<MouseWheel>", scroll_event)

    def insert_movement(self, pieces, movement): # No tocar
        """ Set the movement in the panel.

        Args:
            pieces (str): The pieces that moved
            movement (str): The movement to insert
        """

        if pieces == "whites":
            row = next(self.row_index)

            row_label = tk.Label(self.movements_viewer_framescroll, width=3, bg=pv.OSCURO_SUAVE)
            row_label.configure(fg="white", anchor="w", text=row, font=("Calibri Bold", 12))
            row_label.grid(column=0, row=row, sticky="nw", padx=(5, 0), pady=1)

            white_label = tk.Label(self.movements_viewer_framescroll, width=7, bg=pv.OSCURO_SUAVE,
                             fg="white", anchor="w", text=movement, font=("Calibri Bold", 12))
            white_label.grid(column=1, row=row, sticky="nw", padx=(26, 0), pady=1)

            self.movements_labels_container.append(row_label)
            self.movements_labels_container.append(white_label)
            self.movements_viewer_framescroll.update_idletasks()
            self.movements_viewer_canvas.yview_moveto(1.0)

        elif pieces == "blacks":
            row = int("".join(re.findall(r'\d+', str(iter(self.row_index))))) -1

            back_label = tk.Label(self.movements_viewer_framescroll, bg=pv.OSCURO_SUAVE,
                             fg="white", anchor="w", text=movement, font=("Calibri Bold", 12))
            back_label.grid(column=2, row=row, sticky="nw", padx=(60, 0), pady=1)
            self.movements_labels_container.append(back_label)

    def restart_movements_viewer(self):
        self.movements_viewer_canvas.yview_moveto(0.0)
        self.row_index = count(1)

        for movement_label in self.movements_labels_container:
            movement_label.grid_forget()

        self.movements_labels_container = []
        self.movements_viewer_framescroll.update_idletasks()

    # Controller
    def create_movements_controller_widgets(self):
        ctlr_frame = tk.Frame(self.windows, bd=1, relief="solid")
        ctlr_frame.grid(row=1, column=0, pady=5)

        self.previous_fen_bttn = tk.Button(ctlr_frame, width=69, height=40, bd=0)
        self.previous_fen_bttn.configure(bg=pv.OSCURO_SUAVE, activebackground=pv.OSCURO_SUAVE, image=self.img_back)
        self.previous_fen_bttn.grid(row=0, column=0)

        self.first_fen_bttn = tk.Button(ctlr_frame, width=69, height=40, bd=0)
        self.first_fen_bttn.configure(bg=pv.OSCURO_SUAVE, activebackground=pv.OSCURO_SUAVE, image=self.img_first_fen)
        self.first_fen_bttn.grid(row=0, column=1)

        self.last_fen_bttn = tk.Button(ctlr_frame, width=69, height=40, bd=0)
        self.last_fen_bttn.configure(bg=pv.OSCURO_SUAVE, activebackground=pv.OSCURO_SUAVE, image=self.img_last_fen)
        self.last_fen_bttn.grid(row=0, column=2)

        self.next_fen_bttn = tk.Button(ctlr_frame, width=69, height=40, bd=0)
        self.next_fen_bttn.configure(bg=pv.OSCURO_SUAVE, activebackground=pv.OSCURO_SUAVE, image=self.img_next)
        self.next_fen_bttn.grid(row=0, column=3)

    # Chat
    def create_chat_widgets(self):
        self.chat_frame = tk.Frame(self.windows, bg=pv.OSCURO_FUERTE, relief="solid", bd=1)
        self.chat_frame.grid(row=2, column=0)

        self.chat_text = tk.Text(self.chat_frame, width=38, height=10, bg=pv.OSCURO_SUAVE)
        self.chat_text.configure(font=("Calibri", 11), fg="white", relief="flat")
        self.chat_text.insert(tk.END, 'Escribe algo...\n')
        self.chat_text.configure(state='disabled')
        self.chat_text.grid(row=0, column=0)

        estilo_scrollbar = ttk.Style()
        estilo_scrollbar.theme_use("clam")
        estilo_scrollbar.configure("CustomScrollbar.Vertical.TScrollbar",
                                    gripcount=0,
                                    background="#2e2e2e",
                                    darkcolor=pv.OSCURO_SUAVE,
                                    lightcolor="#3f3f3f",
                                    troughcolor=pv.OSCURO_SUAVE,
                                    bordercolor="black",
                                    arrowcolor="#ffffff",
                                    relief="flat",
                                    troughrelief="sunken",
                                    borderwidth=2)

        estilo_scrollbar.map("CustomScrollbar.Vertical.TScrollbar",
                background=[('active', '#2e2e2e'), ('pressed', '#2e2e2e')],
                arrowcolor=[('active', '#ffffff'), ('pressed', '#ffffff')])

        chat_scrollbar = ttk.Scrollbar(self.chat_frame, style="CustomScrollbar.Vertical.TScrollbar")
        chat_scrollbar.configure(command=self.chat_text.yview)
        chat_scrollbar.grid(row=0, column=1, sticky="ns")

        self.chat_text.configure(yscrollcommand=chat_scrollbar.set)

        entry_frame = tk.Frame(self.chat_frame, height=30, bg=pv.OSCURO_SUAVE)
        entry_frame.grid(row=1, column=0, sticky="ew")

        separador_text_entry = tk.Frame(entry_frame, height=1, bg="black")
        separador_text_entry.pack(side="top", fill="x")

        self.chat_entry = tk.Entry(entry_frame, width=35, bg=pv.OSCURO_SUAVE, relief="flat", fg="white")
        self.chat_entry.pack(padx=2, pady=5, fill="both", expand=True)

        boton_enviar = tk.Button(self.chat_frame, width=1, bg=pv.OSCURO_SUAVE, relief="solid", bd=1)
        boton_enviar.configure(text=">", font=("Arial", 7), fg="white")
        boton_enviar.configure(activebackground=pv.OSCURO_SUAVE, activeforeground="white")
        boton_enviar.configure(command=self.send_message)
        boton_enviar.grid(row=1, column=1, sticky="ns")

    def send_message(self):
        mensaje = self.chat_entry.get()

        # if pv.partida:
        #     pv.partida.send_message(mensaje)

        if mensaje:
            self.chat_entry.delete(0, tk.END)
            self.chat_text.configure(state='normal')
            self.chat_text.insert(tk.END, f'\n{mensaje}')
            self.chat_text.configure(state='disabled')

            self.chat_frame.update_idletasks()
            self.chat_text.yview_moveto(1.0)

    def recive_message(self, mensaje):
        self.chat_entry.delete(0, tk.END)
        self.chat_text.configure(state='normal')
        self.chat_text.insert(tk.END, f'\n{mensaje}')
        self.chat_text.configure(state='disabled')
        # self.chat_text.update_idletasks()
        # self.chat_text.yview_moveto(1.0)

    def put_panel(self):
        self.create_movements_viewer_widgets()
        self.create_movements_controller_widgets()
        self.create_chat_widgets()
