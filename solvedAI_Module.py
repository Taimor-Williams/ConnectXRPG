from chip_Module import *
from backEndBoard_Module import *
import numpy as np
import random
import copy 

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
    def scorePosition(self, board: BackEndBoard, chipColor: InterFaceChip):
        """
        @param board, current gamestate we are considering
        @param chipColor, the perspective we are considering
        @effects
        """
        boardArray = board.showBoardList()
        colCount = len(boardArray)
        rowCount =  len(boardArray[0])
        score = 0
        windowlist: list[list[int]] = []

        # Score centre column
        # centre_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
        # centre_count = centre_array.count(piece)
        # score += centre_count * 3

        # Score horizontal positions
        for window in self._getHorizontal(board):
            score += self.evaluateWindow(window, chipColor)

        # Score vertical positions
        for window in self._getVertical(board):
            score += self.evaluateWindow(window, chipColor)

        # Score positive diagonals
        for window in self._getPositiveDiagnol(board):
            score += self.evaluateWindow(window, chipColor)

        # Score negative diagonals
        for window in self._getNegativeDiagnol(board):
            score += self.evaluateWindow(window, chipColor)
        
        return score
    
    def evaluateWindow(self, window: list[int], chipColor: InterFaceChip)->int:
        """
        @param window, sequence of four squares being checked for victory
        @param chipColor, color AI is playing
        @returns, score of the window for that chipColor perspective
        """
        score = 0
        empty = 0
        # Switch scoring based on turn
        piece = 1
        opponentPiece = 2
        if isinstance(chipColor,RedChip):
            piece = 2
            opponentPiece = 1
        
            

        # Prioritise a winning move
        # Minimax makes this less important
        if window.count(piece) == 4:
            score += 100
        # Make connecting 3 second priority
        elif window.count(piece) == 3 and window.count(empty) == 1:
            score += 5
        # Make connecting 2 third priority
        elif window.count(piece) == 2 and window.count(empty) == 2:
            score += 2
        # Prioritise blocking an opponent's winning move (but not over bot winning)
        # Minimax makes this less important
        if window.count(opponentPiece) == 3 and window.count(empty) == 1:
            score -= 6

        return score
    
    def _getHorizontal(self, board: BackEndBoard)-> [[int]]:
        """
        @param board, 
        """
        boardArray = board.showBoardList()
        rowCount = len(boardArray)
        colCount =  len(boardArray[0])
        score = 0
        windowLength= board.victoryLength

        windowList = []
        for row in range(rowCount):
            for col in range(colCount-windowLength+1):
                windowRow = boardArray[row][:]
                window = windowRow[col:col+windowLength]
                windowList.append(window)
        return windowList
        
    
    def _getVertical(self, board: BackEndBoard)-> [[int]]:
        """
        @param board, 
        @returns 
        """
        boardArray = np.asarray(board.showBoardList())
        rowCount = len(boardArray)
        colCount =  len(boardArray[0])
        score = 0
        windowLength= board.victoryLength

        windowList = []
        for row in range(rowCount-windowLength+1):
            for col in range(colCount):
                windowColumn = boardArray[:, col]
                window = windowColumn[row:row+windowLength]
                windowList.append(list(window))
        return windowList
    
    def _getPositiveDiagnol(self, board: BackEndBoard)->[[int]]:
        """
        @param board, 
        @return
        """
        boardArray = board.showBoardList()
        windowLength = board.victoryLength
        windows = []
        for r in range(board.victoryLength-1, 2*board.victoryLength-1):
            for c in range(board.victoryLength):
            # Create a positive diagonal window of victoryLength
                window = [boardArray[r - i][c - i] for i in range(windowLength)]
                windows.append(window)
        return windows

    def _getNegativeDiagnol(self, board: BackEndBoard)->[[int]]:
        """
        @param board, 
        @return
        """
        boardArray = board.showBoardList()
        windowLength = board.victoryLength
        windows = []
        for r in range(0, board.victoryLength):
            for c in range(board.victoryLength):
            # Create a positive diagonal window of victoryLength
                window = [boardArray[r + i][c + i] for i in range(windowLength)]
                windows.append(window)
        return windows
                


    def isTerminal(self,board:BackEndBoard):
        return board.victoryCheck(RedChip()) or board.victoryCheck(BlackChip()) or board.validMoves()== []

    def winningMove(self,board:BackEndBoard,chipColor):
        """
        did you win? which is b
        Determines if there is a winning move in the position by
        trying each of the possible moves and returns a high score 
        if there is one.
        """
        for column in range(len(board.array)):
            #try making a move
            if board.tryPlaceChip(column,chipColor):
                return 100
        return 0
    
    


    

    def _minMaxAlgorithim(self,board: BackEndBoard, depth: int, alpha, beta, maximizingPlayer: bool, chipColor: InterFaceChip)->tuple[int,int]:
        """
        need to figure out exactly what this is and how it works but should solve the game
        @param board, 
        @param, depth, this is a recursive alg so how far down do you want to go
        @param alpha,
        @param beta,
        @param maximizing player, minmax tries to find the move that maximizes its score and 
        minimizes tge opponets score, this boolean acts as a switch
        @effects
        """

        # setup
        validMoves = board.validMoves()
        isTerminal = self.isTerminal(board)
        if isinstance(chipColor, BlackChip):
            oppColor = RedChip()
            botColor = BlackChip()

        # terminal
        if depth ==0 or isTerminal:
            if isTerminal:
                if board.victoryCheck(botColor):
                    return (None, 9999999)
                elif board.victoryCheck(oppColor):
                    return (None, -9999999)    
                else: 
                    return (None,0)
            else:
                return (None, self.scorePosition(board, chipColor))
            
        #recursive
        if maximizingPlayer:
            value = -9999999
            # Randomise column to start
            column = random.choice(validMoves)
            for col in validMoves:
                # Create a copy of the board
                copyBoard = copy.deepcopy(board)
                # Drop a piece in the temporary board and record score
                copyBoard.placeChip(col, chipColor)
                print(col)
                newScore = self._minMaxAlgorithim(copyBoard, depth - 1, alpha, beta, False, chipColor)[1]
                if newScore > value:
                    value = newScore
                    # Make 'column' the best scoring column we can get
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value
        else:  # Minimising player
            value = 9999999
            # Randomise column to start
            column = random.choice(validMoves)
            for col in validMoves:
                # Create a copy of the board
                copyBoard = copy.deepcopy(board)
                # Drop a piece in the temporary board and record score
                board.placeChip(col, chipColor)
                newScore = self._minMaxAlgorithim(copyBoard, depth - 1, alpha, beta, True, chipColor)[1]
                print(col, newScore)
                if newScore < value:
                    value = newScore
                    # Make 'column' the best scoring column we can get
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value
        
    def minMaxAlgorithim(self, board: BackEndBoard, depth: int, maximizingPlayer: bool)->tuple[int, int]:
        """
        @position, current board position
        @depth, how many moves ahead are we considering
        @maximaizingPlayer, are you black or red, black wants high value, red wants low value
        @returns move made represented by column then score at that resulting board position
        """
        if depth == 0 or self.isTerminal(board):
            # print(board.showBoardList())
            # print((None, self.scorePosition(board, BlackChip()) - self.scorePosition(board,RedChip())))
            return (None, self.scorePosition(board, BlackChip()) - self.scorePosition(board,RedChip()))
        
        validMoves = board.validMoves()

        if maximizingPlayer:
            maxEval = -float('inf')
            maxColumn = 0
            for col in validMoves:
                copyBoard = copy.deepcopy(board)
                copyBoard.placeChip(col, BlackChip())
                eval = self.minMaxAlgorithim(copyBoard,depth-1,False)[1]
                if eval > maxEval:
                    maxEval = eval
                    maxColumn = col
            # print(copyBoard.showBoardList())
            # print(maxColumn,maxEval)
            return maxColumn,maxEval
        
        if not maximizingPlayer:
            minEval = float('inf')
            minColumn = 0
            for col in validMoves:
                copyBoard = copy.deepcopy(board)
                copyBoard.placeChip(col, RedChip())
                eval = self.minMaxAlgorithim(copyBoard,depth-1,False)[1]
                if eval < minEval:
                    minEval = eval
                    minColumn = col
            # print(copyBoard.showBoardList())
            # print(minColumn,minEval)
            return minColumn,minEval
    

    # now we are doing same thing but using ndarray 

    def isTerminalNump(self, board: np.ndarray, chip: InterFaceChip)->bool:
        """
        @param board, array of board position
        @returns, whether the board is in terminal state or not
        """
        piece = 2
        if isinstance(chip, BlackChip):
            piece = 1
        

        totalRows, totalColumns = np.shape(board)
        # Check valid horizontal locations for win
        for c in range(totalColumns - 3):
            for r in range(totalRows):
                if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                    return True

        # Check valid vertical locations for win
        for c in range(totalColumns):
            for r in range(totalRows - 3):
                if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                    return True

        # Check valid positive diagonal locations for win
        for c in range(totalColumns - 3):
            for r in range(totalRows - 3):
                if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                    return True

        # check valid negative diagonal locations for win
        for c in range(totalColumns - 3):
            for r in range(3, totalRows):
                if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                    return True
    


    def windowNump(self, board: np.ndarray):
        """
        @param board, array of board position
        """

    def scorePositionNumpy(self, board: np.ndarray, piece: InterFaceChip):
        """
        @param board,
        @param piece, 
        """
        totalRows, totalColumns = np.shape(board)
        windowLength = 4
        score = 0

        # Score centre column
        # centre_array = [int(i) for i in list(board[:, totalColumns // 2])]
        # centre_count = centre_array.count(piece)
        # score += centre_count * 3

        # Score horizontal positions
        for r in range(totalRows):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(totalColumns - 3):
                # Create a horizontal window of 4
                window = row_array[c:c + windowLength]
                score += self.evaluateWindow(window, piece)

        # Score vertical positions
        for c in range(totalColumns):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(totalRows - 3):
                # Create a vertical window of 4
                window = col_array[r:r + windowLength]
                score += self.evaluateWindow(window, piece)

        # Score positive diagonals
        for r in range(totalRows - 3):
            for c in range(totalColumns - 3):
                # Create a positive diagonal window of 4
                window = [board[r + i][c + i] for i in range(windowLength)]
                score += self.evaluateWindow(window, piece)

        # Score negative diagonals
        for r in range(totalRows - 3):
            for c in range(totalColumns - 3):
                # Create a negative diagonal window of 4
                window = [board[r + 3 - i][c + i] for i in range(windowLength)]
                score += self.evaluateWindow(window, piece)

        return score
    
    def validMovesNumpy(self, board: np.ndarray)->list[int]:
        """
        @param board, board we are considering
        @returns, list of moves we are considering
        """
        totalRows, totalColumns = np.shape(board)
        validMoves = []
        for col in range(totalColumns):
            if self.isValidLocation(board, col):
                validMoves.append(col)
        return validMoves

    def isValidLocation(self, board: np.ndarray, col:int):
        """
        @param board, board we are looking at
        @param col, 
        """
        totalRows, totalColumns = np.shape(board)
        return board[0][col] == 0
    
    def placeChip(self, board: np.ndarray, col: int, piece: int):
        """
        @param board, 
        @param row
        @param col
        """
        # print(board)
        totalChips = 0
        totalRows, totalColumns = np.shape(board)
        curColumn: list= list(board[:, col])
        totalBlackChips = curColumn.count(1)
        totalRedChips = curColumn.count(2)
        totalChips += totalRedChips+totalBlackChips
        # print(curColumn)
        # print(totalChips)
        # print(totalRows-totalChips-1, col)
        board[totalRows-totalChips-1][col] = piece
        

    
    def minMaxAlgorithimNumpy(self, board: np.ndarray, depth: int, maximizingPlayer: bool)->tuple[int, int]:
        """
        @position, current board position
        @depth, how many moves ahead are we considering
        @maximaizingPlayer, are you black or red, black wants high value, red wants low value
        @returns move made represented by column then score at that resulting board position
        """
        if depth == 0 or self.isTerminalNump(board, BlackChip()) or self.isTerminalNump(board, RedChip()):
            # print(board.showBoardList())
            # print((None, self.scorePosition(board, BlackChip()) - self.scorePosition(board,RedChip())))
            # print((None, self.scorePositionNumpy(board, BlackChip()) - self.scorePositionNumpy(board,RedChip())))
            # print('Black', self.scorePositionNumpy(board, BlackChip()))
            # print('Red', self.scorePositionNumpy(board, RedChip()))
            return (None, self.scorePositionNumpy(board, BlackChip()) - self.scorePositionNumpy(board,RedChip()))
        
        validMoves = self.validMovesNumpy(board)
        

        if maximizingPlayer:
            maxEval = -float('inf')
            maxColumn = 0
            for col in validMoves:
                copyBoard = copy.deepcopy(board)
                self.placeChip(copyBoard,col, 1)
                
                eval = self.minMaxAlgorithimNumpy(copyBoard,depth-1,False)[1]
                if eval > maxEval:
                    maxEval = eval
                    maxColumn = col
                    # print(maxColumn,maxEval)
             
            # print(copyBoard.showBoardList())
            # print(maxColumn,maxEval)
            return maxColumn,maxEval
        
        if not maximizingPlayer:
            minEval = float('inf')
            minColumn = 0
            for col in validMoves:
                copyBoard = copy.deepcopy(board)
                self.placeChip(copyBoard,col, 2)
                eval = self.minMaxAlgorithimNumpy(copyBoard,depth-1,True)[1]
                if eval < minEval:
                    minEval = eval
                    minColumn = col
            return minColumn,minEval


    

        

        
            


        