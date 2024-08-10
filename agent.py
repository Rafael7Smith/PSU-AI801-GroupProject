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
    
    def evaluate_gamestate(self):
        """
        Implment evaluation in agent
        """
        return
    
    def run_game(self):
        print(f'******************************')
        print(f'*************NEW GAME*********')
        print(f'******************************')
        #Create Game
        self.current_position = self.game.populate_cave()

        #Ensure Game is solveable with all locations reachable
        solveable, depth = self.game.is_solvable_search(self.current_position)
        while(not solveable):
            if(DEBUG): print(f"DEBUG: Game {self.current_position},{self.game.threats} is not solveable, regenerating")
            self.current_position = self.game.populate_cave()
            solveable, depth = self.game.is_solvable_search(self.current_position)
        
        #Start the game
        game_state = self.game.enter_room(self.current_position)

        while(True):
            #Score the game
            self.record_score(game_state)

            if(game_state[0] == -1):
                print("AGENT LOST GAME")
                print(f'******************************')
                break
            if(game_state[0] == -2):
                print("AGENT WON GAME")
                print(f'******************************')
                break
            
            #update current position
            self.current_position = game_state[0]

            #evaluate the game state and determine the next move
            mode, target = self.evaluate_gamestate(game_state)
            self.current_turn = self.current_turn + 1
            print(f'\n----New Turn: {self.current_turn}----\n')
            #make the next move
            if mode == 'm':
                game_state = self.game.enter_room(target)
                self.game.player_pos = game_state[0]
            elif mode == 's':
                game_state = self.game.shoot_room(target)
            elif mode == 'q':
                game_state = self.game.surrender_game(target)
                break

        self.final_score(game_state)
        
        #print(f'Final Score:\n{self.dataframe_score}')
        self.dataframe_score['Turns'] = self.dataframe_score['Turns'].astype(int)
        self.dataframe_score['Repeats'] = self.dataframe_score['Repeats'].astype(int)
        self.dataframe_score['Bats'] = self.dataframe_score['Bats'].astype(int)
        self.dataframe_score['Missed Arrows'] = self.dataframe_score['Missed Arrows'].astype(int)
        return self.dataframe_score
    
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
            if(len(unvisited_options) > 0):
                target = unvisited_options[0]
            else:
                target = unvisited_options
            self.fired.append(target)
            if(DEBUG): print(f'Shoot mode at {target}, fired at options: {unvisited_options}')
        else:
            mode = 'm'
            if(len(unvisited_options) > 0):
                target = unvisited_options[0]
            else:
                target = unvisited_options
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
        self.layers = {0: [], 1 : [], 2 : [], 3 : [], 4 : [], 5 : []}
        self.current_layer = 0
        self.start_position = -1
        self.visited = []
        self.fired = []
        self.path_queue = []
        self.thread_map = {}
        
    def evaluate_gamestate(self, game_state):
        if(DEBUG): print(f'BFS eval of {game_state}')

        warnings = game_state[1]
        #Start of Game Base case
        if(self.start_position > 0):
            #Record starting postiion as layer zero
            self.layers[0] = game_state[0]
            self.start_position = game_state[0]

            #Generate layer 1
            self.layers[1] = self.game.cave[game_state[0]]
            if(DEBUG): print(f'Initialized BFS: layers={self.layers}')
        #Add current position to visited
        self.visited.append(game_state[0])

        #Add what we currently see to the next layer (minus what is in the previous layer)
        new_nodes = set(self.game.cave[game_state[0]]).difference(self.layers[self.current_layer])
        self.layers[self.current_layer + 1]
        if(DEBUG): print(f'Initializing layer: {self.current_layer + 1}, now ')

        #any warnings?
        if('pit' in warnings):
            print("Handle pit calculations")
        elif('bat'  in warnings):
            print("Handle bat calculations")
        elif('wumpus' in warnings):
            print("Handle wumpus calculations")
        #Have we visited all options available?

        #have we explored all of the current layer?
        if(all(e in self.layers[self.current_layer] for e in self.visited)):
            print(f"We have visited all of layer: {self.current_layer}")
            print(new_nodes)

            #increment the layer
        else:
            print(f"We have not visited all of layer: {self.current_layer}")
            
            #move back up one layer

    
        # available_options = self.game.cave[game_state[0]]
        # if(DEBUG): print(f'Available choices {available_options}')
        # warnings = game_state[1]
        
        # unvisited_options = list(set(available_options).difference(self.visited))
        # unvisited_options.sort()
        # if(DEBUG): print(f'Visited nodes {self.visited}, unvisited options: {unvisited_options}')
        # #if we are near the wumpus shoot an arrow
        # if(len(unvisited_options) < 1):
        #     mode = 'q'
        #     target = 0

        # elif('Missed' in warnings or 'Killbat' in warnings or 'CatchBat' in warnings):
        #     #We missed, reenter room to get the warnings
        #     mode = 'm'
        #     target = game_state[0]
        #     if(DEBUG): print(f'Re-entering room{target}')

        # elif('wumpus' in warnings):
        #     mode = 's'
            
        #     unvisited_options = list(set(unvisited_options).difference(self.fired))
        #     unvisited_options.sort()
        #     target = unvisited_options[0]
        #     self.fired.append(target)
        #     if(DEBUG): print(f'Shoot mode at {target}, fired at options: {unvisited_options}')
        # else:
        #     mode = 'm'
        #     target = unvisited_options[0]
        #     if(DEBUG): print(f'Move mode to {target}')

        # self.visited.append(game_state[0])
        mode = 'm'
        target = 1
        return mode, target

