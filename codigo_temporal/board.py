from tkinter import *
if __name__ != "__main__":
    from components.pieces import *
else:
    from piezas import *
from PIL import Image, ImageTk

LIMITE_TABLERO = 8
TEMA_PREDETERMINADO_TABLERO = ("#bb935b", "#592f0a") # Blanco | Negro

class Casilla(Canvas):
    def __init__(self, master, coord, **kwargs):
        super().__init__(master, **kwargs)
        self.pieza = None
        self.color = None
        self.coordenadas = coord
        self.marcador = False
        self.seleccion_activa = 0

        # Marcadores 
        self.ruta_img_captura = "C:\\Users\\Jesus\\Downloads\\imagenes_prueba\\pieza_captura.png"
        self.img_captura = ImageTk.PhotoImage(Image.open(self.ruta_img_captura))
        self.marcador_captura = self.create_image(40, 40, image=self.img_captura, state="hidden")          
        
        self.ruta_img_libre = "C:\\Users\\Jesus\\Downloads\\imagenes_prueba\\casilla_libre.png"
        self.img_libre = ImageTk.PhotoImage(Image.open(self.ruta_img_libre))
        self.marcador_casilla_libre = self.create_image(40, 40, image=self.img_libre, state="hidden")

        self.ruta_img_seleccionada = "C:\\Users\\Jesus\\Downloads\\imagenes_prueba\\casilla_seleccionada.png"
        self.img_seleccionada = ImageTk.PhotoImage(Image.open(self.ruta_img_seleccionada))
        self.marcador_casilla_seleccionada = self.create_image(40, 40, image=self.img_seleccionada, state="hidden")

    def obtener_fila(self, orientacion_filas):
        return orientacion_filas[self.coordenadas[0]]

    def obtener_columna(self, orientacion_columnas):
        return orientacion_columnas[self.coordenadas[1]]

    def activar_marcador(self):
        """Selecciona y activa el marcador correspondiente al estado de la casilla"""

        if self.seleccion_activa:
            self.itemconfigure(self.marcador_casilla_seleccionada, state="normal")
        elif self.pieza:
            self.itemconfigure(self.marcador_captura, state="normal")
        else:
            self.itemconfigure(self.marcador_casilla_libre, state="normal")
        self.marcador = True

    def desactivar_marcador(self):
        """Desactiva el marcador de la casilla"""       
        self.itemconfigure(self.marcador_casilla_seleccionada, state="hidden")
        self.itemconfigure(self.marcador_captura, state="hidden")
        self.itemconfigure(self.marcador_casilla_libre, state="hidden")
        self.marcador = 0
        self.seleccion_activa = 0

    def cambiar_pieza(self, atributos):
        if self.pieza:
            self.delete(self.pieza.id_pieza)
            self.pieza = False
        self.pieza = Pieza(self, y=40, x=40, color=atributos['color'], tipo_pieza=atributos['tipo'], primer_movimiento=atributos['primer_movimiento'])
        
