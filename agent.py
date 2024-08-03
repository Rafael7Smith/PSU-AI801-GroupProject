agent_list = "TODO"

class agent_generic():
    #start the game and get starting position
    current_position = game.populate_cave()
    
    #evulate starting position
    game_state = game.enter_room(current_position)

    # while(game_state not -1 or -2):
    #     tracking(game_state)
    #     mode, target = evaluate(game_state)
    #         if -1
    #             lost
    #         get warning
        
    #     game_state = game.agent_input(mode, target)
            
    
class agent_astar(agent_generic):
    """
    TODO
    """
    
    while(not gameover):
        do the next thing

    #game start

    


        

class agent_dfs():
    """
    TODO
    """