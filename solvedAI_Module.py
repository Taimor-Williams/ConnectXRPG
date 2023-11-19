import backEndBoard_Module
from backEndBoard_Module import *
class solvedAI():
    """
    AI that plays a perfect game of connect four. When it is given a boardstate and a chipColor, It generates the best
    move it can make in that position. 

    AF()
    RI:
    Protection from rep exposure:
    """

    def makeMove(self,boardState: list[list[int]], chipColor: "interFaceChip")-> int:
        """
        @param boardState, the current state of the board
        @param chipColor, the color the AI is calculating for
        @returns, the column the AI wants to place the chip in 
        """

    def isTerminal(self,board:BackEndBoard):
        return board.victoryCheck(RedChip) or board.victoryCheck(BlackChip) or board.noMoves()

    def winning_move(self,board:BackEndBoard,chipColor):
        """
        Determines if there is a winning move in the position by
        trying each of the possible moves and returns a high score 
        if there is one.
        """
        for column in range(len(board.array)):
            #try making a move
            if board.tryPlaceChip(column,chipColor):
                return 100
        return 0
    


    

    def _minMaxAlgorithim(self,board, depth, alpha, beta, maximizingPlayer):
        """
        need to figure out exactly what this is and how it works but should solve the game
        """
        if self.isTerminal(board):
            if board.victoryCheck(RedChip):
                return (None, 9999999)
            elif board.victoryCheck(BlackChip):
                return (None, 9999999)    
            else: 
                return (None,0)
            
        if depth == 0:
            return (None, )
        