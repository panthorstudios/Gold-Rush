import pygame

class Explosion(pygame.sprite.Sprite):
    EXPLOSION_SIZE=128
    EXPLOSION_FRAMES=38
    SQUARE_SIZE=32
    XYADJUST = 48 # (EXPLOSION_SIZE // 2) - (SQUARE_SIZE // 2)  
    SHEET_WIDTH=8
    IMAGE_FILE='images/explosion_38f_128x128.png'

    def __init__(self,left,top):
        self.BOARD_LEFT=left
        self.BOARD_TOP=top
        pygame.sprite.Sprite.__init__(self)
        
        self.src_image=pygame.image.load(self.IMAGE_FILE).convert_alpha() 

        self.set_location(0,0)
        self.exploding=False
        self.rect = pygame.Rect((0,0,self.EXPLOSION_SIZE,self.EXPLOSION_SIZE))
        self.curr_image = pygame.Surface(self.rect.size,flags=pygame.SRCALPHA)

    def set_location(self,x,y):
        self.x=x
        self.y=y
        posx=self.BOARD_LEFT+(x*self.SQUARE_SIZE)-self.XYADJUST
        posy=self.BOARD_TOP+(y*self.SQUARE_SIZE)-self.XYADJUST
        self.position=(posx,posy)

    def start_explosion(self,x,y):
        self.seqno=0
        self.exploding=True
        self.set_location(x,y)

    def update(self,deltat):
        if self.exploding:

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

    def updateold(self,deltat):
        self.rect=self.image.get_rect() #self.src_image.get_rect()
        self.rect.left=self.position[0]
        self.rect.top=self.position[1]


