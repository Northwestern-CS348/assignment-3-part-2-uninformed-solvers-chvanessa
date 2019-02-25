
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

        # currGS = self.currentState  # game state object, not the tuple
        self.visited[self.currentState] = True
        print('what is currstate', self.currentState.state)
        print('is it visted', self.visited[self.currentState])


        if self.currentState.state == self.victoryCondition: return True
        else:
            # currGS.children should return a list of GS objects, if empty it means this node is not expanded
            if self.currentState.children == []:
                # Need to check if there are no longer any movables
                lom = self.gm.getMovables()
                d = self.currentState.depth
                # print('\nlist of movables', lom)
                if lom is not []:
                    for m in lom:
                        # Make the move, then create new game states and if not visited, save as children
                        self.gm.makeMove(m)
                        childState = GameState(self.gm.getGameState(), d + 1, m)
                        self.gm.reverseMove(m)

                        if childState not in self.visited:
                            self.visited[childState] = False # Set as False, to be visited
                        childState.parent = self.currentState
                        self.currentState.children.append(childState)

                        print('\nHow many children', len(self.currentState.children))
                        print('Child state', childState.state)
                        print('Depth', childState.depth)
                        print('Visited?', self.visited[childState],'\n')

                    self.solveOneStep()
                    print('???')
                    # return False
                    # self.solveOneStep()
                # If there are no movables, then reverse
                else:
                    gobackmove = self.currentState.requiredMovable
                    self.gm.reverseMove(gobackmove)
                    self.currentState = self.currentState.parent
                    print('Go back, this is a move')
                    self.solveOneStep()
            # If there are already children for this node, means we have been here before, explore next node
            else:
                for child in self.currentState.children:
                    if self.visited[child] == True: pass
                    else:
                        print('Making a move, is this the right child', child.state)
                        nextmove = child.requiredMovable
                        self.visited[child] = True
                        self.gm.makeMove(nextmove)
                        self.currentState = child #???
                        print('Movables?',len(self.gm.getMovables()))
                        print('here they are',self.gm.getMovables(), '\n')
                        # print('Facts')
                        # for f in self.gm.kb.facts:
                        #     print(f)
                        # print('\nend\n')
                        if self.currentState.state == self.victoryCondition: return True
                        else: return False # do i need to check vic condition again
                # If they have all been explored
                if self.currentState.requiredMovable:
                    self.gm.reverseMove(self.currentState.requiredMovable)
                    self.currentState = self.currentState.parent # unsure
                    return False


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