class Board:
    def __init__(self, contenedor, vista):
        # Ventana
        self.contenedor_tablero = contenedor
        self.vista = vista

        # Tablero
        self.tablero = [[0 for _ in range(0, LIMITE_TABLERO)] for _ in range(0, LIMITE_TABLERO)]
        self.tema = [TEMA_PREDETERMINADO_TABLERO[0], TEMA_PREDETERMINADO_TABLERO[1]]
        self.vista_tablero = 1 # 1 Para Blancas | 0 Para Negras
        self.casilla_seleccionada = None
        self.pieza_seleccionada = None
        self.turno = [1, 0]
        self.jaque = 0
        self.casillas_del_jaque = []
        self.rey = None

        # Identificadores de coordenadas
        self.numeros_filas = ["8", "7", "6", "5", "4", "3", "2", "1"]
        self.identificadores_filas = []
        self.letras_columnas = ["a", "b", "c", "d", "e", "f", "g", "h"]
        self.identificadores_columnas = []

    def crear_casillas(self): # No modificar
        """Crear las casillas del tablero"""
        for fila in range(0, LIMITE_TABLERO):
            for columna in range(0, LIMITE_TABLERO):
                casilla = Casilla(self.contenedor_tablero, coord=(fila, columna), width=80, height=80, highlightthickness=0)
                casilla.bind('<Button-1>', self.accion_click)
                casilla.grid(row=fila, column=columna)
                casilla.pack_propagate(False)
                self.tablero[fila][columna] = casilla

    def crear_identificadores(self): # No modificar
        """Crea labels que identifican las filas y columnas del tablero"""

        for fila, numero in enumerate(self.numeros_filas):
            num = self.tablero[fila][0].create_text(12, 14, text=numero, font=("Arial Black", 16))
            self.identificadores_filas.append(num)

        for columna, numero in enumerate(self.letras_columnas):
            let = self.tablero[7][columna].create_text(70, 68, text=numero, font=("Arial Black", 16))
            self.identificadores_columnas.append(let)

    def colocar_tema(self): # No modificar
        """Le coloca el tema a las casillas e identificadores del tablero"""
        for fila in self.tablero:
            for casilla in fila:
                casilla.configure(background=self.tema[0])
                casilla.color=self.tema[0]
                self.tema.reverse()
            self.tema.reverse()

        for fila, identificador in enumerate(self.identificadores_filas):
            self.tablero[fila][0].itemconfigure(identificador, fill=self.tema[0] if self.tema[0] != self.tablero[fila][0].color else self.tema[1])

        for columna, identificador in enumerate(self.identificadores_columnas):
            self.tablero[7][columna].itemconfigure(identificador, fill=self.tema[0] if self.tema[0] != self.tablero[7][columna].color else self.tema[1])

    def crear_piezas(self): # Modiicar
        """Crea las piezas y las coloca en sus posiciones inciales dentro del tablero"""
        for grupo_pieza in ({"fila": 0, "color": 0}, {"fila": 7, "color": 1}):
            for columna, tipo in enumerate(("T", "C", "A", "D", "R", "A", "C", "T")):
                pieza = Pieza(self.tablero[grupo_pieza['fila']][columna], y=40, x=40, color=grupo_pieza['color'], tipo_pieza=tipo)
                self.tablero[grupo_pieza['fila']][columna].pieza = pieza

        for casilla in self.tablero[1]:
            pieza = Pieza(casilla, y=40, x=40, color=0, tipo_pieza="P")
            casilla.pieza = pieza

        for casilla in self.tablero[6]:
            pieza = Pieza(casilla, y=40, x=40, color=1, tipo_pieza="P")
            casilla.pieza = pieza

    def __create_initial_position(self):
        pass

    ################## Mecanicas de movimiento #####################

    def accion_click(self, event): # Revisar
        """Determina qué acción toma el evento desencadenado por la casilla seleccionada"""

        casilla = event.widget
        if casilla != self.casilla_seleccionada:
            if casilla.pieza: # Modificar
                if casilla.pieza.color == self.turno[0]:
                    if self.casilla_seleccionada:
                        self.desactivar_marcadores()
                    self.casilla_seleccionada = casilla
                    self.casilla_seleccionada.seleccion_activa = True
                    self.activar_marcadores()   
                else:
                    if casilla.marcador and self.casilla_seleccionada:
                        self.mover_pieza(casilla)
                    self.desactivar_marcadores()
            else:
                if casilla.marcador and self.casilla_seleccionada:
                    self.mover_pieza(casilla)
                self.desactivar_marcadores()
        else:
            self.desactivar_marcadores()

    def activar_marcadores(self): # Revisar
        """ Activa los marcadores de casilla correspondientes a la pieza seleccionada."""
        
        self.casilla_seleccionada.activar_marcador()
        for direccion in self.casilla_seleccionada.pieza.movimientos:
            y, x = self.casilla_seleccionada.coordenadas[0], self.casilla_seleccionada.coordenadas[1]
            for _ in range(0, self.casilla_seleccionada.pieza.cant_movimientos):
                y, x = y + direccion[0], x + direccion[1]
                if y in range(0, LIMITE_TABLERO) and x in range(0, LIMITE_TABLERO):
                    if self.marcador_valido(self.tablero[y][x]):
                        self.tablero[y][x].activar_marcador()
                    if self.tablero[y][x].pieza:
                        break

    def desactivar_marcadores(self): # Revisar
        """ Recorre el tablero para desactivar los marcadores de casilla activos."""

        for fila in self.tablero:
            for casilla in fila:
                if casilla.marcador:
                    casilla.desactivar_marcador()
        if self.casilla_seleccionada:                    
            self.casilla_seleccionada.seleccion_activa = False
            self.casilla_seleccionada = 0

    ################## Mecanicas de movimiento #####################







    def marcador_valido(self, cll_validar): # Revisar
        """ Revisa que se cumplan las condiciones para activar el marcador de la casilla 
        
            Parámetros:
                - cll_validar: casilla que será marcada por la que se llama a la función
        """

        if self.casilla_seleccionada.pieza.tipo == "R":
            return self.casilla_segura(cll_validar)     
        else:
            if self.jaque:
                if self.jaque == 1:
                    return True if not self.casilla_seleccionada.pieza.clavada and cll_validar in self.casillas_del_jaque else False               
                elif self.jaque == 2:
                    return False
            else:
                if self.casilla_seleccionada.pieza.clavada:
                    return True if cll_validar in self.casillas_disponible_para_pieza_clavada() else False
                else:
                    if cll_validar.pieza:
                        return True if cll_validar.pieza.color != self.turno[0] and cll_validar.pieza.tipo != "R" else False                  
                    else:
                        return True

    def casilla_segura(self, casilla): # Revisar

        direcciones = {"lineas": [(-1, 0), (+1, 0), (0, -1), (0, +1)], "diagonales": [(-1, -1), (-1, 1), (1, 1), (1, -1)], "eles": [(-1, -2), (-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2)]}

        for tipo_movimiento, direcciones in direcciones.items():
            if tipo_movimiento == "lineas":
                piezas = ["D", "T"]
                cant_movimientos = 7
            
            elif tipo_movimiento == "diagonales":
                piezas = ["D", "A"]
                cant_movimientos = 7

            elif tipo_movimiento == "eles":
                piezas = ["C"]
                cant_movimientos = 1

            for direccion in direcciones:
                y, x = casilla.coordenadas[0], casilla.coordenadas[1]
                for _ in range(0, cant_movimientos):
                    y, x = y + direccion[0], x + direccion[1]
                    if y in range(0, LIMITE_TABLERO) and x in range(0, LIMITE_TABLERO):
                        if self.tablero[y][x].pieza:

                            if self.tablero[y][x].pieza.tipo == "R" and self.tablero[y][x].pieza.color == self.turno[0]:
                                continue

                            elif self.tablero[y][x].pieza.color == self.turno[0]:
                                break

                            elif self.tablero[y][x].pieza.color != self.turno[0]:
                                if self.tablero[y][x].pieza.tipo in piezas:
                                    return False
                                else:
                                    break

        return True

    def casillas_disponibles_para_pieza_clavada(self): # Revisar

        pass

        #return casillas_disponibles

    def guardar_casillas_del_jaque(self, direction, pieza_atack, rey, cant): # Revisar
        y, x = rey.coordenadas[0], rey.coordenadas[1]
        for _ in range(0, cant):
            y, x = y + direction[0], x + direction[1]
            if y in range(0, LIMITE_TABLERO) and x in range(0, LIMITE_TABLERO):
                self.casillas_del_jaque.append(self.tablero[y][x])
                if pieza_atack == self.tablero[y][x]:
                    return

    def mover_pieza(self, nueva_casilla): # Revisar
        """ Mueve la pieza actualmente seleccionada a la casilla indicada.
        
            Parámetros:
                - nueva_casilla: casilla indicada donde colocar la pieza a mover
        """


        self.jaque = 0
        self.casillas_del_jaque = []
        

        if self.casilla_seleccionada.pieza.tipo in ("P", "R", "T"):
            self.casilla_seleccionada.pieza.primer_movimiento = False

        atts_pieza_a_mover = self.casilla_seleccionada.pieza.atributos()
        nueva_casilla.cambiar_pieza(atts_pieza_a_mover)
        self.casilla_seleccionada.delete(self.casilla_seleccionada.pieza.id_pieza)
        self.casilla_seleccionada.pieza = False
        self.cambiar_turno()

    def revisar_jaques(self): # Revisar
        """ Revisa si el rey del turno está en jaque.
        
            Retorna:
                - tipo_jaque: indicador de tipo de jaque, si normal, doble o mate
        """

        self.casilla_atacada(self.rey)
        if self.jaque:
            print(f"jaque, {self.jaque}")

    def encontrar_rey(self): # Revisar
        for fila in range(0, LIMITE_TABLERO):
            for columna in range(0, LIMITE_TABLERO):
                if self.tablero[fila][columna].pieza and self.tablero[fila][columna].pieza.tipo == "R":
                    if self.tablero[fila][columna].pieza.color == self.turno[0]:
                        self.rey = self.tablero[fila][columna]

    def cambiar_turno(self): # Revisar
        self.turno.reverse()
        self.encontrar_rey()
        self.revisar_jaques()

    def piezas_pruebas(self): 
        """ Inserta en el tablero piezas para provar los mecanismos del juego."""
        pieza = Pieza(self.tablero[7][4], y=40, x=43, color=1, tipo_pieza="R")
        self.tablero[7][4].pieza = pieza

        pieza = Pieza(self.tablero[3][2], y=40, x=43, color=0, tipo_pieza="R")
        self.tablero[3][2].pieza = pieza

        pieza = Pieza(self.tablero[0][5], y=40, x=43, color=0, tipo_pieza="D")
        self.tablero[0][5].pieza = pieza

        pieza = Pieza(self.tablero[0][3], y=40, x=43, color=0, tipo_pieza="A")
        self.tablero[0][3].pieza = pieza

        pieza = Pieza(self.tablero[0][4], y=40, x=43, color=1, tipo_pieza="D")
        self.tablero[0][4].pieza = pieza

    def start_board(self):
        """Llama a las funciones que crean la interfaz gráfica y objetos del tablero"""
        self.crear_casillas()
        self.crear_identificadores()
        self.crear_piezas()
        self.colocar_tema()