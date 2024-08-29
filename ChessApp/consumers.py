import json
import random
from channels.generic.websocket import WebsocketConsumer

from ChessEngine.board import Board
from ChessEngine.move_generator import MoveGenerator
from ChessEngine.precomputed_move_data import PrecomputedMoveData
from ChessEngine.engine import Engine

class MyConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.engine = Engine()

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        action_map = {
            'engine_make_move': lambda: self.engine_make_move(data.get('move'))
        }
        action_func = action_map.get(action)
        if action_func:
            action_func()
        else:
            self.send(text_data=json.dumps({'error': 'Unknown action'}))

    def engine_make_move(self, client_move):
        self.engine.make_move(client_move['starting_square'], client_move['target_square'])
        engine_move = self.engine.get_random_move()
        legal_moves = self.engine.get_legal_moves()
        moves_as_dicts = [move.__dict__ for move in legal_moves]
        self.send(text_data=json.dumps({
            'action': 'engine_make_move',
            'engine_move': engine_move.__dict__,
            'moves': moves_as_dicts
        }))
