import pygame
from backEndBoard_Module import *
from chip_Module import *
import os, sys, glob
from enum import Enum
import tkinter as tk

class Colors(Enum):
    """
    stores the colors
    """
    red = (200,0,0)
    blue = (0,0,255)
    white = (255,255,255)
    green = (0,255,0)
    orange= (200, 100, 0)
    black = (0,0,0)

class FrontEndGameBoard:
    """
    Abstraction function(board, window, width, height, aspectRatio, curChip) = 
        a clickable gameBoard. It exist within window "window". Has a height "len(board.array)*aspectRatio" and 
        width "len(board.array)*aspectRatio". aspectRatio is an adjustable scaling size of the board. 
        curChip is the current chip that the board is waiting to place. 
    
    Rep invarient:
        true

    Protection from rep exposure:
        isClicked():
            @params, immutable
            @returns, void
        showPopup():
            @params: immutable
            @returns: void
        Trivial:
            drawBoard():
            drawChips():
            victoryCheck():
            restart():
    """
    board: BackEndBoard
    window: pygame.surface.Surface
    width: int
    height: int
    aspectRatio: int
    curChip: InterFaceChip

    def __init__(self, board: BackEndBoard, window: pygame.Surface) -> None:
        self.board = board
        self.aspectRatio = 40
        self.width = len(board.array)*self.aspectRatio
        self.height = len(board.array)*self.aspectRatio
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.window = window
        self.curChip = BlackChip()
    
    def clicked(self, mousePos: tuple[int,int]):
        """
        @params mousePos, curposition of the mouse on board, if curPosition is inside board
        place a chip on said position
        @effects, change the current chip to the opposite color
        @handles, if mouse is outside connect board do nothing
        @handles if column is full do nothing
        """

        if not self._isClicked(mousePos):
            return 
        
        #  mouse is inside board
        curCol,curRow = self._convertMouseToBoard(mousePos)
        self.board.placeChip(curCol, self.curChip)
        self._nextChip()
        self.saveGame()

    def drawBoard(self):
        """
        @effects, draws the gameboard should look like a bunch of lines outlining each square
        """
        
        for col in range(len(self.board.array)+1):
            # draw vert lines
            pygame.draw.line(self.window, Colors.blue.value, (self.aspectRatio*col,0), 
            (self.aspectRatio*col, self.height))
            # draw horizontal lines
            pygame.draw.line(self.window, Colors.blue.value, (0,self.aspectRatio*col), 
            (self.width, self.aspectRatio*col))
    
    def drawChips(self):
        """
        @effects, draws the chips in the board
        """
        for col, array in enumerate(self.board.array):
            for row, chip in enumerate(array):
                # have to flip curRow to put the chips on bottom of the grid
                curRow = len(self.board.array)-row-1
                if isinstance(chip, RedChip):
                    pygame.draw.circle(self.window, Colors.red.value, (col*self.aspectRatio+self.aspectRatio/2,
                    curRow*self.aspectRatio+self.aspectRatio/2), self.aspectRatio/2, 1)
                if isinstance(chip, BlackChip):
                    pygame.draw.circle(self.window, Colors.green.value, (col*self.aspectRatio+self.aspectRatio/2,
                    curRow*self.aspectRatio+self.aspectRatio/2), self.aspectRatio/2, 1)
    
    def victoryCheck(self)->bool:
        """
        @returns bool, if either color won
        """
        if self.board.victoryCheck(BlackChip()):
            return True
        if self.board.victoryCheck(RedChip()):
            return True
        return False
    
    def showPopup(self, message):
        """
        @params message, the txt we are displaying in the popup window
        @effects, create a popup in center of screen of dimensions 300,200
        """
        popup_width = 300
        popup_height = 200
        x,y,windowWidth, windowHeight = self.window.get_rect()
        screen_width = windowWidth
        screen_height = windowHeight
        popup_x = (screen_width - popup_width) // 2
        popup_y = (screen_height - popup_height) // 2

        popup_surface = pygame.Surface((popup_width, popup_height))
        popup_surface.fill((255, 255, 255))  # White background

        font = pygame.font.Font(None, 30)
        text = font.render(message, True, (0, 0, 0))  # Black text
        text_rect = text.get_rect(center=(popup_width // 2, popup_height // 2))

        popup_surface.blit(text, text_rect)

        self.window.blit(popup_surface, (popup_x, popup_y))
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    return
                
    def restart(self):
        """
        @effects, resets the board
        """
        self.board = BackEndBoard(self.board.victoryLength)
        self.curChip = BlackChip()

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
      # do your stuff

        
    # private functions
    
    def _convertMouseToBoard(self, mousePos: tuple[int,int])-> tuple[int,int]:
        """
        @param mousePos, position of mouse on screen
        @returns col, col that corresponds to mouse position
        """
        x,y = mousePos
        col, row = x//self.aspectRatio, y//self.aspectRatio
        return col, row

    def _nextChip(self):
        """
        @function, show a new chip that's different from the one just placed
        identify chip by toString value()
        """
        if self.curChip.toString() == 'R':
            self.curChip = BlackChip()
        else:
            self.curChip = RedChip()
        
    def _isClicked(self, mousePos: tuple[int,int])->bool:
        """
        @returns, whether the board has been clicked
        """
        # check to see if mouse is inside board
        x,y = mousePos
        if x > self.width:
            return False
        if y > self.height:
            return False
        return True

class Button:
    """
    Abstraction Function(colorIdle, colorHover, text, rect) = 
        a clickable button that performs some action "action" when clicked.
        button exist within rectangle "rect", has idle color "colorIdle" 
        and hover color "colorHover". Button displays text "text"

    Rep Invarient:
        true

    Protection from rep exposure:
        draw():
            @params screen, mutable surface object however the surface object 
            has no reference to change the button
            @params mousePos, immutable tuple
            @returns void
        isClicked():
            @params, void
            @returns bool, immutable
    """

    colorIdle: tuple[int,int,int]
    colorHover: tuple[int,int,int]
    text: str
    rect: pygame.Rect

    def __init__(self, x, y, width, height, text, colorIdle, colorHover, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.colorIdle = colorIdle
        self.colorHover = colorHover
        self.action = action

    def draw(self, screen: pygame.surface.Surface, mousePos: tuple[int,int]):
        """
        @params screen, surface we are drawing button on
        @params mousePos, if mouse is currently above button then show highlight color
        """
        color = self.colorIdle
        if self.rect.collidepoint(mousePos):
            color = self.colorHover
        pygame.draw.rect(screen, color, self.rect)
        font = pygame.font.Font(None, 30)
        fontColor = (255, 255, 255)
        text_surface = font.render(self.text, True, fontColor)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def _isClicked(self, mousePos)->bool:
        """
        @params mousePos
        @returns bool, true mouse is currently colliding with button
        """
        return self.rect.collidepoint(mousePos)
    
    def clicked(self, mousePos: tuple[int,int]):
        """
        @effects performs action the button is made for
        """
        if not self._isClicked(mousePos):
            return
        
        self.action()
        
class SingletonPattern():
    """
    an encapsalating class that does everything 
    it should format everything correctly
    """

# button functions
def restart_function():
    # Reset game state or perform restart actions here
    curSize = frontEndgameBoard.board.victoryLength
    frontEndgameBoard = FrontEndGameBoard(BackEndBoard(curSize), window)

# setup constants

pygame.init()
circleX = 100
circleY = 100
radius = 10
WINDOW_HEIGHT = 620
WINDOW_WIDTH = 620
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Connect4 Project')
running=True
victory = False
gameBoard = BackEndBoard(6)
frontEndgameBoard = FrontEndGameBoard(gameBoard, window)
restart_button = Button(350, 450, 100, 50, "Restart", (0, 100, 0), (0, 200, 0), restart_function)

# the ending is the best escape

while running:
    window.fill((0, 0, 0))
    frontEndgameBoard.drawBoard()
    frontEndgameBoard.drawChips()
    restart_button.draw(window, pygame.mouse.get_pos())
    frontEndgameBoard.loadGame()

    # events
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type ==pygame.MOUSEBUTTONDOWN:
            x,y = pygame.mouse.get_pos()
            frontEndgameBoard.clicked((x,y))
            victory = frontEndgameBoard.victoryCheck()
            restart_button.clicked((x,y))
        # Show popup when needed
        if victory:  # Replace with your condition
            frontEndgameBoard.showPopup("This is a popup!")
        
            
    pygame.display.flip()
pygame.quit()
    


        
