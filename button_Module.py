import pygame
from backEndBoard_Module import *
from chip_Module import *
import os, sys, glob
from enum import Enum
import tkinter as tk

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
        
        