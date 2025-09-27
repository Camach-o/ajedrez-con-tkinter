import tkinter as tk
from components import project_vars
from components import menu
from components import clock
from components import board
from components import panel

# TEMA_PREDETERMINADO_TABLERO =  ("#bb935b", "#592f0a") # Blanco | Negro

def start_program(root, board_view):
    # Sections Frame
    back_frame = tk.Frame(root, bg="#191918")
    back_frame.place(x=0, y=0)

    # Menu
    menu_bar = tk.Frame(back_frame, width=1070, height=30, bg=project_vars.OSCURO_FUERTE)
    menu_bar.grid_propagate(False)
    menu_bar.grid(row=0, column=0, columnspan=3, padx=(10, 0), pady=(5, 0))

    mymenu = menu.Menu(root)

    for indx, opcion in enumerate(project_vars.menu_options):
        boton_opcion = tk.Label(menu_bar, text=opcion, font=("Arial", 16), bg=project_vars.OSCURO_FUERTE, fg="white")
        boton_opcion.bind("<Button-1>", mymenu.show_menu)
        boton_opcion.grid(row=0, column=indx, padx=(0, 15))

    # Clock
    clock_frame = tk.Frame(back_frame, bg="#191918", width=120, height=640)
    clock_frame.propagate(False)
    clock_frame.grid(row=1, column=0, padx=6, pady=8)
    project_vars.clock_frame = clock_frame

    object_clock = clock.Clock(clock_frame, board_view)
    object_clock.create_clock_widgets()
    project_vars.clock = object_clock

    # Board
    board_frame = tk.Frame(back_frame, bg="#191918", width=300)
    board_frame.grid(row=1, column=1, pady=8)

    object_board = board.Board(board_frame)
    object_board.start_board()
    project_vars.board = object_board

    # Panel
    panel_frame = tk.Frame(back_frame, bg="#191918", width=300)
    panel_frame.grid(row=1, column=2, sticky="nswe", padx=6, pady=8)

    object_panel = panel.Panel(panel_frame)
    object_panel.start_panel()
    project_vars.panel = object_panel

    # Geometry of root
    back_frame.update_idletasks()
    ancho = back_frame.winfo_width()
    alto = back_frame.winfo_height()

    root.geometry(f"{ancho}x{alto}+200+80")
    root.update()

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Ajedrez")
    root.configure(bg="#191918")
    root.resizable(False, False)

    start_program(root, 1)
    
    

    root.mainloop()