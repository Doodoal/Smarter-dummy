# For more info see docs.battlesnake.com

import random
import typing

def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "doodoal", 
        "color": "#F2BBEF",  
        "head": "rocket-helmet",  
        "tail": "mlh-gene", 
    }



def start(game_state: typing.Dict):
    """start is called when the Battlesnake begins a game"""
    print("GAME START")



def end(game_state: typing.Dict):
    """called when the Battlesnake finishes a game"""
    print("GAME OVER\n")


def avoid_walls(possible_moves: typing.Dict, game_state: typing.Dict)-> typing.Dict:
    """
    Delete possible moves that lead into the walls
    Return the remaining moves
    """
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']
    remove = []
    for direction, location in possible_moves.items():
      xOffLimits = (location ["x"]<0 or location["x"] == board_width)
      yOffLimits = (location ["y"]<0 or location["y"] == board_height)

      if xOffLimits or yOffLimits:
        remove.append(direction)

    for direction in remove:
        del possible_moves[direction]

    return possible_moves

def avoid_self(possible_moves: typing.Dict, game_state: typing.Dict)-> typing.Dict:
    """
    Delete possible moves that lead to a self-collusion
    Return the remaining moves
    """
    my_body = game_state["you"]["body"]
    remove = []
    for direction, location in possible_moves.items():
      if (location in my_body): 
        remove.append(direction)

    for direction in remove:
        del possible_moves[direction]
      
    return possible_moves
  
def avoid_others(possible_moves: typing.Dict, game_state: typing.Dict)-> typing.Dict:
    """
    Delete possible moves that lead to a collusion with others
    Return the remaining moves
    """
    remove = []
    opponents = game_state['board']['snakes']
    for snake in opponents:
      for direction, location in possible_moves.items():
        if location in snake["body"]:
          remove.append(direction)

    for direction in remove:
        del possible_moves[direction]
      
    return possible_moves


  
def move(game_state: typing.Dict) -> typing.Dict:
    """"
    move is called on every turn and returns your next move
    Valid moves are "up", "down", "left", or "right"
    See https://docs.battlesnake.com/api/example-move for available data
    """
    my_head = game_state["you"]["body"][0]  

    possible_moves = {
      "up": {
        "x": my_head["x"],
        "y": my_head["y"] + 1
      },
      
      "down": {
        "x": my_head["x"],
        "y": my_head["y"] - 1
      }, 
      "left": {
        "x": my_head["x"]-1,
        "y": my_head["y"] 
      }, 
      "right": {
        "x": my_head["x"]+1,
        "y": my_head["y"] 
      }
    }

    possible_moves = avoid_walls(possible_moves, game_state)
    possible_moves = avoid_self(possible_moves, game_state)
    possible_moves = avoid_others(possible_moves, game_state)
      
    safe_moves = list(possible_moves.keys())
    
    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Choose a random move from the safe ones
    next_move = random.choice(safe_moves)

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    # food = game_state['board']['food']

    ##Lines for debugging
    print(f"MOVE {game_state['turn']}: {next_move}")
    print(f"Safe moves: {safe_moves}")
    print(f"Head coordinates : {my_head}")
    print(f"Next move coordinate: {possible_moves[next_move]}")
    #print(f"Board size: {board_height} x{board_width}")
    print("\n\n")
  
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({
        "info": info, 
        "start": start, 
         "move": move, 
        "end": end
    })
