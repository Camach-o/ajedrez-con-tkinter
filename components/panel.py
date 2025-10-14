if __name__ == "__main__":
    import tkinter as tk
    import project_vars as project_vars
    from tkinter import ttk
    from PIL import Image, ImageTk
    from itertools import count
    import re
else:
    import tkinter as tk
    from tkinter import ttk
    from PIL import Image, ImageTk
    import components.project_vars as project_vars
    from itertools import count
    import re

class Panel:
    def __init__(self, container):
        self.container = container
        self.img_atras = ImageTk.PhotoImage(Image.open("contenido_grafico/imagenes_panel/atras.png"))
        self.img_adelante = ImageTk.PhotoImage(Image.open("contenido_grafico/imagenes_panel/adelante.png"))
        self.img_resetear = ImageTk.PhotoImage(Image.open("contenido_grafico/imagenes_panel/retroceder.png"))
        self.row_index = count(1)
        self.fen = None

    # Movements viewer
    def create_movements_viewer_widgets(self):
        self.frame_movements_viewer = tk.Frame(self.container, width=286, height=370)
        self.frame_movements_viewer.configure(bg=project_vars.OSCURO_SUAVE, relief="solid", bd=1)
        self.frame_movements_viewer.grid_propagate(False)
        self.frame_movements_viewer.grid(row=0, column=0)

        self.frame_movements_viewer.columnconfigure(0, weight=0)
        self.frame_movements_viewer.columnconfigure(1, weight=1)
        self.frame_movements_viewer.columnconfigure(2, weight=1)
        self.frame_movements_viewer.rowconfigure(2, weight=1)

        title_movements_viewer = tk.Label(self.frame_movements_viewer)
        title_movements_viewer.configure(bg=project_vars.OSCURO_SUAVE, fg="white")
        title_movements_viewer.configure(text="TABLA DE MOVIMIENTOS", font=("Calibri Bold", 14))
        title_movements_viewer.grid(row=0, column=0, columnspan=3, sticky="ew")

        title_n_movement = tk.Label(self.frame_movements_viewer, width=5)
        title_n_movement.configure(bg=project_vars.OSCURO_SUAVE, anchor="w")
        title_n_movement.configure(text=" N°", fg="white", font=("Calibri Bold", 12))
        title_n_movement.grid(row=1, column=0)

        title_white_movements = tk.Label(self.frame_movements_viewer)
        title_white_movements.configure(bg=project_vars.OSCURO_SUAVE, anchor="w")
        title_white_movements.configure(text="BLANCAS", fg="white", font=("Calibri Bold", 12))
        title_white_movements.grid(row=1, column=1, sticky="ew", padx=(10, 0))

        title_black_movements = tk.Label(self.frame_movements_viewer)
        title_black_movements.configure(bg=project_vars.OSCURO_SUAVE, anchor="w")
        title_black_movements.configure(text="NEGRAS", fg="white", font=("Calibri Bold", 12))
        title_black_movements.grid(row=1, column=2, sticky="ew", padx=(10, 0))
    
        self.movements_viewer_canvas = tk.Canvas(self.frame_movements_viewer, height=200)
        self.movements_viewer_canvas.configure(bg=project_vars.OSCURO_SUAVE, highlightthickness=0)
        self.movements_viewer_canvas.grid(row=2, column=0, columnspan=3, sticky="nsew", pady=(5, 5))

        self.movements_viewer_framescroll = tk.Frame(self.movements_viewer_canvas, bg=project_vars.OSCURO_SUAVE)
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

    def insert_movement(self, _, pieces, movement): # No tocar
        """ Set the movement in the panel.

        Args:
            pieces (str): The pieces that moved
            movement (str): The movement to insert
        """

        if pieces == "whites":
            row = next(self.row_index)

            row_label = tk.Label(self.movements_viewer_framescroll, width=3, bg=project_vars.OSCURO_SUAVE)
            row_label.configure(fg="white", anchor="w", text=row, font=("Calibri Bold", 12))
            row_label.grid(column=0, row=row, sticky="nw", padx=(5, 0), pady=1)

            white_label = tk.Label(self.movements_viewer_framescroll, bg=project_vars.OSCURO_SUAVE,
                             fg="white", anchor="w", text=movement, font=("Calibri Bold", 12))
            white_label.grid(column=1, row=row, sticky="nw", padx=(26, 0), pady=1)

            self.movements_viewer_framescroll.update_idletasks()
            self.movements_viewer_canvas.yview_moveto(1.0) 
        
        elif pieces == "blacks":
            row = int("".join(re.findall(r'\d+', str(iter(self.row_index))))) -1

            back_label = tk.Label(self.movements_viewer_framescroll, bg=project_vars.OSCURO_SUAVE,
                             fg="white", anchor="w", text=movement, font=("Calibri Bold", 12))
            back_label.grid(column=2, row=row, sticky="nw", padx=(100, 0), pady=1)

    # Controller
    def create_movements_controller_widgets(self):
        
        ctlr_frame = tk.Frame(self.container, bd=1, relief="solid")
        ctlr_frame.grid(row=1, column=0, pady=5)

        btn_atras = tk.Button(ctlr_frame, width=92, height=40, bd=0)
        btn_atras.configure(bg=project_vars.OSCURO_SUAVE, activebackground=project_vars.OSCURO_SUAVE, image=self.img_atras)
        btn_atras.grid(row=0, column=0)

        btn_adelante = tk.Button(ctlr_frame, width=94, height=40, bd=0)
        btn_adelante.configure(bg=project_vars.OSCURO_SUAVE, activebackground=project_vars.OSCURO_SUAVE, image=self.img_resetear)
        btn_adelante.grid(row=0, column=1)

        btn_reiniciar = tk.Button(ctlr_frame, width=92, height=40, bd=0)
        btn_reiniciar.configure(bg=project_vars.OSCURO_SUAVE, activebackground=project_vars.OSCURO_SUAVE, image=self.img_adelante)
        btn_reiniciar.grid(row=0, column=2)

    # Chat
    def create_chat_widgets(self):
        chat_frame = tk.Frame(self.container, bg=project_vars.OSCURO_FUERTE, relief="solid", bd=1)
        chat_frame.grid(row=2, column=0)

        chat_text = tk.Text(chat_frame, width=38, height=10, bg=project_vars.OSCURO_SUAVE)
        chat_text.configure(font=("Calibri", 11), fg="white", relief="flat")
        chat_text.insert(tk.END, 'Escribe algo...\n')
        chat_text.configure(state='disabled')
        chat_text.grid(row=0, column=0)

        estilo_scrollbar = ttk.Style()
        estilo_scrollbar.theme_use("clam")
        estilo_scrollbar.configure("CustomScrollbar.Vertical.TScrollbar", 
                                    gripcount=0,
                                    background="#2e2e2e", 
                                    darkcolor=project_vars.OSCURO_SUAVE, 
                                    lightcolor="#3f3f3f", 
                                    troughcolor=project_vars.OSCURO_SUAVE, 
                                    bordercolor="black", 
                                    arrowcolor="#ffffff",
                                    relief="flat",
                                    troughrelief="sunken",
                                    borderwidth=2)

        estilo_scrollbar.map("CustomScrollbar.Vertical.TScrollbar",
                background=[('active', '#2e2e2e'), ('pressed', '#2e2e2e')],
                arrowcolor=[('active', '#ffffff'), ('pressed', '#ffffff')])

        chat_scrollbar = ttk.Scrollbar(chat_frame, style="CustomScrollbar.Vertical.TScrollbar")
        chat_scrollbar.configure(command=chat_text.yview) 
        chat_scrollbar.grid(row=0, column=1, sticky="ns")

        chat_text.configure(yscrollcommand=chat_scrollbar.set)

        entry_frame = tk.Frame(chat_frame, height=30, bg=project_vars.OSCURO_SUAVE)
        entry_frame.grid(row=1, column=0, sticky="ew")

        separador_text_entry = tk.Frame(entry_frame, height=1, bg="black")
        separador_text_entry.pack(side="top", fill="x")

        chat_entry = tk.Entry(entry_frame, width=35, bg=project_vars.OSCURO_SUAVE, relief="flat", fg="white")
        chat_entry.pack(padx=2, pady=5, fill="both", expand=True)

        boton_enviar = tk.Button(chat_frame, width=1, bg=project_vars.OSCURO_SUAVE, relief="solid", bd=1)
        boton_enviar.configure(text=">", font=("Arial", 7), fg="white")
        boton_enviar.configure(activebackground=project_vars.OSCURO_SUAVE, activeforeground="white")
        boton_enviar.configure(command=lambda: self.send_message(chat_frame, chat_text, chat_entry))
        boton_enviar.grid(row=1, column=1, sticky="ns")

    def send_message(self, frame, wid_text, wid_entry):
        mensaje = wid_entry.get()

        if mensaje:
            wid_entry.delete(0, tk.END)
            wid_text.configure(state='normal')
            wid_text.insert(tk.END, f'\n{mensaje}')
            wid_text.configure(state='disabled')

            frame.update_idletasks()
            wid_text.yview_moveto(1.0) 
    
    def recive_message(self, wid_text, wid_entry, mensaje):
        wid_entry.delete(0, tk.END)
        wid_text.configure(state='normal')
        wid_text.insert(tk.END, f'\n{mensaje}')
        wid_text.configure(state='disabled')
        # wid_text.update_idletasks()
        # wid_text.yview_moveto(1.0)

    def put_panel(self):
        self.create_movements_viewer_widgets()
        self.create_movements_controller_widgets()
        self.create_chat_widgets()
        
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")



    panel = Panel(root)
    panel.put_panel()

    a = "blacks"

    def h(event):
        global a
        if a == "whites":
            a = "blacks"
        else:
            a = "whites"

        
        panel.insert_movement(None, a, "a4")

    root.bind("<Key>", h)

    root.mainloop()