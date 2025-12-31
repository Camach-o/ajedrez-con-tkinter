    # def recibir_pieza(self, event, pieza):
    #     casilla = event.widget
    #     print(casilla.coordenadas)
    #     self.mostrar_marcador(pieza=pieza)
    #     pieza.pack_forget()
    #     pieza.ubicacion = casilla.coordenadas
    #     pieza.movimientos()
    #     pieza.pack(in_=casilla)
    #     #casilla.pieza = pieza


    # def mostrar_marcador(self, pieza):
    #     for m in pieza.movimientos((0, 8)):
    #         if self.tablero[m[0]][m[1]].estado_marcador:
    #             self.tablero[m[0]][m[1]].marcador.pack_forget()
    #             self.tablero[m[0]][m[1]].unbind('<Button-1>')
    #             self.tablero[m[0]][m[1]].estado_marcador = 0
    #         else:
    #             self.tablero[m[0]][m[1]].marcador.pack()
    #             self.tablero[m[0]][m[1]].bind('<Button-1>', lambda event:self.recibir_pieza(event, pieza))
    #             self.tablero[m[0]][m[1]].estado_marcador = 1



    # def mover_pieza(self, nueva_casilla):
    #     if nueva_casilla.pieza:
    #         nueva_casilla.pieza.destroy()
    #         nueva_casilla.pieza = self.pieza_seleccionada
    #         self.casilla_seleccionada.quitar_pieza()
    #         nueva_casilla.poner_pieza()
    #     else:
    #         nueva_casilla.pieza = self.pieza_seleccionada
    #         self.casilla_seleccionada.quitar_pieza()
    #         nueva_casilla.poner_pieza()


    #     if llamada == "pieza":
    #         if not self.casilla_seleccionada:
    #             return
    #         nueva_casilla = event.widget.pack_info().get('in')
    #     else:
    #         nueva_casilla = event.widget

    #     anterior_casilla = self.casilla_seleccionada

    #     if nueva_casilla.marcador:
    #         if not nueva_casilla.pieza:
    #             nueva_casilla.pieza = anterior_casilla.pieza
    #             anterior_casilla.quitar_pieza()
    #             nueva_casilla.poner_pieza()
    #         else:
    #             if nueva_casilla.pieza.color != anterior_casilla.pieza.color:
    #                 nueva_casilla.pieza.destroy()
    #                 nueva_casilla.pieza = anterior_casilla.pieza
    #                 anterior_casilla.quitar_pieza()
    #                 nueva_casilla.poner_pieza()

    #     self.quitar_marcadores(None)

#lista_piezas = [
        #     #Negras
        #     Torre(0, (0, 0)),
        #     Caballo(0, (0, 1)),
        #     Alfil(0, (0, 2)),
        #     Dama(0, (0, 3)),
        #     Rey(0, (0, 4)),
        #     Alfil(0, (0, 5)),
        #     Caballo(0, (0, 6)),
        #     Torre(0, (0, 7)),
        #     #Blancas
        #     Torre(1, (7, 0)),
        #     Caballo(1, (7, 1)),
        #     Alfil(1, (7, 2)),
        #     Dama(1, (7, 3)),
        #     Rey(1, (7, 4)),
        #     Alfil(1, (7, 5)),
        #     Caballo(1, (7, 6)),
        #     Torre(1, (7, 7))
        # ]

        # for pieza in lista_piezas:

        #     coord = pieza.ubicacion
        #     pieza.bind('<Button-1>', self.accion_pieza)
        #     pieza.pack(in_=self.tablero[coord[0]][coord[1]])
        #     self.tablero[coord[0]][coord[1]].pieza = pieza


