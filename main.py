from fastapi import FastAPI
from ChessEngine import Engine

app = FastAPI()

@app.get("/engine/getLegalMoves")
def engine_get_legal_moves(FEN: str):
    engine = Engine()
    print(engine)
    engine.set_position(FEN)
    moves = engine.get_legal_moves()
    for move in moves:
        start = "abcdefgh"[move.get_starting_square() % 8] + str(8 - (move.get_starting_square() // 8))
        target = "abcdefgh"[move.get_target_square() % 8] + str(8 - (move.get_target_square() // 8))
        print(start, target)
    return moves

@app.get("/engine/getBestMove")
def engine_make_move(FEN: str):
    engine = Engine()
    engine.set_position(FEN)
    best_move = engine.get_best_move()
    return best_move
