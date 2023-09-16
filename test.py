from backEndBoard_Module import *
from chip_Module import *
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
    board.placeChip(0, RedChip())
    board.placeChip(0, BlackChip())
    assert(len(board.showColumn(0)) == 5)
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

def test_BackEndBoard_victoryCheckRed_downDiagnol_2():
    board = BackEndBoard(2)
    board.placeChip(3,BlackChip())
    board.placeChip(3,BlackChip())
    board.placeChip(3,BlackChip())
    board.placeChip(3,BlackChip())
    board.placeChip(3,RedChip())
    board.placeChip(4,BlackChip())
    board.placeChip(4,BlackChip())
    board.placeChip(4,BlackChip())
    board.placeChip(4,RedChip())
    print(board.array)
    print(board.showBoard())
    assert(board.victoryCheck(RedChip()))






