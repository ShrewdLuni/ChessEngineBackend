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
            'engine_unmake_move': self.engine_unmake_move,
            'engine_set_position': lambda: self.engine_set_position(data.get('fen'))
        }
        action_func = action_map.get(action)
        if action_func:
            action_func()
        else:
            self.send(text_data=json.dumps({'error': 'Unknown action'}))

    def engine_get_legal_moves(self):
        legal_moves = self.engine.get_legal_moves()
        if self.engine.board.is_checkmate:
            self.send(text_data=json.dumps({
                'action': 'engine_game_over',
            }))
        else:
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
        self.send(text_data=json.dumps({
            'action': 'engine_update_evaluation',
            'evaluation': self.engine.evaluation.evaluate()
        }))
        result = self.engine.get_best_move()
        move = ["a", "b", "c", "d", "e", "f", "g", "h"][result["move"].get_starting_square() % 8] + str(8 - (result["move"].get_starting_square() // 8)) + ["a", "b", "c", "d", "e", "f", "g", "h"][result["move"].get_target_square() % 8] + str(8 - (result["move"].get_target_square() // 8))
        self.send(text_data=json.dumps({
            'action': 'engine_make_move',
            'fen': self.engine.board.fen_from_board(),
            'move': move,
            'evaluation': result["evaluation"]
        }))

    def engine_unmake_move(self):
        self.engine.unmake_move()
        self.send(text_data=json.dumps({
            'action': 'engine_make_move',
            'fen': self.engine.board.fen_from_board(),
        }))

    def engine_set_position(self, fen):
        self.engine.set_position(fen)
        self.send(text_data=json.dumps({
            'action': 'engine_set_position',
            'fen': self.engine.board.fen_from_board(),
            'evaluation': self.engine.evaluation.evaluate()
        }))
        self.engine_get_legal_moves()

