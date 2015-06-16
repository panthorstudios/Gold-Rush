import pygame
from pygame.locals import *

class GameScreen(object):
    BOARD_LEFT = 20
    BOARD_TOP = 130
    SQUARE_SIZE = 32
    BLACK = (0,0,0)
    GREEN=(128,255,128)
    YELLOW=(255,255,128)
    RED=(255,128,128)
    FRAMES_PER_SECOND = 30

    ASSAY_X = 540
    ASSAY_Y = 84
    CHARGES_X = 180 
    CASH_X = 20
    CASH_OFFSET = 30 
    GOLD_X = 16
    CHARGES_OFFSET = 32
    HEALTH_X =CHARGES_X + 40
    TITLE_X = 340
    board=None

    def __init__(self,title,width,height):
        self.screen=pygame.display.set_mode((width,height))
        pygame.display.set_caption(title)

        self.digits=pygame.image.load('assets/images/digits.png')

# load background image 
        self.soil=pygame.image.load('assets/images/background.png')
        self.opening=pygame.image.load('assets/images/begin.png')
        self.gameover=pygame.image.load('assets/images/gameover.png')

        self.bg=pygame.image.load('assets/images/background.png')
        self.all_sprites=pygame.sprite.Group()


# create surface to blit sprites etc.
        self.gamearea=pygame.Surface(self.bg.get_size()) #, flags=pygame.SRCALPHA)

        self.board=None

# currently 2 nugget images
        self.nuggets=[]
        self.nuggets.append(pygame.image.load('assets/images/gold01-%dpx.png' % self.SQUARE_SIZE))
        self.nuggets.append(pygame.image.load('assets/images/gold02-%dpx.png' % self.SQUARE_SIZE))

# title image
        text=pygame.image.load('assets/images/text_title.png')
        self.screen.blit(text,(self.TITLE_X,self.BOARD_LEFT))

# assay office image
        self.office=pygame.image.load('assets/images/assayoffice.png')
        self.screen.blit(self.office,(self.ASSAY_X+self.BOARD_LEFT,self.ASSAY_Y))
 
# add "Gold"
        text=pygame.image.load('assets/images/nugget.png')
        self.screen.blit(text,(self.GOLD_X,self.BOARD_LEFT))
        self.display_gold()

# add "Cash"
        text=pygame.image.load('assets/images/text_cash.png')
        self.screen.blit(text,(self.CASH_X,66))
        self.display_cash()

# add "Charges"
        text=pygame.image.load('assets/images/dynamite.png')
        self.screen.blit(text,(self.CHARGES_X,16))
        self.display_charges()

# add "Miner head"
        text=pygame.image.load('assets/images/miner_head.png')
        self.screen.blit(text,(self.CHARGES_X,66))
        self.display_health()
# redraw background each time
        self.bg.blit(self.soil,(0,0))

#redraw assay office
        self.bg.blit(self.office,(self.ASSAY_X,self.ASSAY_Y-self.BOARD_TOP))

# add soil
        self.gamearea.blit(self.bg,(0,0))


    def set_board(self,board):
        self.board=board

    def draw_board(self):
        for y in range(1,len(self.board)):
# make a hole
            for x in range(len(self.board[y])):
                c=self.board[y][x]
                if c!='*':
                    self.bg.fill(self.BLACK,(x*self.SQUARE_SIZE,y*self.SQUARE_SIZE,self.SQUARE_SIZE,self.SQUARE_SIZE))
                if c in '01':
                    nugg=self.nuggets[int(c)]
                    self.bg.blit(nugg,(x*self.SQUARE_SIZE,y*self.SQUARE_SIZE))
        self.gamearea.blit(self.bg,(0,0))


    def add_sprite(self,sprite):
        self.all_sprites.add(sprite)

    def setup(self):

# redraw background each time
        self.bg.blit(self.soil,(0,0))

#redraw assay office        
        self.bg.blit(self.office,(self.ASSAY_X,self.ASSAY_Y-self.BOARD_TOP))

# add soil
        self.gamearea.blit(self.bg,(0,0))
        self.screen.blit(self.gamearea,(self.BOARD_LEFT,self.BOARD_TOP))

        pygame.display.flip()
      

    def draw(self,deltat):
        self.all_sprites.update(deltat)
        self.all_sprites.draw(self.gamearea)

        self.screen.blit(self.gamearea,(self.BOARD_LEFT,self.BOARD_TOP))
        pygame.display.flip()


    def display_gold(self,gold=0):
        scoretext='%03d' % gold
        for i in range(len(scoretext)):
            num=int(scoretext[i])*24
            pos=i*24
            self.screen.blit(self.digits,(self.CASH_X+self.CASH_OFFSET+(i*24),20),(num,0,24,35))

    def display_charges(self,charges=0):
        scoretext='%02d' % charges
        for i in range(len(scoretext)):
            num=int(scoretext[i])*24
            pos=i*24
            self.screen.blit(self.digits,(self.CHARGES_X+self.CHARGES_OFFSET+(i*24),20),(num,0,24,35))

    def display_cash(self,cash=0):
        scoretext='%05d' % cash
        for i in range(len(scoretext)):
            num=int(scoretext[i])*24
            pos=i*24
            self.screen.blit(self.digits,(self.CASH_X+self.CASH_OFFSET+(i*24),66),(num,0,24,35))

    def display_health(self,health=100):
         h=int(84*(health/100.0))
         b=84-h
         c=self.GREEN
         if health<20:
             c=self.RED
         elif health<40:
             c=self.YELLOW
         self.screen.fill(c,(self.HEALTH_X,70,h,32))
         self.screen.fill(self.BLACK,(self.HEALTH_X+h,70,b,32))
#        num=int(scoretext[i])*24
#        pos=i*24
#        self.screen.blit(self.digits,(self.CASH_X+self.CASH_OFFSET+(i*24),66),(num,0,24,35))

    def display_opening(self):
        self.bg.blit(self.opening,(150,100))
        self.gamearea.blit(self.bg,(0,0))

    def display_gameover(self):
        self.bg.blit(self.gameover,(120,80))
        self.gamearea.blit(self.bg,(0,0))


    def clear_sprites(self):
        self.all_sprites.clear(self.gamearea,self.bg)

    def clear_square(self,x,y):
        self.bg.fill(self.BLACK,(x*self.SQUARE_SIZE,y*self.SQUARE_SIZE,self.SQUARE_SIZE,self.SQUARE_SIZE))

    def reset_square(self,x,y):
        xpos=x*self.SQUARE_SIZE
        ypos=y*self.SQUARE_SIZE
        self.bg.blit(self.soil,(x*self.SQUARE_SIZE,y*self.SQUARE_SIZE),(xpos,ypos,self.SQUARE_SIZE,self.SQUARE_SIZE))
        self.gamearea.blit(self.bg,(0,0))
 
