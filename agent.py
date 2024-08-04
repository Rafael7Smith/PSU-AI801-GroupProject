agent_list = "TODO"


import pandas as pd

DEBUG = True
class agent_generic():

    def __init__(self, game):
        self.dataframe_score = pd.DataFrame()
        self.game = game
        self.current_position = 0
        self.current_turn = 0

        return

    def run_game(self):
        self.current_position = self.game.populate_cave()
        game_state = self.game.enter_room(self.current_position)

        while(True):
            if(DEBUG): print(f'----New Turn: {self.current_turn}, Game State: {game_state}----')
            if(game_state[0] == -1):
                print("AGENT LOST GAME")
                break
            if(game_state[0] == -2):
                print("AGENT WON GAME")
                break
            
            #update current position
            self.current_position = game_state[0]

            #Score the game
            self.record_score(game_state)

            #evaluate the game state and determine the next move
            mode, target = self.evaluate_gamestate(game_state)

            #make the next move
            if mode == 'm':
                game_state = self.game.enter_room(target)
                self.game.player_pos = game_state[0]
            elif mode == 's':
                game_state = self.game.shoot_room(target)
            elif mode == 'q':
                print("AGENT LOST GAME")
                break

            self.current_turn = self.current_turn + 1

        return
    
    def evaluate_gamestate(self):
        return

    def record_score(self, game_state):
        return
    
class agent_dfs(agent_generic):
    """
    DFS
    YY YY YY YY YY
    12 13 14 15 16
    11 10 09 XX 17
    06 07 08 01 18
    05 04 03 02 19
    """
    def __init__(self, game):
        self.dataframe_score = pd.DataFrame()
        self.game = game
        self.current_position = 0
        self.current_turn = 0
        self.visited = []
        self.fired = []

    def evaluate_gamestate(self, game_state):
        if(DEBUG): print(f'DFS eval of {game_state}')

        available_options = self.game.cave[game_state[0]]
        if(DEBUG): print(f'Available choices {available_options}')
        warnings = game_state[1]
        
        unvisited_options = list(set(available_options).difference(self.visited))
        unvisited_options.sort()
        if(DEBUG): print(f'Visited nodes {self.visited}, unvisited options: {unvisited_options}')
        #if we are near the wumpus shoot an arrow
        if(len(unvisited_options) < 1):
            mode = 'q'
            target = 0

        elif('Missed' in warnings or 'bat' in warnings):
            #We missed, reenter room to get the warnings
            mode = 'm'
            target = game_state[0]
            if(DEBUG): print(f'Missed arrow. Re-entering room{target}')

        elif('wumpus' in warnings):
            mode = 's'
            
            unvisited_options = list(set(unvisited_options).difference(self.fired))
            target = unvisited_options[0]
            self.fired.append(target)
            if(DEBUG): print(f'Shoot mode at {target}, fired at options: {self.fired}')
        else:
            mode = 'm'
            target = unvisited_options[0]
            if(DEBUG): print(f'Move mode to {target}')

        self.visited.append(game_state[0])
        return mode, target
    
    def dfs_search(self, stack, visited):
        return

class agent_bfs(agent_generic):
    """
    TODO
    """
    """
    BFS
    05 04 03 02 03
    04 03 02 01 02
    03 02 01 XX 01
    04 03 02 01 02
    05 04 03 02 03
    """
class agent_astar(agent_generic):
    """
    TODO
    """

