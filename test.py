from backEndBoard_Module import *
from chip_Module import *
from solvedAI_Module import *
"""
Testing Strategy 
    InterfaceChip:
        constructor():
        toString():
            partiton on redChip, blackChip
"""

"""
Testing Strategy
    backEndBoard:
        placeChip():
            partition on column: column full, column empty, column neither full or empty
            parrition on chip color: black,red
        victoryCheck(RedChip()):
            partition on victoryLength: 4,5
            partition on won: True, False
            partition on victoryType: verticle, horizontal, diagonalUp, diagnolDown
        victortCheckBlack():
            partition on victoryLength: 4,5
            partition on won: True, False
            partition on victoryType: verticle, horizontal, diagonalUp, diagnolDown
        showBoardList():
            partion on chip placement: verticle, horizontal
"""

"""
Testing Strategy
    SolvedAI:
       evaluateWindow():
            partition on window: horizontal, verticle, updiagnoal, downdiagnol
            parrition on chip color: black,red
"""

# InterfaceChip
# toString
def test_InterFaceChip_toString_redChip():
    redChip = RedChip()
    assert(redChip.toString() == "R")

def test_InterFaceChip_toString_blackChip():
    blackChip = BlackChip()
    assert(blackChip.toString() == "B")


# backEndBoard
# placeChip():
def test_BackEndBoard_placeChip_Red():
    redChip = RedChip()
    board = BackEndBoard(4)
    board.placeChip(0, redChip)
    assert(board.showColumn(0) == ['R'])

def test_BackEndBoard_placeChip_Black():
    blackChip = BlackChip()
    board = BackEndBoard(4)
    board.placeChip(0, blackChip)
    assert(board.showColumn(0) == ['B'])

def test_BackEndBoard_placeChip_full():
    board = BackEndBoard(2)
    board.placeChip(0, BlackChip())
    board.placeChip(0, RedChip())
    board.placeChip(0, BlackChip())
    assert(len(board.showColumn(0)) == 3)
    board.placeChip(0,RedChip())
    assert(board.showColumn(0)[-1] == 'B')

def test_BackEndBoard_placeChip_empty():
    board = BackEndBoard(2)
    assert(len(board.showColumn(0)) == 0)
    board.placeChip(0,RedChip())
    assert(board.showColumn(0)[-1] == 'R')

def test_BackEndBoard_placeChip_notFullorEmpty():
    board = BackEndBoard(2)
    assert(len(board.showColumn(0)) == 0)
    board.placeChip(0,BlackChip())
    assert(len(board.showColumn(0)) == 1)
    assert(board.showColumn(0)[-1] == 'B')
    board.placeChip(0,RedChip())
    assert(len(board.showColumn(0)) == 2)
    assert(board.showColumn(0)[-1] == 'R')

# victoryCheck red 
# true and false
def test_BackEndBoard_victoryCheckRed_true():
    board = BackEndBoard(4)
    board.placeChip(0,RedChip())
    board.placeChip(0,RedChip())
    board.placeChip(0,RedChip())
    board.placeChip(0,RedChip())
    assert(board.victoryCheck(RedChip()))

def test_BackEndBoard_victoryCheckRed_false():
    board = BackEndBoard(4)
    board.placeChip(0,RedChip())
    board.placeChip(0,RedChip())
    board.placeChip(0,RedChip())
    assert(board.victoryCheck(RedChip()) != True)

# length
def test_BackEndBoard_victoryCheckRed_victoryLength5():
    board = BackEndBoard(5)
    board.placeChip(0,RedChip())
    board.placeChip(0,RedChip())
    board.placeChip(0,RedChip())
    board.placeChip(0,RedChip())
    board.placeChip(0,RedChip())
    assert(board.victoryCheck(RedChip()))

def test_BackEndBoard_victoryCheckRed_victoryLength2():
    board = BackEndBoard(2)
    board.placeChip(0,RedChip())
    board.placeChip(0,RedChip())
    assert(board.victoryCheck(RedChip()))

# type
def test_BackEndBoard_victoryCheckRed_Verticle():
    board = BackEndBoard(2)
    board.placeChip(0,RedChip())
    board.placeChip(0,RedChip())
    assert(board.victoryCheck(RedChip()))

def test_BackEndBoard_victoryCheckRed_Horizontal():
    board = BackEndBoard(2)
    board.placeChip(0,RedChip())
    board.placeChip(1,RedChip())
    assert(board.victoryCheck(RedChip()))

def test_BackEndBoard_victoryCheckRed_upDiagnol_1():
    board = BackEndBoard(2)
    board.placeChip(0,RedChip())
    board.placeChip(1,BlackChip())
    board.placeChip(1,RedChip())
    print(board.array)
    print(board.array[1][1].toString())
    assert(board.victoryCheck(RedChip()))

