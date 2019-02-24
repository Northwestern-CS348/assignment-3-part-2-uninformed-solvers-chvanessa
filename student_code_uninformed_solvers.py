
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here

        currGS = self.currentState  # game state object, not the tuple

        if currGS.state == self.victoryCondition : return True
        else:
            print('is this where i die')
            # set up to explore possible moves
            lom = self.gm.getMovables() # list of movable statements
            d = self.currentState.depth
            print('\nmoves??', lom)

            tovisit = []

            # need to check if there are no longer any movables
            if not lom:
                gobackmove = self.currentState.requiredMovable
                if gobackmove: #if this exists
                    self.gm.reverseMove(gobackmove)
                    self.currentState = self.currentState.parent  # is this legal
                    # self.currentState.depth -= 1

            for m in lom:
                # Make the move, then create new game states and if not visited, save as children
                self.gm.makeMove(m)
                childState = GameState(self.currentState, d+1, m)
                self.gm.reverseMove(m)
                print('what is this?', self.visited)
                print('a CS', childState)
                print('is this a tuple', childState.state)
                # if childState not in self.visited:

                if self.visited[childState.state] == False:
                    self.visited[childState.state] = False # wait should this be set as True or False for unvisited
                    tovisit.append(childState)
                    childState.parent = self.currentState
                    self.gm.makeMove(m)
                    self.currentState = childState
                    # break
                else:
                    if self.visited[childState.state] == True: # if has been visited, then go back up to parent node
                        if currGS.requiredMovable:
                            self.gm.reverseMove(currGS.requiredMovable)
                            self.solveOneStep()

            # self.currentState.children = tovisit
            i = self.currentState.nextChildToVisit

            for each in tovisit:
                try:
                    nextGS = tovisit[i]
                except:
                    # go back up parent
                    gobackmove = self.currentState.requiredMovable
                    self.gm.reverseMove(gobackmove)
                    self.currentState = self.currentState.parent    # is this legal
                    self.solveOneStep()

                nextmove = nextGS.requiredMovable
                self.gm.makeMove(nextmove)
                self.visited[nextGS] = True #update that you have visited

                if self.currentState.state == self.victoryCondition: return True
                else: pass



class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        return True
