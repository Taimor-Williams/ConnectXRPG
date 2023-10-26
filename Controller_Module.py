from button_Module import *
from frontEndBoard import *
import tkinter as tk

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
    gameFrame: "FrontEndGameBoard"
    titleDisplay: "tileDisplay"
    window: pygame.Surface

    def __init__(self) -> None:
        # game variables
        boardSize = 6
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
        self.restartButton = Button(xPositionButtons-3*SquareSize/2, 2*yPositionButtons-1.5*SquareSize/2, 3*SquareSize, 1.5*SquareSize, "Restart", (0, 100, 0), (0, 200, 0), restart_function)
        self.optionsButton = Button(xPositionButtons-3*SquareSize/2, 3*yPositionButtons-1.5*SquareSize/2, 3*SquareSize, 1.5*SquareSize, "Options", (0, 100, 0), (0, 200, 0), restart_function)
        self.loadButton = Button(xPositionButtons-3*SquareSize/2, 4*yPositionButtons-1.5*SquareSize/2, 3*SquareSize, 1.5*SquareSize, "load", (0, 100, 0), (0, 200, 0), restart_function)    
        self.saveButton = Button(xPositionButtons-3*SquareSize/2, 5*yPositionButtons-1.5*SquareSize/2, 3*SquareSize, 1.5*SquareSize, "save", (0, 100, 0), (0, 200, 0), restart_function)

        
    
    def draw(self):
        """
        @params none
        @returns none
        @effects, calls the draw function for all Buttons and frames
        """
        self.window.fill((0, 0, 0))
        self.frontEndgameBoard.drawBoard(self.window, pygame.mouse.get_pos())
        self.frontEndgameBoard.drawChips(self.window)
        self.restartButton.draw(self.window, pygame.mouse.get_pos())
        self.optionsButton.draw(self.window, pygame.mouse.get_pos())
        self.saveButton.draw(self.window,pygame.mouse.get_pos())
        self.loadButton.draw(self.window, pygame.mouse.get_pos())
    
    def clicked(self, mousePos: tuple[int,int]):
        """
        @effects, calls the clicked function for all buttons and frames
        """
        self.frontEndgameBoard.clicked(mousePos)
        self.restartButton.clicked(mousePos)
        self.optionsButton.clicked(mousePos)
        self.saveButton.clicked(mousePos)
        self.loadButton.clicked(mousePos)

    def saveGame(self):
        """
        @effects, saves the current game to a text file. Where the file is in the format
        example code:

        4, (B,1),(R,2),(B,3),(R,1)
        where 4 is the victoryLength
        and every tuple is a move that was made
        """

        gameStr = self.board.saveGame()
        with open('readme.txt', 'w') as f:
            f.write(gameStr)
        
    def loadGame(self):
        """
        @effects, load game board from saved games
        """
        # for filename in os.listdir(os.getcwd()):
        #     print(filename)
        # good code
        folder_path = '/Users/taimorwilliams/Desktop/Documents/Summer 2023/Connect4'
        for filename in glob.glob(os.path.join(folder_path, '*.htm')):
            with open(filename, 'r') as f:
                text = f.read()
                print (filename)
                print (len(text))



# button functions
def restart_function():
    """
    reset game state
    """

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
    