class agent_simpleKB(agent_generic):
    """
    TODO
    """
    #Build a map of cave
    #Avoid pits
    #evaluate probability of threat @ location

class human(agent_generic):
    def __init__(self, game):
        super().__init__(game)
        print("*********GAME MAP*********")
        print( """
        21 22 23 24 25
        16 17 18 19 20
        11 12 13 14 15
        06 07 08 09 10
        01 02 03 04 05
        """)
    def evaluate_gamestate(self, game_state):
        print("You are in room {}.".format(self.game.player_pos), end=" ")
        print("Tunnels lead to:  {}".format(self.game.cave[self.game.player_pos]))
        print(f"Modes = M(Move), S(Shoot), Q(Quit)")
        return self.get_players_input()
    
    def get_players_input(self):
        """ Queries input until valid input is given.
        """
        while 1:                               
            human_input = input("Input: 'Mode Target'\n")
            split_input = human_input.split(" ")
            try:                                # Ensure that the player choses a valid action (shoot or move)
                mode = split_input[0].lower()
                assert mode in ['s', 'm', 'q', 'c']

            except (ValueError, AssertionError):
                print("This is not a valid action: pick 'S' to shoot and 'M' to move.")
                continue

            if mode == 'q':                            # I added a 'quit-button' for convenience.
                return 'q', -1
            
            try:                                # Ensure that the chosen target is convertable to an integer.
                target = int(split_input[1])
            except ValueError:
                print("This is not even a real number.")
                continue

            if mode == 'm':
                try:                            # When walking, the target must be adjacent to the current room.
                    assert target in self.game.cave[self.game.player_pos] or target == self.game.player_pos
                    break
                except AssertionError:
                    print("You cannot walk that far. Please use one of the tunnels.")
            elif mode == 's':
                try:                            # When shooting, the target must be reachable within 1 tunnels.
                    bfs = self.game.breadth_first_search(self.game.player_pos, target)
                    assert bfs[0] == True
                    assert bfs[1] < self.game.arrow_travel_distance
                    break
                except AssertionError:
                    if bfs[1] > self.game.arrow_travel_distance:                # The target is too far.
                        print("Arrows cant go that far.")
        return mode, target
    
class agent_advancedKB(agent_generic):
    """
    TODO
    """