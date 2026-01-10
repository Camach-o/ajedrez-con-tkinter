import tkinter as tk
from components import board
from components import menu
from components import panel
from components import clock
from components import partide
from components import project_vars as pv

window = tk.Tk()
window.title(pv.APP_TITTLE)
window.configure(bg=pv.DARK_GRAY)
window.resizable(False, False)
pv.window = window

# Back Container
back_frame = tk.Frame(window, bg=pv.DARK_GRAY)
back_frame.place(x=0, y=0)

# Menu
menu_frame = tk.Frame(back_frame, width=1070, height=30)
menu_frame.configure(bg=pv.DARK_GRAY)
menu_frame.grid_propagate(False)
menu_frame.grid(row=0, column=0, columnspan=3, padx=(10, 0), pady=(5, 0))

game_menu = menu.Menu(window)
for indx, txt_option in enumerate(pv.menu_options):
    option_label = tk.Label(menu_frame, text=txt_option, font=("Arial", 16))
    option_label.configure(bg=pv.DARK_GRAY, fg="white")
    option_label.bind("<Button-1>", game_menu.show_menu)
    option_label.grid(row=0, column=indx, padx=(0, 15))
pv.menu = game_menu

# Clock
clock_frame = tk.Frame(back_frame, bg=pv.DARK_GRAY, width=120, height=640)
clock_frame.propagate(False)
clock_frame.grid(row=1, column=0, padx=6, pady=8)

game_clock = clock.Clock(clock_frame)
game_clock.put_clock()
pv.clock = game_clock

# Board
board_frame = tk.Frame(back_frame, bg=pv.DARK_GRAY, width=300)
board_frame.grid(row=1, column=1, pady=8)
game_board = board.ChessBoard(board_frame)
game_board.put_board()
pv.board = game_board

# Panel
panel_frame = tk.Frame(back_frame, bg=pv.DARK_GRAY, width=300)
panel_frame.grid(row=1, column=2, sticky="nswe", padx=6, pady=8)

game_panel = panel.Panel(panel_frame)
game_panel.put_panel()
pv.panel = game_panel

# Partide
pv.partide = partide.ChessPartide()

# Geometry of window
back_frame.update_idletasks()
pv.width_windows = back_frame.winfo_width()
pv.height_windows = back_frame.winfo_height()
window.geometry(f"{pv.width_windows}x{pv.height_windows}+200+80")
window.update()

if __name__ == '__main__':
    window.mainloop()
