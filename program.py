import WumpusGame
import agent
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

    WG = WumpusGame.WumpusGame(cave='square')
    # WG.gameloop()

    # TODO:

    agent_dfs = agent.agent_dfs(WG)
    agent_dfs.run_game()

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