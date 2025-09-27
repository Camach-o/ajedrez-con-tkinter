class Game():
    def __init__(self):
        # Game
        self.fen_historial = {}
        self.last_move = None
        self.halfmove = None
        self.fullmove = None
        self.en_passant = None
        self.castling = None
        self.turn = None
        self.team_winner = None

        # Clock
        self.time = None
        self.bonus = None

        # Panel
        self.movement_index = None