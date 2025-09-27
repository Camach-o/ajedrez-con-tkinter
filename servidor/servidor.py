import tkinter as tk
from tkinter import ttk

ventana = tk.Tk()
ventana.title("Sistema de Emparejamiento")
ventana.geometry("+500+200")
ventana.resizable(False, False)
ventana.configure(bg="#191918")

def validar_etiqueda():
    pass

def buscar_anfitrion(username):
    if not username:
        pass
    pass

def activar_anfitrion(username):
    if not username:
        pass
    pass

estilo = ttk.Style()
estilo.theme_use("clam")
estilo.configure("MiEstilo.TEntry",
    foreground="black",
    background="#191918",
    highlightcolor="white",
    highlightthickness=0,
    font=("Arial Unicode MS", 10))

frame_izq = tk.Frame(ventana, bg="#191918")
frame_izq.pack(fill="x")

titulo = tk.Label(frame_izq, text="EMPAREJAMIENTO DE TABLERO", font=("Arial Unicode MS", 15), bg="#191918", fg="white")
titulo.pack(side="top", pady=(20, 0))

boton_activar_anfitrion = tk.Button(frame_izq, text="Convertirme en Anfitrión", bg="#1f1f1f", bd=3)
boton_activar_anfitrion.configure(font=("Arial Unicode MS", 10), anchor="nw", fg="white")
boton_activar_anfitrion.pack(side="bottom", pady=(20, 0))

frame_der = tk.Frame(ventana, bg="#191918", relief="solid", bd=2)
frame_der.pack(pady=(20, 0))

anfitriones_activos = tk.Button(frame_der, text="Listar Anfitriones Activos", bg="#1f1f1f", bd=3)
anfitriones_activos.configure(font=("Arial Unicode MS", 10), anchor="nw", fg="white")
anfitriones_activos.grid(row=0, column=0, sticky="ew")

frame_listado = tk.Frame(frame_der, height=200, bg="#1f1f1f")
frame_listado.propagate(False)
frame_listado.grid(row=1, column=0, columnspan=2, sticky="ew")

borde_frame_listado = tk.Frame(frame_listado, bg="black", height=2) 
borde_frame_listado.pack(side="top", fill="x")


if __name__ == '__main__':
    ventana.mainloop()