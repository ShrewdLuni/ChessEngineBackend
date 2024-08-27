import json
import random
from channels.generic.websocket import WebsocketConsumer

from ChessEngine.board import Board
from ChessEngine.move_generator import MoveGenerator
from ChessEngine.precomputed_move_data import PrecomputedMoveData

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
        random_number = random.randint(1, 100)
        self.send(text_data=json.dumps({
            'action': 'generate_random_number',
            'random_number': random_number
        }))

    def get_chess_info(self):
        brd = Board()
        pmd = PrecomputedMoveData()
        mg = MoveGenerator(brd, pmd)
        brd.fen_to_board("rnbqkbnr/pppppppp/8/8/8/8/8/RNBQKBNR w KQkq - 0 1")

        mg.generate_legal_moves()

        moves_as_dicts = [move.__dict__ for move in mg.moves]
        self.send(text_data=json.dumps({
            'action': 'get_chess_info',
            'moves': moves_as_dicts
        }))

