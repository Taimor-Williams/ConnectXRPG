from button_Module import *
from frontEndBoard import *
import tkinter as tk
import csv  
from tkinter.filedialog import askdirectory
import pandas as pd
from solvedAI_Module import *

class SingletonPattern():
    """
    an encapsalating class that does everything 
    it should format everything correctly
    """
    restartButton: "Button"
    optionsButton: "Button"
    nextButton: "Button"
    saveButton: "Button"
    loadButton: "Button"
    frontEndgameBoard: "FrontEndGameBoard"
    titleDisplay: "TitleDisplay"
    window: pygame.Surface

    def __init__(self) -> None:
        # game variables
        boardSize = 4
        SquareSize = 60
        AspectRatio = 3/2
        WINDOW_HEIGHT = (boardSize*2+1)*SquareSize
        WINDOW_WIDTH = (boardSize*2+1)*AspectRatio*SquareSize
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        # gameBoard
        gameBoard = BackEndBoard(boardSize)
        self.frontEndgameBoard = FrontEndGameBoard(gameBoard, self.window)

        # buttons
        xPositionButtons = WINDOW_HEIGHT+(WINDOW_WIDTH-WINDOW_HEIGHT)/2
        yPositionButtons = WINDOW_HEIGHT/6
        
        self.titleDisplay = TitleDisplay(WINDOW_HEIGHT, 0, WINDOW_WIDTH-WINDOW_HEIGHT, 
                                    2*SquareSize)
        self.restartButton = Button(xPositionButtons-3*SquareSize/2, 2*yPositionButtons-1.5*SquareSize/2, 3*SquareSize, 
                                    1.5*SquareSize, "Restart", Colors.darkGreen.value, Colors.green.value)
        self.optionsButton = Button(xPositionButtons-3*SquareSize/2, 3*yPositionButtons-1.5*SquareSize/2, 3*SquareSize,
                                     1.5*SquareSize, "Options", Colors.darkGreen.value, Colors.green.value)
        self.loadButton = Button(xPositionButtons-3*SquareSize/2, 4*yPositionButtons-1.5*SquareSize/2, 3*SquareSize, 
                                 1.5*SquareSize, "load", Colors.darkGreen.value, Colors.green.value)
        self.saveButton = Button(xPositionButtons-3*SquareSize/2, 5*yPositionButtons-1.5*SquareSize/2, 3*SquareSize, 
                                 1.5*SquareSize, "save", Colors.darkGreen.value, Colors.green.value)
    
    def draw(self):
        """
        @params none
        @returns none
        @effects, calls the draw function for all Buttons and frames
        """
        self.window.fill((0, 0, 0))
        self.frontEndgameBoard.drawBoard(self.window, pygame.mouse.get_pos())
        self.frontEndgameBoard.drawChips(self.window)
        self.titleDisplay.draw(self.window, pygame.mouse.get_pos())
        self.restartButton.draw(self.window, pygame.mouse.get_pos())
        self.optionsButton.draw(self.window, pygame.mouse.get_pos())
        self.saveButton.draw(self.window,pygame.mouse.get_pos())
        self.loadButton.draw(self.window, pygame.mouse.get_pos())
    
    def clicked(self, mousePos: tuple[int,int]):
        """
        @effects, calls the clicked function for all buttons and frames
        """
        if self.frontEndgameBoard._isClicked(mousePos):
            self.frontEndgameBoard.clicked(mousePos)
            self.frontEndgameBoard._nextChip()
            self._makeMoveAI()
        # buttons
        if self.restartButton.isClicked(mousePos):
            self._restartButtonEffect()
        if self.optionsButton.isClicked(mousePos):
            print("help")
        if self.saveButton.isClicked(mousePos):
            self.saveGame()
        if self.loadButton.isClicked(mousePos):
            self.loadGame()
    
    def _makeMoveAI(self):
        """
        
        """
        Ai = solvedAI()
        backEndBoard = self.frontEndgameBoard.board
        npBoard = np.array(backEndBoard.showBoardList())
        move,score = Ai.minMaxAlgorithimNumpy(npBoard,2,False)
        print(npBoard)
        print(move,score)
        backEndBoard.placeChip(move, RedChip())

    # popups

    # buttonEffects
    def _restartButtonEffect(self):
        """
        
        """
        self.frontEndgameBoard.restart()

    def saveGame(self):
        """
        @effects, saves the current game to a csv file. Where the file is in the format
        example code:

        4, (B,1),(R,2),(B,3),(R,1)
        where 4 is the victoryLength
        and every tuple is a move that was made
        """
        fields = ['Move', 'VictoryLength'] 
        filename = 'savedGames/Game.csv'
        rows = []
        for move in self.frontEndgameBoard.board.moveList:
            rows.append([move, self.frontEndgameBoard.board.victoryLength])

        with open(filename, 'w') as csvfile:  
        # creating a csv writer object  
            csvwriter = csv.writer(csvfile)  
        # writing the fields  
            csvwriter.writerow(fields)  
        # writing the data rows  
            csvwriter.writerows(rows) 
            

        
    def loadGame(self):
        """
        @effects, load game board from saved games
        """
        self._restartButtonEffect()
        # load the csv file
        folder_path = '/Users/taimorwilliams/Desktop/Documents/Summer 2023/Connect4/savedGames/Game.csv'
        # opening the CSV file
        # with open('savedGames/Game.csv', mode ='r')as file:
        #     # reading the CSV file
        #     csvFile = csv.reader(file)
        #     # displaying the contents of the CSV file
        #     for lines in csvFile:
        #         print(lines)
        
        # reading the CSV file
        csvFile = pd.read_csv('savedGames/Game6.csv')
 
        # displaying the contents of the CSV file
        #
        moves = csvFile.loc[:,'Move']
        #
        for move in moves:
            color = move[2]
            number = move[6]
            self.frontEndgameBoard.autoClicked((color,number))
    
        

# setup constants

pygame.init()
pygame.display.set_caption('Connect4 Project')
running=True
victory = False
master = SingletonPattern()

# the ending is the best escape
while running:
    master.draw()
    # events
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type ==pygame.MOUSEBUTTONDOWN:
            x,y = pygame.mouse.get_pos()
            master.clicked((x,y))
        # Show popup when needed
        
        # if victory:  # Replace with your condition
        #     frontEndgameBoard.showPopup("This is a popup!")
    pygame.display.flip()
pygame.quit()
    
