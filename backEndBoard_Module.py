from chip_Module import *
import math

class BackEndBoard:

    array: list[list[InterFaceChip]]
    victoryLength: int
    moveList: list[tuple[str,int]]

    """
    AF(array, victoryLength) = a board of length and height 2*victoryLength +1
                                where array[i], 0 < i < 2*victoryLength +1 is a column 
                                in the board. The columns are filled with chips where 
                                each chip has another below it or is at the bottom of the column.
                                moveList is a record of the moves made in the game so far. 

    rep invarient:
        for all i,  0 < i < 2*victoryLength +1, array[i] is of length 0 to 2*victoryLength +1
        
    protection from rep exposure:
        placeChip:
            @param column is immuatable
            @param chip is immuatable
            @returns is void
        victoryCheckBlack:
            @param is void
            @returns bool
        victoryCheckRed:
            @param is void
            @returns bool

    """
    def __init__(self, victoryLength: int) -> None:
        self.victoryLength = victoryLength
        self.array = []
        self.moveList = []
        for _ in range(2*self.victoryLength-1):
            self.array.append([])

        
    def placeChip(self, column: int, chip: InterFaceChip):
        """
        @param column, column we are placing chip in
        @param chip, chip we are placing in board
        @exceptions, if column is full do nothing
        """
        curColumn = self.array[column]
        if len(curColumn) == 2*self.victoryLength-1:
            return
        curColumn.append(chip)
        self.moveList.append((str(chip), column))

    def removeChip(self, column: int, chip: InterFaceChip):
        """
        @param column, column we are placing chip in
        @param chip, chip we are placing in board
        @exceptions, if column is full do nothing
        """
        curColumn = self.array[column]
        curColumn.pop()


    def tryPlaceChip(self, column: int, chip: InterFaceChip):
        """
        @param column, column we are placing chip in
        @param chip, chip we are placing in board
        @exceptions, if column is full do nothing
        """
        curColumn = self.array[column]
        if len(curColumn) == 2*self.victoryLength-1:
            return
        curColumn.append(chip)
        self.moveList.append((str(chip), column))
        if self.victoryCheck(self, chip):
            self.removeChip(column)
            return True
        else:
            self.removeChip(column)
        

    def victoryCheck(self, chip: InterFaceChip)->bool:
        """
        @returns bool, returns true if chip of type str(chip) has won
        """
        if self._columnVictoryCheck(chip):
            return True
        if self._rowVictoryCheck(chip):
            return True
        if self._upDiagonalVictoryCheck(chip):
            return True
        if self._downDiagonalVictoryCheck(chip):
            return True
        return False
  
    def validMoves(self)->list[int]:
        """
        @returns, list of valid columns to place chips in
        """
        validMoveList = []
        for col, column in enumerate(self.array):
            if len(column) < 2*self.victoryLength-1:
                validMoveList.append(col)
        return validMoveList


    def showColumn(self, column: int)->list[str]:
        """
        @returns list of chip toStrings
        represents a column in the board
        """
        returnList = []
        curColumn = self.array[column]
        for chip in curColumn:
            returnList.append(chip.toString())
        return returnList
    
    def showBoard(self)-> str:
        """
        @params void
        @returns a string representation of graph
        example reps: 
            empty board victoryLength == 2
                empty   empty   empty   empty   empty
                empty   empty   empty   empty   empty
                empty   empty   empty   empty   empty
                empty   empty   empty   empty   empty
                empty   empty   empty   empty   empty

            empty board victoryLength == 2, red victory
                empty   empty   empty   empty   empty
                empty   empty   empty   empty   empty
                empty   empty   empty   empty   empty
                empty   empty   empty   empty   R
                empty   empty   empty   B       R
        """
        returnStr:str = ""
        # returnStr = f'{self.width}x{self.height}\n'
        for row in range(2*self.victoryLength-1):
            curRow = 2*self.victoryLength - row
            for col in range(2*self.victoryLength-1):
                curCol = col
                # how to make sure something is there
                if len(self.array[curCol])> curRow and len(self.array[curCol])!= 0:
                    returnStr = returnStr + self.array[curCol][curRow].toString()+'\t'
                else:
                    returnStr = returnStr + 'empty\t'
                if col == 2*self.victoryLength:
                    returnStr = returnStr+ '\n'
        return returnStr
    
    def showBoardList(self)->list[list[int]]:
        """
        @returns, the current board as a 2x2 matrix of length victoryLength*2-1 by victoryLength*2-1
        empty squares are 0, blackChips are represented with 1, reed chips with 2
        """
        # make a board
        returnBoard = []
        for _ in range(self.victoryLength*2-1):
            newList = []
            for _ in range(self.victoryLength*2-1):
                newList.append(0)
            returnBoard.append(newList)
        # append the board array to the final product
        for row, stack in enumerate(self.array):
            for col, chip in enumerate(stack):
                finalCol = row
                finalRow = self.victoryLength*2-2-col
                if isinstance(chip, RedChip):
                    returnBoard[finalRow][finalCol] = 2
                else:
                    returnBoard[finalRow][finalCol] = 1
        return returnBoard
    
    def saveGameStr(self):
        """
        @effects, saves the current game to a text file. Where the file is in the format
        example code:

        4, (B,1),(R,2),(B,3),(R,1)
        where 4 is the victoryLength
        and every tuple is a move that was made
        """
        gameStr = str(self.victoryLength)
        for move in self.moveList:
            gameStr += f',{str(move)}'
        return gameStr
    
    def saveGameCSV(self):
        """
        @effects, saves the current game to a text file. Where the file is in the format
        example code:

        4, (B,1),(R,2),(B,3),(R,1)
        where 4 is the victoryLength
        and every tuple is a move that was made
        """
        gameStr = str(self.victoryLength)
        for move in self.moveList:
            gameStr += f',{str(move)}'
        return gameStr

        
                
    #privateFunctuins
    def _columnVictoryCheck(self, chipType: InterFaceChip)->bool:
        """
        @param chipType, chip type we are checking victory for
        @returns bool, wether this chip has won or not vertically
        """
        for column in self.array:
            count = 0
            for chip in column:
                if chip.toString() == chipType.toString():
                    count +=1
                else:
                    count = 0
                if count == self.victoryLength:
                    return True
        return False
    
    def _rowVictoryCheck(self, chipType: InterFaceChip)->bool:
        """
        @param chipType, chip type we are checking victory for
        @returns bool, wether this chip has won or not vertically
        """
        for row in range(len(self.array)):
            count = 0
            for col in range(len(self.array)):
                # empty case 
                if len(self.array[col]) <= row:
                    count = 0
                else:
                    chip = self.array[col][row]
                # same color chip case
                    if chip.toString() == chipType.toString():
                        count +=1
                # differnet color chip case
                    else:
                        count = 0
                if count == self.victoryLength:
                    return True
        return False
    
    def _upDiagonalVictoryCheck(self, chipType: InterFaceChip)->bool:
        """
        @param chipType, chip type we are checking victory for
        @returns bool, wether this chip has won or not along the upDiagonal
        """

        # left col of the square is begin position 
        for row in range(len(self.array)):
            curPos = (0,row)
            count = 0
            while curPos[0]<2*self.victoryLength-1 and curPos[1]<2*self.victoryLength-1:
                # empty case 
                col = curPos[0]
                curRow = curPos[1]
                if len(self.array[col]) <= curRow:
                    count = 0
                else:
                    chip = self.array[col][curRow]
                # same color chip case
                    if chip.toString() == chipType.toString():
                        count +=1
                # differnet color chip case
                    else:
                        count = 0
                if count == self.victoryLength:
                    return True
                # increment
                curPos = (1+curPos[0],1+curPos[1]) 
        
        # bottom row of the square is begin position 
        for col in range(len(self.array)):
            curPos = (col,0)
            count = 0
            while curPos[0]<2*self.victoryLength-1 and curPos[1]<2*self.victoryLength-1:
                # empty case 
                curCol = curPos[0]
                curRow = curPos[1]
                if len(self.array[curCol]) <= curRow:
                    count = 0
                else:
                    chip = self.array[curCol][curRow]
                # same color chip case
                    if chip.toString() == chipType.toString():
                        count +=1
                # differnet color chip case
                    else:
                        count = 0
                if count == self.victoryLength:
                    return True
                # increment
                curPos = (1+curCol,1+curRow) 
        return False
                    
    def _downDiagonalVictoryCheck(self, chipType: InterFaceChip)->bool:
        """
        @param chipType, chip type we are checking victory for
        @returns bool, wether this chip has won or not along the upDiagonal
        """

        # left col of the square is begin position 
        for row in range(len(self.array)):
            curPos = (0,row)
            count = 0
            while curPos[0]>= 0 and curPos[1] >=0:
                # empty case 
                col = curPos[0]
                curRow = curPos[1]
                if len(self.array[col]) <= curRow:
                    count = 0
                else:
                    chip = self.array[col][curRow]
                # same color chip case
                    if chip.toString() == chipType.toString():
                        count +=1
                # differnet color chip case
                    else:
                        count = 0
                if count == self.victoryLength:
                    return True
                # increment
                
                curPos = (curPos[0]+1,curPos[1]-1) 
        
        # top row of the square is begin position 
        for col in range(len(self.array)):
            curPos = (col,len(self.array)-1)
            count = 0
            curCol, curRow = curPos
            while curCol <= len(self.array)-1 and curRow >= 0:
                # empty case 
                if len(self.array[curCol]) <= curRow or len(self.array[curCol]) == 0:
                    count = 0
                else:
                    chip = self.array[curCol][curRow]
                # same color chip case
                    if chip.toString() == chipType.toString():
                        count +=1
                # differnet color chip case
                    else:
                        count = 0
                if count == self.victoryLength:
                    return True
                # increment
                curCol = curCol + 1
                curRow = curRow - 1          
        return False


# board = BackEndBoard(2)
# board.placeChip(0,RedChip())
# board.placeChip(0,RedChip())
# print(board.showBoard())
# print(board.showBoardList())
    