# for casilla in self.tablero[1]:
        #     pieza = Peon(0, (casilla.coordenadas[0], casilla.coordenadas[1]))
        #     pieza.bind('<Button-1>', self.accion_pieza)
        #     casilla.pieza = pieza
        #     casilla.poner_pieza()

        # for casilla in self.tablero[6]:
        #     pieza = Peon(1, (casilla.coordenadas[0], casilla.coordenadas[1]))
        #     pieza.bind('<Button-1>', self.accion_pieza)
        #     casilla.pieza = pieza
        #     casilla.poner_pieza()

        # dama_blanca = PhotoImage(file="imagenes_piezas/reina-blanca.png")
        # dama_negra = PhotoImage(file="imagenes_piezas/rey-negro.png")
        

        # rey_blanco = PhotoImage(file="imagenes_piezas/rey-blanco.png")
        # rey_negro = Image.open("imagenes_piezas/rey-negro.png")
        # foto = ImageTk.PhotoImage(rey_negro)

        # lista_piezas = [
            #Negras
            # Torre(0, (0, 0)),
            # Caballo(0, (0, 1)),
            # Alfil(0, (0, 2)),
            # Dama(0, (0, 3)),
            # Rey(0, (0, 4)),
            # Alfil(0, (0, 5)),
            # Caballo(0, (0, 6)),
            # Torre(0, (0, 7)),
            # #Blancas
            # Torre(1, (7, 0)),
            # Caballo(1, (7, 1)),
            # Alfil(1, (7, 2)),
            # Dama(1, (7, 3)),
            #Rey(1, (7, 4)),
            # Alfil(1, (7, 5)),
            # Caballo(1, (7, 6)),
            # Torre(1, (7, 7))
        # ]

       
        # for pieza in lista_piezas:

        #     coord = pieza.ubicacion
        #     pieza.bind('<Button-1>', self.accion_pieza)
        #     self.tablero[coord[0]][coord[1]].pieza = pieza
        #     self.tablero[coord[0]][coord[1]].poner_pieza()
        #     pieza.configure(bg=self.tablero[coord[0]][coord[1]].color)
        #     self.ventana.update()


    # def accion_pieza(self, event):
    #     """Determina qué acción toma el evento desencadenado por la pieza seleccionada"""
    #     pieza = event.widget
    #     casilla = pieza.place_info()['in']

    #     # Si la pieza que llama la función tiene el color del turno
    #     if pieza.color == self.turno[0]:
    #         # Definirla como seleccionada y marcar sus movimientos
    #         self.pieza_seleccionada = pieza
    #         self.revisar_movimientos(pieza)
    #     else:
    #         # De haber una pieza seleccionada previamente a la llamada
    #         if self.pieza_seleccionada:
    #             # Verificar si la casilla de la pieza que acaba de ser seleccionada tiene un marcador (pieza)
    #             if casilla.marcador:
    #                 # De tener el marcador llama a mover pieza (se hace una captura)
    #                 self.mover_pieza(casilla)


    # def quitar_marcadores(self): # No modificar
    #     """Recorre el tablero para desactivar los marcadores de casilla"""

    #     for fila in self.tablero:
    #         for casilla in fila:
    #             if casilla.marcador:
    #                 casilla.desactivar_marcador()
    #     self.casilla_seleccionada = 0

    # def revisar_movimientos(self, pieza):
    #     """Activa o desactiva los marcadores en las casillas disponibles para mover la pieza seleccionada"""

    #     casilla = pieza.place_info()['in']   
    #     coord = casilla.coordenadas
    #     if self.casilla_seleccionada and casilla != self.casilla_seleccionada:
    #         self.quitar_marcadores()

    #     casilla.seleccion_activa = 1
    #     self.switch_marcador(coord)
        
    #     for direccion in pieza.movimientos:
    #         y, x = coord[0], coord[1]
    #         for _ in range(0, pieza.cantidad_movimientos):
    #             y, x = y + direccion[0], x + direccion[1]
    #             if y in range(0, LIMITE_TABLERO) and x in range(0, LIMITE_TABLERO):
    #                 if self.tablero[y][x].pieza and self.tablero[y][x].pieza.color == self.turno[0]:
    #                     break
    #                 if self.pieza_seleccionada.nombre == "Peon":
    #                     if direccion == pieza.movimientos[1] or direccion == pieza.movimientos[2]:
    #                         if not self.tablero[y][x].pieza:
    #                             break
    #                     elif self.tablero[y][x].pieza:
    #                         break

    #                 self.switch_marcador((y, x))

    #                 if self.tablero[y][x].pieza:
    #                     break



    # def switch_marcador(self, coord): # No modificar
    #     """Decide si marcar o desmarcar la casilla indicada
        
    #         Parámetros:
    #             coord: coordenadas casilla indicada
    #     """

    #     if not self.tablero[coord[0]][coord[1]].marcador:
    #         self.tablero[coord[0]][coord[1]].activar_marcador()
    #     else:
    #         self.tablero[coord[0]][coord[1]].desactivar_marcador()


    # def recibir_pieza(self, event):
    #     """Evento llamado por la casilla seleccionada para recibir la pieza seleccionada"""
    #     casilla = event.widget

    #     # De contar la casilla seleccionada con un marcador
    #     if casilla.marcador:
    #         # De no haber una pieza dentro de la casilla
    #         if not casilla.pieza:
    #             # Mueve la pieza seleccionada a la casilla que llama la función 
    #             self.mover_pieza(casilla)
    #         else: # de haber una dentro
    #             # Si la pieza dentro de la casilla es del color del turno
    #             if casilla.pieza.color == self.turno[0]:
    #                 # Cambia de pieza selecciona y marca los movimientos de la pieza dentro de la casilla seleccionada
    #                 self.revisar_movimientos(casilla.pieza)

    #             else: # de ser la pieza del color opuesto
    #                 # quita la pieza de la casilla seleccionada y mueve la pieza seleccionada a la casilla seleccionada # captura
    #                 self.mover_pieza(casilla)
    #     else:
    #         # de no contar contar con marcador "cambia el punto de mira" y borra los marcadores
    #         self.quitar_marcadores()
        
        

