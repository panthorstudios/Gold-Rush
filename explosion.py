import pygame

class Explosion(pygame.sprite.Sprite):

# sprite sheet image (8x5)
    IMAGE_FILE='assets/images/explosion_38f_128x128.png'

# these are related to the image config
    EXPLOSION_SIZE=128
    EXPLOSION_FRAMES=38
    SHEET_WIDTH=8
    SQUARE_SIZE=32
    def __init__(self,x,y):
# The square_size parameter is the size of one square
#   in the playing area (e.g. the size of a nugget)

        pygame.sprite.Sprite.__init__(self)

        self.XYADJUST=(self.EXPLOSION_SIZE//2) - (self.SQUARE_SIZE //2) 
        self.image_src=pygame.image.load(self.IMAGE_FILE) #.convert_alpha() 
        self.image=pygame.Surface((self.EXPLOSION_SIZE,self.EXPLOSION_SIZE),flags=pygame.SRCALPHA)       
        self.set_position(x,y)
        self.exploding=False

# Rect which contains current sprite
        self.rect = pygame.Rect((0,0,self.EXPLOSION_SIZE,self.EXPLOSION_SIZE))

    def set_position(self,x,y):
        posx=(x*self.SQUARE_SIZE)-self.XYADJUST
        posy=(y*self.SQUARE_SIZE)-self.XYADJUST
        self.position=(posx,posy)

    def explode(self,x,y):
        self.seqno=0
        self.exploding=True
        self.set_position(x,y)

    def update(self,deltat):
        expl=self.exploding
        if expl:
# First copy the appropriate sprite image to the main image
            irow=self.seqno // self.SHEET_WIDTH
            icol=self.seqno % self.SHEET_WIDTH
            self.image.blit(self.image_src,(0,0),(icol*self.EXPLOSION_SIZE,irow*self.EXPLOSION_SIZE,self.EXPLOSION_SIZE,self.EXPLOSION_SIZE)) 
            self.seqno += 1
            if self.seqno > self.EXPLOSION_FRAMES:
                self.exploding=False
                self.set_position(-1,-1)

            self.rect=self.image.get_rect()

            self.rect.left=self.position[0]
            self.rect.top=self.position[1]

