import tkinter as tk
from tkinter import messagebox
import project_vars

#game_type, color, clock_status, clock_type, time, bonus, fen

def start_a_partide():
    if not project_vars.partida:
        messagebox.showerror(title="Error")
    project_vars.partida.init_partide()
    print(project_vars.partida)

root = tk.Tk()

#   Set configure of the frame
back_frame = tk.Frame(root, width=400, height=700, relief="solid")
back_frame.configure(bd="2", bg="#1f1f1f") # , highlightthickness=0
back_frame.propagate(False)
back_frame.pack()

#######################################################################

partideopts_frame = tk.Frame(back_frame, width=400, height=180, bg="#1f1f1f")
partideopts_frame.grid(row=0, column=0)

type_game = tk.StringVar()
type_game.set(1)
color_selected = tk.StringVar()
color_selected.set(1)

partida_label = tk.Label(partideopts_frame, text="Partida")
partida_label.configure(bg="#1f1f1f", font=("Calibri Bold", 18), fg="white")
partida_label.place(x=15, y=15)

opts_partida_label = tk.Label(partideopts_frame, text="Opciones de la partida")
opts_partida_label.configure(bg="#1f1f1f", font=("Calibri Bold", 15), fg="white")
opts_partida_label.place(x=15, y=55)

only_option = tk.Radiobutton(partideopts_frame, text="Jugar Solo", variable=type_game, value=1)
only_option.configure(bg=project_vars.OSCURO_SUAVE, activebackground=project_vars.OSCURO_SUAVE)      
only_option.configure(fg="white", font=("Calibri Bold", 14), activeforeground="white")
only_option.configure(selectcolor=project_vars.OSCURO_SUAVE)
only_option.place(x=35, y=95)

stockfish_option = tk.Radiobutton(partideopts_frame, text="Jugar contra Stockfish", variable=type_game, value=2)
stockfish_option.configure(bg=project_vars.OSCURO_SUAVE, activebackground=project_vars.OSCURO_SUAVE)      
stockfish_option.configure(fg="white", font=("Calibri Bold", 14), activeforeground="white")
stockfish_option.configure(selectcolor=project_vars.OSCURO_SUAVE)
stockfish_option.place(x=170, y=95)

whites_label = tk.Radiobutton(partideopts_frame, text="Jugar con Blancas", variable=color_selected, value=1)
whites_label.configure(bg=project_vars.OSCURO_SUAVE, activebackground=project_vars.OSCURO_SUAVE)      
whites_label.configure(fg="white", font=("Calibri Bold", 14), activeforeground="white")
whites_label.configure(selectcolor=project_vars.OSCURO_SUAVE)
whites_label.place(x=35, y=140)

blacks_label = tk.Radiobutton(partideopts_frame, text="Jugar con Negras", variable=color_selected, value=2)
blacks_label.configure(bg=project_vars.OSCURO_SUAVE, activebackground=project_vars.OSCURO_SUAVE)      
blacks_label.configure(fg="white", font=("Calibri Bold", 14), activeforeground="white")
blacks_label.configure(selectcolor=project_vars.OSCURO_SUAVE)
blacks_label.place(x=220, y=140)

#########################################################################


clockopts_frame = tk.Frame(back_frame, width=400, height=220, bg="#1f1f1f")
clockopts_frame.grid(row=2, column=0)

clock_status = tk.StringVar()
clock_status.set(1)
clock_type = tk.StringVar()
clock_type.set(1)

clock_label = tk.Label(clockopts_frame, text="Opciones del reloj")
clock_label.configure(bg="#1f1f1f", font=("Calibri Bold", 15), fg="white")
clock_label.place(x=15, y=15)

with_reloj = tk.Radiobutton(clockopts_frame, text="Jugar con Reloj", variable=clock_status, value=1)
with_reloj.configure(bg=project_vars.OSCURO_SUAVE, activebackground=project_vars.OSCURO_SUAVE)      
with_reloj.configure(fg="white", font=("Calibri Bold", 14), activeforeground="white")
with_reloj.configure(selectcolor=project_vars.OSCURO_SUAVE)
with_reloj.place(x=35, y=55)

