import json
from channels.generic.websocket import WebsocketConsumer

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
            'engine_get_legal_moves': self.engine_get_legal_moves,
            'engine_make_move': lambda: self.engine_make_move(data.get('move')),
            'engine_unmake_move': self.engine_unmake_move
        }
        action_func = action_map.get(action)
        if action_func:
            action_func()
        else:
            self.send(text_data=json.dumps({'error': 'Unknown action'}))

    def engine_get_legal_moves(self):
        legal_moves = self.engine.get_legal_moves()
        moves = [
            {
                'starting_square': move.get_starting_square(),
                'target_square': move.get_target_square(),
                'flag': move.get_move_flag(),
            }
            for move in legal_moves
        ]
        self.send(text_data=json.dumps({
            'action': 'engine_get_legal_moves',
            'moves': moves,
        }))

    def engine_make_move(self, client_move):
        self.engine.make_move(client_move['starting_square'], client_move['target_square'], client_move['flag'])
        engine_move = self.engine.get_best_move()
        self.send(text_data=json.dumps({
            'action': 'engine_make_move',
            'fen': self.engine.board.fen_from_board(),
        }))

    def engine_unmake_move(self):
        self.engine.unmake_move()
        self.send(text_data=json.dumps({
            'action': 'engine_make_move',
            'fen': self.engine.board.fen_from_board(),
        }))

