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
    final_results = None
    for iter in range(100):
        WG = WumpusGame.WumpusGame(cave='square')
        agent_dfs = agent.agent_dfs(WG)
        results = agent_dfs.run_game()
        if(final_results is None):
            final_results = results
        else:
            final_results = pd.concat([final_results, results], ignore_index=True)

    print(f'-----------------------------------------------------------------\n')
    print(f'-----------------------------------------------------------------\n')
    print(f'-----------------------------------------------------------------\n')

    Human_final_results = None
    for iter in range(2):
        WG = WumpusGame.WumpusGame(cave='square')
        agent_dfs = agent.human(WG)
        results = agent_dfs.run_game()
        if(Human_final_results is None):
            Human_final_results = results
        else:
            Human_final_results = pd.concat([Human_final_results, results], ignore_index=True)

    pd.set_option('display.float_format', lambda x: '%.2f' % x)
    with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 1,
                       ):
        print(final_results)
    print(final_results.describe(include='all'))
    final_results.to_csv('DFS_Results.csv')
    print(f'\n-----------------------------------------------------------------\n')

    with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 1,
                       ):
        print(Human_final_results)
    print(Human_final_results.describe(include='all'))
    Human_final_results.to_csv('Human_Results.csv')