without_reloj = tk.Radiobutton(clockopts_frame, text="Jugar sin Reloj", variable=clock_status, value=2)
without_reloj.configure(bg=project_vars.OSCURO_SUAVE, activebackground=project_vars.OSCURO_SUAVE)      
without_reloj.configure(fg="white", font=("Calibri Bold", 14), activeforeground="white")
without_reloj.configure(selectcolor=project_vars.OSCURO_SUAVE)
without_reloj.place(x=220, y=55)

manual = tk.Radiobutton(clockopts_frame, text="Modo Automatico", variable=clock_type, value=1)
manual.configure(bg=project_vars.OSCURO_SUAVE, activebackground=project_vars.OSCURO_SUAVE)      
manual.configure(fg="white", font=("Calibri Bold", 14), activeforeground="white")
manual.configure(selectcolor=project_vars.OSCURO_SUAVE)
manual.place(x=35, y=100)

automatico = tk.Radiobutton(clockopts_frame, text="Modo Manual", variable=clock_type, value=2)
automatico.configure(bg=project_vars.OSCURO_SUAVE, activebackground=project_vars.OSCURO_SUAVE)      
automatico.configure(fg="white", font=("Calibri Bold", 14), activeforeground="white")
automatico.configure(selectcolor=project_vars.OSCURO_SUAVE)
automatico.place(x=220, y=100)

##################################################################################

# Time and Increment section
def validate_entry(text):
    return text == "" or (text.isdigit() and len(text) <= 2)
vcmd = (clockopts_frame.register(validate_entry), "%P")

# Time
time_label = tk.Label(clockopts_frame, bg=project_vars.OSCURO_SUAVE)
time_label.configure(text="Tiempo", font=("Calibri Bold", 14), fg="white")
time_label.place(x=35, y=150)

time_entry = tk.Entry(clockopts_frame, width=20, cursor="arrow", bg="#A6A6A6", relief="raised", bd=1)
time_entry.configure(validate="key", validatecommand=vcmd)
time_entry.insert(0, project_vars.clock_time)
time_entry.pack_propagate(False)
time_entry.place(x=130, y=155)

# Increment
bonus_label = tk.Label(clockopts_frame, bg=project_vars.OSCURO_SUAVE)
bonus_label.configure(text="Bonus", font=("Calibri Bold", 14), fg="white")
bonus_label.place(x=35, y=190)

bonus_entry = tk.Entry(clockopts_frame, width=20, cursor="arrow", bg="#A6A6A6", relief="raised", bd=1)
bonus_entry.configure(validate="key", validatecommand=vcmd)
bonus_entry.insert(0, project_vars.clock_bonus)
bonus_entry.pack_propagate(False)
bonus_entry.place(x=130, y=195)


#########################################################################

fen_frame = tk.Frame(back_frame, width=400, height=230, bg="#1f1f1f")
fen_frame.grid(row=3, column=0)

fen = tk.Label(fen_frame, text="Configuración del FEN")
fen.configure(bg="#1f1f1f", font=("Calibri Bold", 15), fg="white")
fen.place(x=15, y=15)

startpos_fen = tk.Entry(fen_frame, width=36, bg="#A6A6A6")
startpos_fen.configure(font=project_vars.FUENTE_BOTONES_MENU)
startpos_fen.place(x=15, y=60)

startpos = tk.Button(fen_frame, width=13, text="Posición Inicial", bg="#A6A6A6")
startpos.configure(font=project_vars.FUENTE_BOTONES_MENU, activebackground="#A6A6A6")
startpos.place(x=15, y=105)

save_button = tk.Button(fen_frame, width=8, text="Iniciar", bg="#A6A6A6")
save_button.configure(font=project_vars.FUENTE_BOTONES_MENU, activebackground="#A6A6A6")
save_button.configure(command=start_a_partide)
save_button.place(x=301, y=180)
cancel_button = tk.Button(fen_frame, width=8, text="Cancelar", bg="#A6A6A6")
cancel_button.configure(font=project_vars.FUENTE_BOTONES_MENU, activebackground="#A6A6A6")
cancel_button.configure(command=root.destroy)
cancel_button.place(x=10, y=180)

root.mainloop()