from stockfish import Stockfish
import time


# class StockfishEngine():
#     def __init__(self):
#         self.path = "stockfish_module/stockfish/stockfish-windows-x86-64.exe"

print("\n\n")


try:
    stockfish = Stockfish(path="stockfish_module/stockfish/stockfish-windows-x86-64.exe")  # Reemplaza con tu ruta
    kill = False

    # Establecer una posición de ejemplo
    stockfish.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    moves = []
    while True:

        # moves.append(stockfish.get_best_move())
        movem = [stockfish.get_best_move()]

        print("\n", movem, "\n")
        stockfish.make_moves_from_current_position(movem)
        print(stockfish.get_board_visual(), "\n\n")
        # print(moves[-1])
        time.sleep(2)

        if len(moves) > 30:
            break




except FileNotFoundError:
    print("¡Error! No se encontró el ejecutable de Stockfish.")
except Exception as e:
    print(f"Ocurrió un error: {e}")
finally:
    pass