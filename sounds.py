import pygame
from pygame.locals import *

class Sounds(object):
    def __init__(self):
        self.bellsound=pygame.mixer.Sound('assets/sounds/bell.ogg')
        self.chargesound=pygame.mixer.Sound('assets/sounds/bomb.ogg')
        self.yeehawsound=pygame.mixer.Sound('assets/sounds/yeehaw.ogg')
        self.kachingsound=pygame.mixer.Sound('assets/sounds/kaching.ogg')


    def play_bell(self):
        self.bellsound.play()

    def play_boom(self):
        self.chargesound.play()

    def play_yeehaw(self):
        self.yeehawsound.play() 

    def play_kaching(self):
        self.kachingsound.play()