def test_BackEndBoard_victoryCheckRed_upDiagnol_2():
    board = BackEndBoard(2)
    board.placeChip(1,RedChip())
    board.placeChip(2,BlackChip())
    board.placeChip(2,RedChip())
    assert(board.victoryCheck(RedChip()))

def test_BackEndBoard_victoryCheckRed_downDiagnol():
    board = BackEndBoard(2)
    board.placeChip(0,BlackChip())
    board.placeChip(0,RedChip())
    board.placeChip(1,RedChip())
    assert(board.victoryCheck(RedChip()))

# def test_BackEndBoard_victoryCheckRed_downDiagnol_2():
#     board = BackEndBoard(2)
#     board.placeChip(3,BlackChip())
#     board.placeChip(3,BlackChip())
#     board.placeChip(3,BlackChip())
#     board.placeChip(3,BlackChip())
#     board.placeChip(3,RedChip())
#     board.placeChip(4,BlackChip())
#     board.placeChip(4,BlackChip())
#     board.placeChip(4,BlackChip())
#     board.placeChip(4,RedChip())
#     print(board.array)
#     print(board.showBoard())
#     assert(board.victoryCheck(RedChip()))

def test_showBoardList_horizontal():
    board = BackEndBoard(2)
    board.placeChip(0, BlackChip())
    board.placeChip(1, RedChip())
    board.placeChip(2, BlackChip())
    assert(board.showBoardList() == [[0, 0, 0], [0, 0, 0], [1, 2, 1]])

def test_showBoardList_verticle():
    board = BackEndBoard(2)
    board.placeChip(0, BlackChip())
    board.placeChip(0, RedChip())
    board.placeChip(0, BlackChip())
    assert(board.showBoardList() == [[1, 0, 0], [2, 0, 0], [1, 0, 0]])

"""
Testing Strategy
    SolvedAI:
       evaluateWindow():
            partition on window: horizontal, verticle, updiagnoal, downdiagnol
            parrition on chip color: black,red
        scorePosition():
            partition on #chips, 1,2,3,4
            partition on chip color: black, red
        placeChip():
            partition on col
            partition on array emptyness
"""

def test_solvedAI_horizontal():
    board = BackEndBoard(2)
    ai = solvedAI()
    board.placeChip(0,BlackChip())
    assert(ai._getHorizontal(board) == [[0, 0], [0, 0], [0, 0], [0, 0], [1, 0], [0, 0]])

