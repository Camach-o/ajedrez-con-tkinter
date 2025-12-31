# import tkinter as tk

# def mostrar_listbox(event=None):
#     listbox.place(x=entry.winfo_x(), y=entry.winfo_y() + entry.winfo_height())
#     actualizar_resultados()

# def ocultar_listbox(event=None):
#     listbox.place_forget()

# def actualizar_resultados(event=None):
#     texto = entry.get().lower()
#     listbox.delete(0, tk.END)
#     for elemento in elementos:
#         if texto in elemento.lower():
#             listbox.insert(tk.END, elemento)

# def seleccionar_elemento(event):
#     seleccion = listbox.get(listbox.curselection())
#     entry.delete(0, tk.END)
#     entry.insert(0, seleccion)
#     ocultar_listbox()

# ventana = tk.Tk()
# ventana.geometry("300x200")

# elementos = ["Perro", "Gato", "Ratón", "Pájaro", "Pez", "Caballo", "Conejo"]

# entry = tk.Entry(ventana, width=30)
# entry.pack(pady=10)
# entry.bind("<KeyRelease>", mostrar_listbox)
# entry.bind("<FocusIn>", mostrar_listbox)
# entry.bind("<FocusOut>", ocultar_listbox)

# listbox = tk.Listbox(ventana, width=30, height=5)
# listbox.bind("<<ListboxSelect>>", seleccionar_elemento)

# ventana.mainloop()


# import tkinter as tk

# ventana = tk.Tk()
# radio = tk.Radiobutton(
#     ventana,
#     text="Opción",
#     fg="blue",         # color del texto y círculo
#     selectcolor="red", # color de fondo del círculo seleccionado
#     bg="white"         # color de fondo del widget
# )
# radio.pack()
# ventana.mainloop()
# import tkinter as tk

# def quitar_foco():
#     boton.focus_set()  # El foco pasa al botón

# ventana = tk.Tk()
# listbox = tk.Listbox(ventana)
# listbox.pack()

# preset_seconds = ["1", "2", "3", "5", "10"]
# for second in preset_seconds:
#     listbox.insert(tk.END, second)

# boton = tk.Button(ventana, text="Quitar foco al Listbox", command=quitar_foco)
# boton.pack()

# ventana.mainloop()

# from itertools import islice

# texto = "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2"

# hola = list([v for v in islice(texto.split(), 3)])  # toma las primeras 3 palabras

# print(hola)
# import threading
# import time

# def tarea_a_ejecutar(nombre, duracion):
#     """Función que será ejecutada por el hilo."""
#     print(f"Hilo {nombre}: Empezando la tarea.")
#     time.sleep(duracion) # Simula una tarea larga (ej. una petición web)
#     print(f"Hilo {nombre}: Tarea finalizada.")

# # --- Aplicación ---

# # 1. Crear los objetos Thread
# hilo1 = threading.Thread(target=tarea_a_ejecutar, args=("H1", 2))
# hilo2 = threading.Thread(target=tarea_a_ejecutar, args=("H2", 3))

# # 2. Iniciar la ejecución de los hilos
# hilo1.start()
# hilo2.start()

# # 3. Bloquear el programa principal hasta que los hilos terminen (opcional)
# hilo1.join()
# hilo2.join()

# print("Programa principal terminado.")

# class OtraClase():
    
#     def funcion(argumentos):
#         pass

# class MyClase():
#     def __init__(self):
        
#         self.otra_clase = OtraClase()

#     def tarea(self):
#         hilo =  threading.Thread(target=self.otra_clase.funcion("argumentos"), args=("H1", 2))

#         # otras tareas que tiene que hacer MyClase


# hola = "Qkq"

# if "K" in hola:
#     print("!")

# def first_function(_):
#     # Code
#     pass

# def second_function(_):
#     # Code

#     # Call first_function
#     # Wait a value

#     # Code
#     pass

# path_capture_img = "contenido_grafico/images_highlight/capture.png"
# capture_img = ImageTk.PhotoImage(Image.open(self.path_capture_img))

# import tkinter as tk
# from tkinter import messagebox

# def funcion_principal():
#     print("Iniciando flujo...")
#     # ... operaciones iniciales ...
#     label.config(text="Procesando parte 1...")
    
#     # 1. Creamos una variable de control
#     var_seleccion = tk.StringVar(value="esperando")

#     # 2. Mostramos el "menú" (en este caso un frame o botones)
#     # Aquí simulamos que aparece un menú de selección
#     menu_flotante = tk.Frame(root, bd=2, relief="raised", bg="lightgrey")
#     menu_flotante.place(x=100, y=100)
    
#     tk.Label(menu_flotante, text="Selecciona una opción:").pack()
    
#     def seleccionar(opcion):
#         var_seleccion.set(opcion) # Esto liberará el wait_variable
#         menu_flotante.destroy()   # Cerramos el menú

#     tk.Button(menu_flotante, text="Opción A", command=lambda: seleccionar("A")).pack()
#     tk.Button(menu_flotante, text="Opción B", command=lambda: seleccionar("B")).pack()

#     print("Función pausada, esperando al usuario...")
    
#     # 3. LA MAGIA: El programa se detiene aquí, pero la GUI sigue viva
#     root.wait_variable(var_seleccion)
    
#     # 4. Al cambiar la variable, la función continúa
#     resultado = var_seleccion.get()
#     print(f"Función reanudada. El usuario eligió: {resultado}")
#     label.config(text=f"Continuando con selección: {resultado}")
    
#     # ... el resto de tu lógica ...

# # Configuración básica de Tkinter
# root = tk.Tk()
# root.geometry("400x300")
# label = tk.Label(root, text="Presiona el botón para iniciar")
# label.pack(pady=20)

# btn_inicio = tk.Button(root, text="Iniciar Proceso", command=funcion_principal)
# btn_inicio.pack()

# root.mainloop()
# print("olha")

def player_thread(self, player_socket):

        # print('se activó un jugador')
        while True:
            try:
                data = player_socket.recv(1024).decode()
                if not data:
                    continue
                print(data, type(data))
                for player in self.connected_players:
                    if player != player_socket:
                        interaction = data.split()
                        interaction_type, content = interaction
                        if interaction_type == 'movement':
                            self.get_new_movement(content)
                        elif interaction_type == 'message':
                            self.get_new_message(content)
                        elif interaction_type == 'give_me_settings':
                            command = ['reciv_settings', 'configuración']
                            command = " ".join(command)
                            player_socket.sendall(command.encode())
                            print('ya se envió los settings')
                        elif interaction_type == 'reciv_settings':
                            print(content)
            except socket.timeout:
                print("Error: Se agotó el tiempo de espera.")
                continue
            except Exception as e:
                print(f"Ocurrió un error inesperado en la recepción de la interacción: {e}")
                break
        player_socket.close()
        self.connected_players.remove(player_socket)