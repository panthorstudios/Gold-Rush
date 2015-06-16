from random import random
from random import randint
import pygame
from pygame.locals import *


class InputHandler(object):

    space_press=False
    key_press=None
    exit_action=False
    arrow_press=None

    def __init__(self):
        pass
 
    def reset(self):
        self.key_press=None
        self.space_press=False
        self.arrow_press=None

    def check(self):
        for event in pygame.event.get():
            self.key_press=None
            if event.type == QUIT:
                self.exit_action=True 
            elif event.type == KEYDOWN:
                self.key_press=event.key
                if event.key == K_ESCAPE:
                    self.exit_action=True 
                elif event.key in (K_RIGHT,K_LEFT,K_UP,K_DOWN):
                    self.arrow_press = event.key
                elif event.key == K_SPACE:
                    self.space_press = True
            elif event.type == KEYUP:
                if event.key in (K_RIGHT,K_LEFT,K_UP,K_DOWN):
                    if self.arrow_press == event.key:
                        self.arrow_press = None
                elif event.key == K_SPACE:
                    self.space_press=False
                elif self.key_press==event.key:
                    self.key_press=None
 

