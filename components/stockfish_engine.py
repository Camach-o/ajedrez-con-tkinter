# from stockfish import Stockfish

# # Reemplaza con la ruta a tu ejecutable de Stockfish
# stockfish_path = "stockfish_module/stockfish/stockfish-windows-x86-64.exe"
# try:
#     stockfish = Stockfish(path=stockfish_path)
# except FileNotFoundError:
#     print(f"Error: No se encontró el ejecutable de Stockfish en la ruta: {stockfish_path}")
#     exit()

# # Configura la posición inicial del tablero (FEN)
# stockfish.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")

# # Obtén el mejor movimiento
# best_move = stockfish.get_best_move()
# print("Mejor movimiento:", best_move)

from stockfish import Stockfish

try:
    stockfish = Stockfish(path="stockfish_module/stockfish/stockfish-windows-x86-64.exe")  # Reemplaza con tu ruta

    # Establecer una posición de ejemplo
    stockfish.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq e3 0 1")
    
    print(stockfish.get_board_visual())

    stockfish.make_moves_from_current_position()

    for i in dir(stockfish):
        print(i)

    # print(stockfish.is_move_correct("asd"))

    # Casilla de la pieza que nos interesa (ejemplo: el peón en e4)
    # pieza_casilla = "e4"

    # Obtener todos los movimientos legales
    # todos_los_movimientos = stockfish.get_legal_moves()


except FileNotFoundError:
    print("¡Error! No se encontró el ejecutable de Stockfish.")
except Exception as e:
    print(f"Ocurrió un error: {e}")
finally:
    pass


# # # Obtén la evaluación de la posición
# # evaluation = stockfish.get_evaluation()
# # print("Evaluación:", evaluation)

# # # Cambiar la profundidad de búsqueda de Stockfish (más profundidad = análisis más fuerte, más tiempo)
# # stockfish.set_depth(15)

# # # Obtener la posición de un tablero en formato visual (ASCII)
# # print("/nTablero actual:")
# # print(stockfish.get_board_visual())

# # Obtener los N mejores movimientos para la posición actual
# top_moves = stockfish.get_top_moves(3)
# print("/nLos 3 mejores movimientos:", top_moves)

# # # Obtener estadísticas de probabilidad de victoria, empate o derrota (WDL)
# # wdl_stats = stockfish.get_wdl_stats()
# # print("/nEstadísticas WDL:", wdl_stats)

# # # Puedes realizar movimientos en el motor Stockfish
# # stockfish.make_moves_from_current_position(["e2e4", "e7e5"])
# # print("/nTablero después de e4 e5:")
# # print(stockfish.get_board_visual())

# # # Deshacer el último movimiento
# # stockfish.undo_last_move()
# # print("/nTablero después de deshacer:")
# # print(stockfish.get_board_visual())

# # Cierra la conexión con Stockfish (opcional, se cierra automáticamente al finalizar el script)
# # stockfish.quit()
