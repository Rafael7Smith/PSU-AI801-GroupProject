agent_list = "TODO"


import pandas as pd

class agent_generic():

    def __init__(self, game):
        self.dataframe_score = pd.dataframe()
        self.game = game
        self.current_position = 0
        self.current_turn = 0

        return

    def run_game(self):
        self.current_position = self.game.populate_cave()
        game_state = self.game.enter_room(self.current_position)

        while(game_state[0] is not -1 and game_state[0] is not -2):
            #update current position
            self.current_position = game_state[0]

            #Score the game
            self.record_score(game_state)

            #evaluate the game state and determine the next move
            mode, target = self.evaluate_gamestate(game_state)

            #make the next move
            if mode == 'm':
                game_state = self.game.enter_room(target)
            elif mode == 's':
                game_state = self.game.shoot_room(target)

        return
    
    def evaluate_gamestate(self):
        return

    def record_score(self):
        return
    
class agent_dfs(agent_generic):
    """
    TODO
    """
    def __init__(self, game):
        super.__init__(game)
        self.visited = []
        self.fired = []

    def evaluate_gamestate(self, game_state):
        available_options = self.game.cave[game_state[0]]
        warnings = game_state[1]
        
        self.visited.append(game_state[0])

       
        selectable_options = list(set(available_options.difference(self.visited)))
        #if we are near the wumpus shoot an arrow
        if('wumpus' in warnings):
            mode = 's'
            self.fired.append(target)
            selectable_options = list(set(selectable_options).difference(self.fired))
        else:
            mode = 'm'
            target = selectable_options[0]

        
        

        return mode, target
    
    def dfs_search(self, stack, visited):
        return

class agent_astar(agent_generic):
    """
    TODO
    """

