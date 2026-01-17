# Juego de Ajedrez

![Image Alt](https://github.com/Camach-o/ajedrez-con-tkinter/blob/d120273d53cbb67b5a3da4184b65a8b130ab1d0a/visual_reference.png)

## Descripción

Es un juego de ajedrez creado en Python con una interfaz gráfica elaborada con Tkinter.  Diseñado para satisfacer toda la lógica de una partida de ajedrez: enroques, peón al paso, coronación, etc. También cumple con las reglas de las tablas como 50 movimientos, triple repetición, material insuficiente y ahogado.

Además del tablero, he implementado varios componentes y funciones al programa para brindar una mejor experiencia al jugador. Entre estos tenemos el motor de Stockfish, un menú para cambiar la dificultad de Stockfish, un reloj, un visor de movimientos, un control para desplazarse entre las jugadas de la partida, un chat para partidas conectadas y un menú para personalizar el tema del tablero. Se permite modificar características de la partida como la posición por notación FEN; el bando que empieza, si blancas o negras; el estado del reloj, activado o desactivado; los minutos y bonus de incremento del reloj; el modo de juego, solo, conectado (se conecta el tablero con el de otro jugador activo en la misma red) o contra Stockfish.

## Razón del proyecto

Quise combinar dos actividades que me fascinan, programar y jugar al ajedrez. Inicié por el reto personal de poder crear un tablero de ajedrez aplicando toda la lógica que tiene este juego, aprendiendo a explicar y/o traducir cómo se puede jugar al ajedrez paso a paso. Determiné en hacer este proyecto para afinar los conocimientos que había adquirido independientemente sobre programación, con intención de convertirlo en el primer programa completo que pueda presentar.

## Pasos para usar

### Dependencias

- OS Recomendado: Windows
- Lenguaje: Python
- Librerías: Pillow, stockfish

### Ejecución

Abrir y ejecutar el archivo main.py

### Posibles errores

- Si entras en el menú de dificultad y cambias el ELO de Stockfish mientras este está moviendo no tendrá efecto el cambio. Esto debido a que puede bloquear el movimiento de Stockfish. Es necesario volver a hacer el cambio cuando sea tu turno para que se efectue.

- El menú de emparejamiento cambia cuando estás conectado a una partida. En este caso muestra la opción para desconectarse. Pasa que luego de desconectarte, este menú no se cierra, por lo que todavía no se cambiará al modo conectarse si no se presiona el botón de cerrar. Si no se ha cerrado y se vuelve a presionar el botón para desconetarse esto genera un error ya que el servidor ya habría sido cerrado.

- Stockfish puede sentirse monótono ya que no cuenta con un catálogo de aperturas y solo se modifica el ELO, otras configuraciones del motor no se tocan.

## Licencia

GNU General Public License version 3 (GPL v3)