# class DamaNegra:
#     def __init__(self, canvas, y, x):
#         # Atributos de pieza
#         self.nombre = "D"
#         self.color = 0
#         self.cantidad_movimientos = 7
#         self.movimientos = [(-1, -1), (-1, 1), (1, 1), (1, -1), (-1, 0), (+1, 0), (0, -1), (0, +1)]

#         # Atributos de objeto gráfico
#         self.canvas = canvas
#         self.imagen = ImageTk.PhotoImage(Image.open("ruta"))
#         self.id_pieza = canvas.create_image(x, y, image=self.imagen)

# class TorreNegra:
#     def __init__(self, canvas, y, x):
#         # Atributos de pieza
#         self.nombre = "T"
#         self.color = 0
#         self.cantidad_movimientos = 7
#         self.movimientos = None

#         # Atributos de objeto gráfico
#         self.canvas = canvas
#         self.imagen = ImageTk.PhotoImage(Image.open("ruta"))
#         self.id_pieza = canvas.create_image(x, y, image=self.imagen)

# class AlfilNegro:
#     def __init__(self, canvas, y, x):
#         # Atributos de pieza
#         self.nombre = "A"
#         self.color = 0
#         self.cantidad_movimientos = 7
#         self.movimientos = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
        
#         # Atributos de objeto gráfico
#         self.canvas = canvas
#         self.imagen = ImageTk.PhotoImage(Image.open("ruta"))
#         self.id_pieza = canvas.create_image(x, y, image=self.imagen)

# class CaballoNegro:
#     def __init__(self, canvas, y, x):
#         # Atributos de pieza
#         self.nombre = "C"
#         self.color = 0
#         self.cantidad_movimientos = 1
#         self.movimientos = [(-1, -2), (-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2)]

#         # Atributos de objeto gráfico
#         self.canvas = canvas
#         self.imagen = ImageTk.PhotoImage(Image.open("ruta"))
#         self.id_pieza = canvas.create_image(x, y, image=self.imagen)

# class PeonNegro:
#     def __init__(self, canvas, y, x):
#         self.nombre = "P"
#         self.color = 0
#         self.primer_movimiento = True
#         self.cantidad_movimientos = 2
#         self.movimientos = self.definir_movimientos()

#         # Atributos de objeto gráfico
#         self.canvas = canvas
#         self.imagen = ImageTk.PhotoImage(Image.open("ruta"))
#         self.id_pieza = canvas.create_image(x, y, image=self.imagen)
        

#     def definir_movimientos(self):
#         movimientos = [[(1, 0), (1, 1), (1, -1)],
#                        [(-1, 0), (-1, -1), (-1, 1)]]

#         return movimientos[self.color]




    # def validacion_general(self, casilla):
    #     if casilla.pieza and casilla.pieza.color == self.turno[0]:
    #         return False
                           

    # def validacion_para_rey(self, casilla, direccion):
    #     if casilla.pieza.tipo == "P":
    #         if direccion == casilla.pieza.movimientos[1] or direccion == casilla.pieza.movimientos[2]:
    #             if not casilla.pieza:
    #                 return False
    #             elif casilla.pieza:
    #                 return False

    # def validacion_para_peon(self, casilla, direccion):
    #     if casilla.pieza.tipo == "R":
    #         if not self.casilla_valida_para_rey(casilla):
    #             return False
    #         elif direccion == (0, +2) or direccion == (0, -2):

    #             if casilla.pieza and casilla.pieza.color == self.turno[0]:
    #                 return False
    #             elif casilla.pieza and casilla.pieza.color == self.turno[0]:
    #                 return False
    #             elif casilla.pieza and casilla.pieza.color == self.turno[0]:
    #                 return False


# # ver fila y contar las piezas iguales
#         for square in self.board[oldrow]:
#             if square.piece:
#                 if square.piece.type == piece_moved:
#                     if square.piece.color != self.turn[0]:
#                         there_is_other_same_piece_in_row += 1

        
#         # ver columna y contar las piezas iguales
#         for row_indx, _ in enumerate(self.board):
#             if self.board[row_indx][oldcolumn].piece:
#                 if self.board[row_indx][oldcolumn].piece.type == piece_moved:
#                     if self.board[row_indx][oldcolumn].piece.color != self.turn[0]:
#                         there_is_other_same_piece_in_column += 1

