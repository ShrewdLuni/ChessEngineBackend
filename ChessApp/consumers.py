import json
import random
from channels.generic.websocket import WebsocketConsumer

from ChessEngine.board import Board
from ChessEngine.moveGenerator import MoveGenerator
from ChessEngine.precomputedMoveData import PrecomputedMoveData

class MyConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        print(1)
        brd = Board()
        pmd = PrecomputedMoveData()
        mg = MoveGenerator(brd, pmd)
        brd.FENtoBoard("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

        mg.GenerateLegalMoves()
        moves_as_dicts = [move.__dict__ for move in mg.moves]
        moves_json = json.dumps(moves_as_dicts)
        self.send(text_data=moves_json)
