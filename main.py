import tkinter as tk
from components import project_vars
from components import menu
from components import clock
from components import board
from components import panel
from components import game

window = tk.Tk()
window.title("Ajedrez")
window.configure(bg="#191918")
window.resizable(False, False)

# Back Container
back_frame = tk.Frame(window, bg="#191918")
back_frame.place(x=0, y=0)

# Menu
menu_frame = tk.Frame(back_frame, width=1070, height=30)
menu_frame.configure(bg=project_vars.OSCURO_FUERTE)
menu_frame.grid_propagate(False)
menu_frame.grid(row=0, column=0, columnspan=3, padx=(10, 0), pady=(5, 0))

game_menu = menu.Menu(window)
for indx, txt_option in enumerate(project_vars.menu_options):
    option_label = tk.Label(menu_frame, text=txt_option, font=("Arial", 16))
    option_label.configure(bg=project_vars.OSCURO_FUERTE, fg="white")
    option_label.bind("<Button-1>", game_menu.show_menu)
    option_label.grid(row=0, column=indx, padx=(0, 15))
project_vars.menubar = game_menu

# Clock
clock_frame = tk.Frame(back_frame, bg="#191918", width=120, height=640)
clock_frame.propagate(False)
clock_frame.grid(row=1, column=0, padx=6, pady=8)
project_vars.clock_frame = clock_frame

game_clock = clock.Clock(clock_frame)
game_clock.put_clock()
project_vars.clock = game_clock

# Board
board_frame = tk.Frame(back_frame, bg="#191918", width=300)
board_frame.grid(row=1, column=1, pady=8)
chess_game = game.ChessGame(board_frame)
chess_game.ob_board.put_board()
project_vars.game = chess_game

# Panel
panel_frame = tk.Frame(back_frame, bg="#191918", width=300)
panel_frame.grid(row=1, column=2, sticky="nswe", padx=6, pady=8)

game_panel = panel.Panel(panel_frame)
game_panel.put_panel()
project_vars.panel = game_panel

# Geometry of window
back_frame.update_idletasks()
width = back_frame.winfo_width()
height = back_frame.winfo_height()
window.geometry(f"{width}x{height}+200+80")
window.update()

if __name__ == '__main__':
    window.mainloop()