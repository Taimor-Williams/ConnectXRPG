import pygame
from backEndBoard_Module import *
from chip_Module import *
import os, sys, glob
from enum import Enum
from button_Module import *

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
    # window: pygame.surface.Surface
    rect: pygame.Rect
    curChip: InterFaceChip
    aspectRatio: int

    def __init__(self, board: BackEndBoard, window: pygame.Surface, squareSize = 60) -> None:
        self.board = board
        self.aspectRatio = squareSize
        self.width = len(board.array)*self.aspectRatio
        self.height = len(board.array)*self.aspectRatio
        x = 0
        y = 0
        self.rect = pygame.Rect(x, y, self.width, self.height)
        # self.window = window
        self.curChip = BlackChip()
        self.colorIdle = Colors.blue.value
        self.colorHover = Colors.green.value
        
    
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

    def drawBoard(self, screen: pygame.surface.Surface, mousePos: tuple[int,int]):
        """
        @effects, draws the gameboard should look like a bunch of lines outlining each square
        """
        color = self.colorIdle
        if self.rect.collidepoint(mousePos):
            color = self.colorHover
        pygame.draw.rect(screen, color, self.rect)
        # font = pygame.font.Font(None, 30)
        # fontColor = (255, 255, 255)
        # text_surface = font.render(self.text, True, fontColor)
        # text_rect = text_surface.get_rect(center=self.rect.center)
        # screen.blit(text_surface, text_rect)

        for col in range(len(self.board.array)+1):
            # draw vert lines
            pygame.draw.line(screen, Colors.blue.value, (self.aspectRatio*col,0), 
            (self.aspectRatio*col, self.height))
            # draw horizontal lines
            pygame.draw.line(screen, Colors.blue.value, (0,self.aspectRatio*col), 
            (self.width, self.aspectRatio*col))
    
    def drawChips(self, screen: pygame.surface.Surface):
        """
        @effects, draws the chips in the board
        """
        for col, array in enumerate(self.board.array):
            for row, chip in enumerate(array):
                # have to flip curRow to put the chips on bottom of the grid
                curRow = len(self.board.array)-row-1
                if isinstance(chip, RedChip):
                    pygame.draw.circle(screen, Colors.red.value, (col*self.aspectRatio+self.aspectRatio/2,
                    curRow*self.aspectRatio+self.aspectRatio/2), self.aspectRatio/2, 1)
                if isinstance(chip, BlackChip):
                    pygame.draw.circle(screen, Colors.green.value, (col*self.aspectRatio+self.aspectRatio/2,
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

  



        
