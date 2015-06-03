import pygame

#from pygame.sprite import Sprite
#from pygame import image

class Miner(pygame.sprite.Sprite):
    MOVE_COUNTER = 5
    MINER_SIZE = 32
    def __init__(self,left,top):
        pygame.sprite.Sprite.__init__(self)
        self.BOARD_LEFT=left
        self.BOARD_TOP=top
        self.src_image = pygame.image.load('images/miner-%dpx.png' % self.MINER_SIZE) #.convert()
        self.set_location(8,0)
        self.movecnt=self.MOVE_COUNTER

    def update_move(self):
        if self.movecnt>0:
            self.movecnt -= 1

    def can_move(self):
        if self.movecnt==0:
            self.movecnt=self.MOVE_COUNTER
            return True
        else:
            return False

    def set_location(self,x,y):
        self.x=x
        self.y=y
        self.position=(self.BOARD_LEFT+(self.x*self.MINER_SIZE),self.BOARD_TOP+(self.y*self.MINER_SIZE))


    def update(self,deltat):
        self.image=self.src_image
        self.rect=self.src_image.get_rect()
        self.rect.left=self.position[0]
        self.rect.top=self.position[1]


