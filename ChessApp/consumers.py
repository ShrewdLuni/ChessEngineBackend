import json
import random
from channels.generic.websocket import WebsocketConsumer

from ChessEngine.board import Board
from ChessEngine.move_generator import MoveGenerator
from ChessEngine.precomputed_move_data import PrecomputedMoveData
from ChessEngine.engine import Engine

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
            'get_chess_info': self.get_chess_info,
            'engine_make_move': self.engine_make_move
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

    #update board aka make player move
    #find and make best move aka update board again
    #search legal moves for client
    #send server move and legal moves

    def get_chess_info(self):
        brd = Board()
        pmd = PrecomputedMoveData()
        mg = MoveGenerator(brd, pmd)
        brd.fen_to_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

        mg.generate_legal_moves()

        moves_as_dicts = [move.__dict__ for move in mg.moves]
        self.send(text_data=json.dumps({
            'action': 'get_chess_info',
            'moves': moves_as_dicts
        }))

    def engine_make_move(self):
        engine = Engine()
        engine_move = engine.get_random_move("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.send(text_data=json.dumps({
            'action': 'engine_make_move',
            'engine_move': engine_move.__dict__
        }))
