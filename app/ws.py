from fastapi import APIRouter, WebSocket

from ChessEngine import Engine

router = APIRouter(prefix="/ws", tags=["websocket"])

@router.websocket("/chess")
async def websocket_endpoint(websocket: WebSocket):
    engine = Engine()
    await websocket.accept()

    while True:
        data = await websocket.receive_json()
        print(data)
        action = data.get('action')
        match action:
            case 'engine_get_legal_moves':
                await engine_get_legal_moves(websocket, engine)
            case 'engine_make_move':
                await engine_make_move(websocket, engine, data.get('move'))
            case 'engine_unmake_move':
                await engine_unmake_move(websocket, engine)
            case 'engine_set_position':
                await engine_set_position(websocket, engine, data.get('fen'))
            case _:
                await websocket.send_json({
                    "error": 'Unknown action'
                })


async def engine_get_legal_moves(websocket: WebSocket, engine: Engine):
    legal_moves = engine.get_legal_moves()
    if engine.is_checkmate():
        await websocket.send_json({
            'action': 'engine_game_over'
        })
    else:
        moves = [
            {
                'starting_square': move.get_starting_square(),
                'target_square': move.get_target_square(),
                'flag': move.get_move_flag(),
            }
            for move in legal_moves
        ]
        await websocket.send_json({
            'action': 'engine_get_legal_moves',
            'moves': moves,
        })
        
async def engine_make_move(websocket: WebSocket, engine: Engine, client_move):
        engine.make_move(client_move['starting_square'], client_move['target_square'], client_move['flag'])
        await websocket.send_json({
            'action': 'engine_update_evaluation',
            'evaluation': engine.get_current_evaluation()
        })
        result = engine.get_best_move()
        move = ["a", "b", "c", "d", "e", "f", "g", "h"][result["move"].get_starting_square() % 8] + str(8 - (result["move"].get_starting_square() // 8)) + ["a", "b", "c", "d", "e", "f", "g", "h"][result["move"].get_target_square() % 8] + str(8 - (result["move"].get_target_square() // 8))
        await websocket.send_json({
            'action': 'engine_make_move',
            'fen': engine.get_fen(),
            'move': move,
            'evaluation': result["evaluation"]
        })

async def engine_unmake_move(websocket: WebSocket, engine: Engine):
    engine.unmake_move()
    await websocket.send_json({
        'action': 'engine_make_move',
        'fen': engine.get_fen(),
    })

async def engine_set_position(websocket: WebSocket, engine: Engine, fen):
    engine.set_position(fen)
    await websocket.send_json({
        'action': 'engine_set_position',
        'fen': engine.get_fen(),
        'evaluation': engine.get_current_evaluation()
    })
    await engine_get_legal_moves(websocket, engine)