#         if there_is_other_same_piece_in_row:
#             ambiguity_indicator = self.get_square_position(row=oldrow)
#         if there_is_other_same_piece_in_column:
#             ambiguity_indicator = self.get_square_position(column=oldcolumn)
#         if there_is_other_same_piece_in_row and there_is_other_same_piece_in_column:
#             ambiguity_indicator = self.get_square_position(row=oldrow, column=oldcolumn)



# old = self.ob_board.get_position_of_square(self.selected_square)
# new = self.ob_board.get_position_of_square(square_touched)
# last_move = f"{old}{new}"
    
# self.start_process_to_move(self.selected_square, square_touched)
# self.stockfish.make_moves_from_current_position([last_move])

# print(f"Movimiento jugador: {last_move}", "\n", self.stockfish.get_board_visual())

# last_move = self.stockfish.get_best_move()
# self.stockfish.make_moves_from_current_position([last_move])

# print(f"Movimiento de stockfish: {last_move}", "\n", self.stockfish.get_board_visual())
# self.recive_movement(last_move)

# self.stockfish.make_moves_from_current_position([last_move])
# time.sleep(5)


# print(f"Movimiento jugador: {last_move}", "\n", self.stockfish.get_board_visual())

# last_move = self.stockfish.get_best_move()
# self.stockfish.make_moves_from_current_position([last_move])

# print(f"Movimiento de stockfish: {last_move}", "\n", self.stockfish.get_board_visual())
# self.recive_movement(last_move)


# def myfunction():
#     print("hello")

# def function_to_call_the_thread():
#     task = threading.Thread(target=myfunction)
#     task.start()

# # Programa
# function_to_call_the_thread()

       #### Caso de estudio

        # colocation = colocation.split("/")
        # print(colocation)

        # if self.board_view[0] == 0:
        #     colocation = colocation.reverse()

        # for row, r_letters in enumerate(colocation):
        #     saltos_pendientes = 0
        #     for column, c_letter in enumerate(r_letters):
        #         if saltos_pendientes > 0:
        #             saltos_pendientes -= 1
        #             continue

        #         if c_letter.upper() in "RNBQKP":
        #             color = 1 if c_letter.isupper() else 0
        #             self.ob_board.put_piece(self.board[row][column], 
        #                                     type=c_letter.upper(), 
        #                                     color=color,
        #                                     board_view=board_view)
        #         elif c_letter in "12345678":
        #             v = int(c_letter)
        #             saltos_pendientes = v-1

        # if self.board_view[0] == 0:
        #     colocation = colocation.split("/")
        #     colocation.reverse()
        #     for row in colocation:
        #         if len(row) == 1:
        #             continue
        #         row = row.split()
        #         row.reverse()
        #         row = "".join(row)
        #     print(colocation)
        #     # colocation = "/".join(colocation)



import threading
import queue
import time

# 1. Cola para enviar mensajes al bot sin bloquear la UI
cola_entrada_bot = queue.Queue()

def logica_del_chatbot():
    """Este hilo vive para procesar lo que el usuario escribe."""
    while True:
        mensaje_usuario = cola_entrada_bot.get() # Espera a que llegue un mensaje
        if mensaje_usuario == "SALIR": 
            break
            
        # Simulación de "pensamiento" (petición a API, procesamiento, etc.)
        print(f"\n(Bot procesando: '{mensaje_usuario}'...)")
        time.sleep(3) # El bot tarda 3 segundos
        
        print(f"\n[BOT]: Mi respuesta a '{mensaje_usuario}' es: 42.")
        cola_entrada_bot.task_done()

# --- INICIO DEL PROGRAMA ---

# Iniciamos el hilo del bot una sola vez al arrancar
hilo_bot = threading.Thread(target=logica_del_chatbot, daemon=True)
hilo_bot.start()

print("--- Chatbot Activo (Escribe algo o 'exit') ---")

# Bucle de la UI (Hilo Principal)
while True:
    # Esta parte nunca se detiene, el usuario siempre puede escribir
    opcion = input("Tú: ") 
    
    if opcion.lower() == 'exit':
        cola_entrada_bot.put("SALIR")
        break
    
    # En lugar de procesar aquí, "lanzamos" el mensaje a la cola y seguimos
    cola_entrada_bot.put(opcion)
    print("Sigo disponible para que hagas otras cosas mientras el bot piensa...")

print("Cerrando programa.")