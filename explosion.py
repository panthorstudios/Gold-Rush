import pygame

class Explosion(pygame.sprite.Sprite):

# sprite sheet image (8x5)
    IMAGE_FILE='images/explosion_38f_128x128.png'

# these are related to the image config
    EXPLOSION_SIZE=128
    EXPLOSION_FRAMES=38
    SHEET_WIDTH=8

    def __init__(self,left,top,square_size):
# The square_size parameter is the size of one square
#   in the playing area (e.g. the size of a nugget)

        pygame.sprite.Sprite.__init__(self)
        self.SQUARE_SIZE=square_size
        self.XYADJUST=(self.EXPLOSION_SIZE//2) - (self.SQUARE_SIZE //2) 
        self.src_image=pygame.image.load(self.IMAGE_FILE).convert_alpha() 

        self.set_position(0,0)
        self.exploding=False
        self.rect = pygame.Rect((0,0,self.EXPLOSION_SIZE,self.EXPLOSION_SIZE))
        self.curr_image = pygame.Surface(self.rect.size,flags=pygame.SRCALPHA)

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
            self.curr_image.blit(self.src_image,(0,0),(icol*self.EXPLOSION_SIZE,irow*self.EXPLOSION_SIZE,self.EXPLOSION_SIZE,self.EXPLOSION_SIZE)) 

# Set image to main image
            self.image=self.curr_image

# Go to next sequence
            self.seqno += 1
            if self.seqno > self.EXPLOSION_FRAMES:
                self.exploding=False
            self.rect=self.image.get_rect()
            self.rect.left=self.position[0]
            self.rect.top=self.position[1]
        return expl

