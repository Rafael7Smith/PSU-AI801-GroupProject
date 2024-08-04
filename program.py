import WumpusGame
import agent
import pandas as pd
"""
Metrics:
Failures
Total Turns
Revisited Rooms
Arrows Fired
Bats Encountered
"""

if __name__ == '__main__':                        
    # TODO: In the original game you can replay a dungeon (same positions of you and the threats)

    
    # WG.gameloop()

    # TODO:
    final_results = pd.DataFrame(columns=['Victory','Cause', 'Turns', 'Explored %', 'Repeats', 'Bats', 'Missed Arrows'])
    for iter in range(100):
        WG = WumpusGame.WumpusGame(cave='square')
        agent_dfs = agent.agent_dfs(WG)
        results = agent_dfs.run_game()
        final_results = pd.concat([final_results, results], ignore_index=True)

    with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 3,
                       ):
        print(final_results)
    for iter in final_results.columns:
        print(f'Column: {iter}\n{final_results[iter].describe()}')
    """
    For Agent in agent.Agent_list:
        WG = WumpusGame(agent = true)
        score = Agent(WG)
        print(score)
            score - Dataframe
            iteration # (run #)     turns   Revisited Rooms bats encountered   Arrows Fired     win


        Agent_DFS avg of 32 turns, Avg of 11 revisted rooms, Avg of 0 bats
        Agnet_Astar avg of 12 turns, win rate 32%

    """