def test_solvedAI_horizontal_2(): 
    board = BackEndBoard(4)
    ai = solvedAI()
    board.placeChip(0, BlackChip())
    board.placeChip(0, RedChip())
    assert(ai._getHorizontal(board) == [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], 
                                        [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], 
                                        [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
                                          [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [2, 0, 0, 0], [0, 0, 0, 0], 
                                          [0, 0, 0, 0], [0, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
def test_solvedAI_vertical():
    board = BackEndBoard(2)
    ai = solvedAI()
    board.placeChip(0,BlackChip())
    assert(ai._getVertical(board) == [[0, 0], [0, 0], [0, 0], [0, 1], [0, 0], [0, 0]])

def test_solvedAI_getPositiveDiagnol():
    board = BackEndBoard(2)
    ai = solvedAI()
    board.placeChip(0,BlackChip())
    assert(ai._getPositiveDiagnol(board) == [[0, 0], [0, 0], [1, 0], [0, 0],])

def test_solvedAI_getNegativeDiagnol():
    board = BackEndBoard(2)
    ai = solvedAI()
    board.placeChip(0,BlackChip())
    assert(ai._getNegativeDiagnol(board) == [[0, 0], [0, 0], [0, 0], [0, 0],])

def test_solvedAI_getNegativeDiagnol():
    board = BackEndBoard(2)
    ai = solvedAI()
    board.placeChip(0,BlackChip())
    assert(ai._getNegativeDiagnol(board) == [[0, 0], [0, 0], [0, 0], [0, 0],])

def test_solvedAI_score_1():
    board = BackEndBoard(4)
    ai = solvedAI()
    board.placeChip(0,BlackChip())
    board.placeChip(0,BlackChip())
    print(ai.scorePosition(board, BlackChip))
    assert(ai.scorePosition(board, BlackChip) == 2)

def test_solvedAI_score_2():
    board = BackEndBoard(4)
    ai = solvedAI()
    board.placeChip(0,BlackChip())
    board.placeChip(0,BlackChip())
    print(ai.scorePosition(board, BlackChip))
    assert(ai.scorePosition(board, BlackChip) == 2)

def test_solvedAI_score_3():
    board = BackEndBoard(4)
    ai = solvedAI()
    board.placeChip(0,BlackChip())
    board.placeChip(0,BlackChip())
    board.placeChip(0,BlackChip())
    print(ai.scorePosition(board, BlackChip))
    assert(ai.scorePosition(board, BlackChip) == 7)

def test_solvedAI_score_4():
    board = BackEndBoard(4)
    ai = solvedAI()
    board.placeChip(0,BlackChip())
    board.placeChip(0,BlackChip())
    board.placeChip(0,BlackChip())
    board.placeChip(0,BlackChip())
    print(ai.scorePosition(board, BlackChip))
    assert(ai.scorePosition(board, BlackChip) == 107)

# def test_solvedAI_minmax_win_vert():
#     board = BackEndBoard(4)
#     ai = solvedAI()
#     board.placeChip(0,BlackChip())
#     board.placeChip(0,BlackChip())
#     board.placeChip(0,BlackChip())
#     assert(ai._minMaxAlgorithim(board,4,-9999,+9999,True, BlackChip()) == (0, 9999999))

# def test_solvedAI_minmax_win_horiz():
#      board = BackEndBoard(4)
#      ai = solvedAI()
#      board.placeChip(0,BlackChip())
#      board.placeChip(1,BlackChip())
#      board.placeChip(2,BlackChip())
#      print(ai._minMaxAlgorithim(board,4,-9999,+9999,True, BlackChip()))
#      assert(ai.scorePosition(board, BlackChip) == (3, 9999999))

def test_solvedAI_minmax_win_vert():
    board = BackEndBoard(4)
    ai = solvedAI()
    board.placeChip(0,BlackChip())
    board.placeChip(0,BlackChip())
    board.placeChip(0,BlackChip())
    npBoard = np.array(board.showBoardList())
    assert(ai.minMaxAlgorithimNumpy(npBoard,1,True)[0] == 0)

def test_solvedAI_minmax_win_horiz():
     board = BackEndBoard(4)
     ai = solvedAI()
     board.placeChip(0,BlackChip())
     board.placeChip(1,BlackChip())
     board.placeChip(2,BlackChip())
     npBoard = np.array(board.showBoardList())
     assert(ai.minMaxAlgorithimNumpy(npBoard,1,True)[0] == 3)


def test_solvedAI_minmax_win_horiz_block():
     board = BackEndBoard(4)
     ai = solvedAI()
     board.placeChip(0,BlackChip())
     board.placeChip(1,BlackChip())
     board.placeChip(2,BlackChip())
     npBoard = np.array(board.showBoardList())
     assert(ai.minMaxAlgorithimNumpy(npBoard,1,False)[0] == 3)

def test_solvedAI_minmax_win_horiz_block_1():
     board = BackEndBoard(4)
     ai = solvedAI()
     board.placeChip(0,BlackChip())
     board.placeChip(1,BlackChip())
     board.placeChip(2,BlackChip())
     npBoard = np.array(board.showBoardList())
     assert(ai.minMaxAlgorithimNumpy(npBoard,1,False)[0] == 3)

# def test_solvedAI_minmax_win_horiz_block_2():
#      board = BackEndBoard(4)
#      ai = solvedAI()
#      board.placeChip(0,BlackChip())
#      board.placeChip(1,BlackChip())
#      board.placeChip(0,RedChip())
#      board.placeChip(0,RedChip())
#      board.placeChip(0,RedChip())
#      npBoard = np.array(board.showBoardList())
#      assert(ai.minMaxAlgorithimNumpy(npBoard,1,True) == (1, 0))

def test_solvedAI_minmax_win_vertical_block():
     board = BackEndBoard(4)
     ai = solvedAI()
     board.placeChip(1,BlackChip())
     board.placeChip(1,BlackChip())
     board.placeChip(0,RedChip())
     board.placeChip(0,RedChip())
     board.placeChip(0,RedChip())
     npBoard = np.array(board.showBoardList())
     assert(ai.minMaxAlgorithimNumpy(npBoard,1,True)[0] == 0)

def test_solvedAI_minmax_win_vertical_block_1():
     board = BackEndBoard(4)
     ai = solvedAI()
     board.placeChip(0,BlackChip())
     board.placeChip(0,BlackChip())
     board.placeChip(0,BlackChip())
     board.placeChip(2,RedChip())
     board.placeChip(3,RedChip())
     npBoard = np.array(board.showBoardList())
     assert(ai.minMaxAlgorithimNumpy(npBoard,2,False)[0] == 0)
     


def test_solvedAI_placeChip_col_empty():
    board = BackEndBoard(4)
    ai = solvedAI()
    board.placeChip(0,BlackChip())
    npBoard = np.array(board.showBoardList())
    ai.placeChip(npBoard, 1, 1)
    print(npBoard)
    assert npBoard[6][1]== 1, ""

def test_solvedAI_placeChip_col_nonEmpty():
    board = BackEndBoard(4)
    ai = solvedAI()
    board.placeChip(0,BlackChip())
    npBoard = np.array(board.showBoardList())
    ai.placeChip(npBoard, 0, 1)
    print(npBoard)
    assert npBoard[5][0]== 1, ""














