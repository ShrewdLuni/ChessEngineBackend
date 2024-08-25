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
        data = json.loads(text_data)
        action = data.get('action')

        action_map = {
            'generate_random_number': self.generate_random_number,
            'get_chess_info': self.get_chess_info
        }

        action_func = action_map.get(action)
        if action_func:
            action_func()
        else:
            self.send(text_data=json.dumps({'error': 'Unknown action'}))

    def generate_random_number(self):
        random_number = random.randint(1, 100)  # Generate a random number between 1 and 100
        self.send(text_data=json.dumps({
            'random_number': random_number
        }))

    def get_chess_info(self):
        brd = Board()
        pmd = PrecomputedMoveData()
        mg = MoveGenerator(brd, pmd)
        brd.FENtoBoard("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

        mg.GenerateLegalMoves()
        moves_as_dicts = [move.__dict__ for move in mg.moves]
        moves_json = json.dumps(moves_as_dicts)
        self.send(text_data=moves_json)
