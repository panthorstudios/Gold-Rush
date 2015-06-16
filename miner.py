import pygame

#from pygame.sprite import Sprite
#from pygame import image

class Miner(pygame.sprite.Sprite):
    MOVE_DELAY = 10 
    MINER_SIZE = 32
    MINER_IMAGE = 'assets/images/miner-%dpx.png' % MINER_SIZE
    EXPLOSION_DELAY = 30

    def __init__(self,x=0,y=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(self.MINER_IMAGE)
        self.image.convert_alpha()

        self.set_location(x,y)
        self.movecnt=self.MOVE_DELAY

# This delays movement based on the MOVE_DELAY value
    def can_move(self):
        if self.movecnt==0:
            self.movecnt=self.MOVE_DELAY
            return True
        else:
            self.movecnt -= 1
            return False

    def set_location(self,x,y):
        self.x=x
        self.y=y
        self.position=((x*self.MINER_SIZE),(y*self.MINER_SIZE))


    def update(self,deltat):
        self.rect=self.image.get_rect()
        self.rect.left=self.position[0]
        self.rect.top=self.position[1]

    def add_delay(self,d=30):
        self.movecnt+=d

