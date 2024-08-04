agent_list = "TODO"
score_columns = ['Victory','Cause', 'Turns', 'Explored %', 'Repeats', 'Bats', 'Missed Arrows']

import pandas as pd

DEBUG = True
class agent_generic():

    def __init__(self, game):
        self.dataframe_score = pd.DataFrame(columns=score_columns)
        self.game = game
        self.current_position = 0
        self.current_turn = 0

        self.visit_count = dict.fromkeys(self.game.cave.keys(), 0)
        self.misssed_count = 0
        self.bat_count = 0
        self.victory = False
        return

    def run_game(self):
        self.current_position = self.game.populate_cave()
        game_state = self.game.enter_room(self.current_position)

        while(True):
            if(DEBUG): print(f'----New Turn: {self.current_turn}, Game State: {game_state}----')
            
            #Score the game
            self.record_score(game_state)

            if(game_state[0] == -1):
                print("AGENT LOST GAME")
                break
            if(game_state[0] == -2):
                print("AGENT WON GAME")
                break
            
            #update current position
            self.current_position = game_state[0]

            #evaluate the game state and determine the next move
            mode, target = self.evaluate_gamestate(game_state)

            #make the next move
            if mode == 'm':
                game_state = self.game.enter_room(target)
                self.game.player_pos = game_state[0]
            elif mode == 's':
                game_state = self.game.shoot_room(target)
            elif mode == 'q':
                game_state = self.game.surrender_game(target)
                break

            self.current_turn = self.current_turn + 1

        self.final_score(game_state)
        
        #print(f'Final Score:\n{self.dataframe_score}')
        return self.dataframe_score
    
    def evaluate_gamestate(self):
        return

    def record_score(self, game_state):

        if(game_state[0] == -1):
            self.victory = False
        elif(game_state[0] == -2):
            self.victory = True
        else:
            #how many times have you visited each square
            self.visit_count[game_state[0]] += 1

            #how many times did you run into a bat
            if('CatchBat' in game_state[1]):
                self.bat_count += 1
            #how many arrows missed
            if('Missed' in game_state[1]):
                self.misssed_count += 1
        return
    
    def final_score(self, game_state):

        visited_cells = list(filter(self.filter_grthanzero, self.visit_count.values()))
        explored_percent = len(visited_cells)/(len(self.game.cave)) * 100

        repeated_cells = list(filter(self.filter_grthanone, self.visit_count.values()))
        #['Victory','Cause', 'Turns', 'Explored', 'Repeats', 'Bats', 'Missed Arrows']
        df_index = len(self.dataframe_score.index)
        self.dataframe_score.loc[df_index] = [self.victory, game_state[1], self.current_turn, explored_percent,len(repeated_cells),self.bat_count,self.misssed_count]
        return
    
    def filter_grthanzero(self, item):
        return item > 0
    
    def filter_grthanone(self, item):
        return item > 1
    
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
        super().__init__(game)
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

        elif('Missed' in warnings or 'Killbat' in warnings or 'CatchBat' in warnings):
            #We missed, reenter room to get the warnings
            mode = 'm'
            target = game_state[0]
            if(DEBUG): print(f'Re-entering room{target}')

        elif('wumpus' in warnings):
            mode = 's'
            
            unvisited_options = list(set(unvisited_options).difference(self.fired))
            unvisited_options.sort()
            target = unvisited_options[0]
            self.fired.append(target)
            if(DEBUG): print(f'Shoot mode at {target}, fired at options: {unvisited_options}')
        else:
            mode = 'm'
            target = unvisited_options[0]
            if(DEBUG): print(f'Move mode to {target}')

        self.visited.append(game_state[0])
        return mode, target
    
class agent_bfs(agent_generic):
    """
    BFS
    05 04 03 02 03
    04 03 02 01 02
    03 02 01 XX 01
    04 03 02 01 02
    05 04 03 02 03
    """
    def __init__(self, game):
        super().__init__(game)
        self.visited = []
        self.fired = []

    def evaluate_gamestate(self, game_state):
        if(DEBUG): print(f'BFS eval of {game_state}')

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

        elif('Missed' in warnings or 'Killbat' in warnings or 'CatchBat' in warnings):
            #We missed, reenter room to get the warnings
            mode = 'm'
            target = game_state[0]
            if(DEBUG): print(f'Re-entering room{target}')

        elif('wumpus' in warnings):
            mode = 's'
            
            unvisited_options = list(set(unvisited_options).difference(self.fired))
            unvisited_options.sort()
            target = unvisited_options[0]
            self.fired.append(target)
            if(DEBUG): print(f'Shoot mode at {target}, fired at options: {unvisited_options}')
        else:
            mode = 'm'
            target = unvisited_options[0]
            if(DEBUG): print(f'Move mode to {target}')

        self.visited.append(game_state[0])
        return mode, target


class agent_simpleKB(agent_generic):
    """
    TODO
    """
    #Build a map of cave
    #Avoid pits
    #evaluate probability of threat @ location


class agent_advancedKB(agent_generic):
    """
    TODO
    """